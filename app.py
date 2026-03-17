from flask import Flask, render_template, redirect, flash, request, url_for, session, jsonify
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

# Generate PDF using Reportlab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch

# PostgreSQL driver
import psycopg2
from psycopg2.extras import RealDictCursor

# Object detection
from ultralytics import YOLO
import numpy as np
import cv2
import base64
import os
import uuid

model = YOLO("yolov8n.pt")

def get_db_connection():
    # Render-la set panna pora Environment Variable moolama connect aagum
    db_url = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(db_url, sslmode='require')
    return conn

app = Flask(__name__)
app.secret_key = "supersecretkey123" 

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        f_name = request.form['f_name']
        l_name = request.form['l_name']
        email = request.form['email'].strip().lower()
        phone = request.form['phno']
        password = request.form['password']
        c_password = request.form['c_password']

        if password != c_password:
            flash("Passwords do not match!", "danger")
            return redirect('/register')

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered!", "warning")
            return redirect('/register')
        
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, phone, password)
            VALUES (%s,%s,%s,%s,%s)
        """, (f_name, l_name, email, phone, hashed_password))

        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect('/login')
    
    return render_template('register.html') 

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['role'] = user['role']

            session.pop('exam_questions', None)
            session.pop('exam_start_time', None)
            session.pop('exam_duration', None)
            session.pop('exam_completed', None)

            cursor.execute(
                "UPDATE users SET last_login=%s WHERE id=%s", 
                (datetime.now(), user['id'])
            )
            conn.commit()
            conn.close()

            flash(f"Welcome {user['first_name']}!", 'success')

            if user['role'] == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('exam_procedure'))
        else:
            conn.close()
            flash('Invalid Email or Password!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET last_logout=%s WHERE id=%s",
            (datetime.now(), user_id)
        )
        conn.commit()
        conn.close()

    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT r.user_id) FROM results r JOIN users u ON r.user_id = u.id WHERE u.role = 'user'")
    total_attended = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM results WHERE UPPER(status)='PASS'")
    total_passed = cursor.fetchone()[0]

    cursor.execute("""
        SELECT u.first_name, u.last_name, MAX(r.percentage) as max_percentage
        FROM results r
        JOIN users u ON r.user_id = u.id
        WHERE u.role = 'user'
        GROUP BY u.first_name, u.last_name, r.user_id
        ORDER BY max_percentage DESC
        LIMIT 10
    """)
    topper = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_attended=total_attended,
        total_passed=total_passed,
        topper=topper
    )

@app.route('/manage_questions')
def manage_questions():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM questions ORDER BY id ASC")
    questions = cursor.fetchall()
    conn.close()

    return render_template("manage_questions.html", questions=questions)

@app.route('/delete_question/<int:id>')
def delete_question(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    flash("Question deleted successfully!", "success")
    return redirect(url_for('manage_questions'))

@app.route('/view_users')
def view_users():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT id, first_name, last_name, email, role FROM users")
    users = cursor.fetchall()
    conn.close()

    return render_template('view_users.html', users=users)

@app.route('/admin_results')
def admin_results():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT r.id as result_id, r.user_id, u.first_name, u.last_name, u.email,
               r.score, r.percentage, r.status, r.exam_date
        FROM results r
        JOIN users u ON r.user_id = u.id
        WHERE u.role = 'user'
        ORDER BY r.exam_date DESC
    """)
    results = cursor.fetchall()
    conn.close()
    return render_template('admin_results.html', results=results)

@app.route('/add_question', methods=['GET', 'POST'])
def add_question():
    if session.get('role') != 'admin':
        flash("Unauthorized Access")
        return redirect(url_for('login'))

    if request.method == 'POST':
        question = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']
        mark = request.form['mark']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO questions 
            (question, option_a, option_b, option_c, option_d, correct_option, mark)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (question, option_a, option_b, option_c, option_d, correct_option, mark))
        conn.commit()
        conn.close()
        flash("Question Added Successfully!")
        return redirect(url_for('add_question'))

    return render_template('add_question.html')

@app.route('/edit_question/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    if session.get('role') != 'admin':
        flash("Unauthorized Access", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("SELECT * FROM questions WHERE id=%s", (id,))
    question = cursor.fetchone()

    if request.method == 'POST':
        question_text = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']
        mark = request.form['mark']

        cursor.execute("""
            UPDATE questions
            SET question=%s, option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s, mark=%s
            WHERE id=%s
        """, (question_text, option_a, option_b, option_c, option_d, correct_option, mark, id))
        conn.commit()
        conn.close()
        flash("Question updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    conn.close()
    return render_template('edit_question.html', question=question)

@app.route("/log_violation", methods=["POST"])
def log_violation():
    if "user_id" not in session:
        return {"status": "error"}, 401
    data = request.get_json()
    violation_type = data.get("type")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO exam_violations (user_id, violation_type)
        VALUES (%s, %s)
    """, (session["user_id"], violation_type))
    conn.commit()
    conn.close()
    return {"status": "logged"}

@app.route("/admin/violations")
def view_violations():
    if "user_id" not in session or session.get("role") != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    cursor.execute("""
        SELECT ev.*, CONCAT(u.first_name, ' ', u.last_name) AS full_name, u.email
        FROM exam_violations ev
        JOIN users u ON ev.user_id = u.id
        ORDER BY ev.violation_time DESC
    """)
    data = cursor.fetchall()
    conn.close()
    return render_template("admin_violations.html", data=data)

@app.route('/exam_procedure')
def exam_procedure():
    if 'user_id' not in session or session.get('role','').strip().lower() != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))
    instructions = [
        "The exam consists of Multiple Choice Questions (MCQs) only.",
        "Each question carries specific marks.",
        "Click Submit Exam once you finish."
    ]
    duration_minutes = 10
    return render_template('exam_procedure.html', instructions=instructions, duration=duration_minutes)

@app.route('/start_exam', methods=['GET','POST'])
def start_exam():
    if 'user_id' not in session or session.get('role', '').lower() != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))
    
    if session.get('exam_completed'):
        flash("You already completed the exam.", "warning")
        return redirect(url_for('exam_procedure'))

    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    if not session.get("exam_questions"):
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("DELETE FROM student_answers WHERE user_id=%s", (session["user_id"],))
        conn.commit()

        # Postgres uses RANDOM()
        cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 10")
        questions = cursor.fetchall()
        session['exam_questions'] = [q['id'] for q in questions]
        session['exam_start_time'] = datetime.now().timestamp()
        session['exam_duration'] = 600
        conn.close()

    start_time = session.get('exam_start_time')
    duration = session.get('exam_duration')
    elapsed = datetime.now().timestamp() - start_time
    remaining_time = int(duration - elapsed)
    
    if remaining_time <= 0:
        return redirect(url_for('submit_exam'))

    question_ids = session['exam_questions']
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Use ANY for Postgres array matching to preserve ID list
    cursor.execute("SELECT * FROM questions WHERE id = ANY(%s)", (question_ids,))
    questions = cursor.fetchall()
    # Sort manually to maintain session order if needed
    questions.sort(key=lambda x: question_ids.index(x['id']))

    cursor.execute("SELECT question_id, selected_option FROM student_answers WHERE user_id=%s", (session["user_id"],))
    saved_answers = {row['question_id']: row['selected_option'] for row in cursor.fetchall()}
    conn.close()

    return render_template('start_exam.html', questions=questions, remaining_time=remaining_time, 
                           saved_answers=saved_answers, current_index=session.get('current_question_index', 0))

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/save_answer", methods=["POST"])
def save_answer():
    if "user_id" not in session:
        return {"status": "error"}, 401
    data = request.get_json()
    user_id = session["user_id"]
    question_id = int(data.get("question_id"))
    selected_option = data.get("selected_option")
    session['current_question_index'] = data.get("current_index")

    conn = get_db_connection()
    cursor = conn.cursor()
    # Postgres UPSERT syntax
    cursor.execute("""
        INSERT INTO student_answers (user_id, question_id, selected_option)
        VALUES (%s, %s, %s)
        ON CONFLICT (user_id, question_id) DO UPDATE SET selected_option = EXCLUDED.selected_option
    """, (user_id, question_id, selected_option))
    conn.commit()
    conn.close()
    return {"status": "saved"}

@app.route('/submit_exam', methods=['POST','GET'])
def submit_exam():
    if 'exam_questions' not in session:
        return redirect(url_for('start_exam'))

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    question_ids = session['exam_questions']
    cursor.execute("SELECT * FROM questions WHERE id = ANY(%s)", (question_ids,))
    questions = cursor.fetchall()

    total_score = 0
    for q in questions:
        selected = request.form.get(f"question_{q['id']}")
        if selected == q['correct_option']:
            total_score += q['mark']

    total_possible = sum(q['mark'] for q in questions)
    percentage = (total_score / total_possible) * 100 if total_possible > 0 else 0
    status = "PASS" if percentage >= 40 else "FAIL"

    # Postgres RETURNING to get ID
    cursor.execute("""
        INSERT INTO results (user_id, score, percentage, status)
        VALUES (%s, %s, %s, %s) RETURNING id
    """, (session['user_id'], total_score, percentage, status))
    result_id = cursor.fetchone()['id']

    for q in questions:
        selected = request.form.get(f"question_{q['id']}") or None
        cursor.execute("INSERT INTO results_answers (result_id, question_id, answer) VALUES (%s, %s, %s)",
                       (result_id, q['id'], selected))

    conn.commit()
    session['exam_completed'] = True
    session.pop('exam_questions', None)
    conn.close()

    return render_template("result.html", score=total_score, total=len(questions), 
                           percentage=percentage, status=status, user_id=session['user_id'])

@app.route('/detect', methods=["POST"])
def detect():
    data = request.json["image"]
    img_bytes = base64.b64decode(data.split(",")[1])
    np_arr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    results = model(frame)
    violations = []
    person_count = 0

    for r in results:
        for box in r.boxes:
            class_name = model.names[int(box.cls[0])]
            if class_name == "cell phone": violations.append("mobile_detected")
            if class_name == "person": person_count += 1
    if person_count > 1: violations.append("multiple_person_detected")

    if violations:
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join("static/violations", filename)
        # Ensure folder exists
        os.makedirs("static/violations", exist_ok=True)
        cv2.imwrite(filepath, frame)
        conn = get_db_connection()
        cursor = conn.cursor()
        for v in violations:
            cursor.execute("INSERT INTO exam_violations (user_id, violation_type, screenshot_path) VALUES (%s, %s, %s)",
                           (session["user_id"], v, filepath))
        conn.commit()
        conn.close()
    return jsonify({"violations": violations})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
