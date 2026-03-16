from flask import Flask, render_template, redirect 
from flask import  flash, request, url_for, session
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

#Generate PDF using Reportlab
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet

import mysql.connector
#object detection
from flask import request, jsonify
from ultralytics import YOLO
import numpy as np
import cv2
import base64

import os
import uuid

model = YOLO("yolov8n.pt")

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='online_exam'
    )
    return conn


app=Flask(__name__)

app.secret_key = "supersecretkey123" 

#home route
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=['POST','GET'])
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
        cursor = conn.cursor()

        # Check duplicate email
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Email already registered!", "warning")
            return redirect('/register')
        
        # Hash password
        hashed_password = generate_password_hash(password)

        # Insert user
        cursor.execute("""
            INSERT INTO users (first_name, last_name, email, phone, password)
            VALUES (%s,%s,%s,%s,%s)
        """, (f_name, l_name, email, phone, hashed_password))

        conn.commit()
        conn.close()

        flash("Registration successful! Please login.", "success")
        return redirect('/login')
    
    return render_template('register.html') 


# LOGIN ROUTE
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'],password):
            # Store user info in session
            session['user_id'] = user['id']
            session['first_name'] = user['first_name']
            session['last_name'] = user['last_name']
            session['role'] = user['role']


            # Clear old exam session data
            session.pop('exam_questions', None)
            session.pop('exam_start_time', None)
            session.pop('exam_duration', None)
            session.pop('exam_completed', None)


            # Update last_login time
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

# LOGOUT ROUTE
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

    session.clear()  # clear all session data
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

#admin route
@app.route('/admin')
def admin_dashboard():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    # Total Users
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
    total_users = cursor.fetchone()[0]

    # Students Attended Exam
    cursor.execute("SELECT COUNT(DISTINCT r.user_id) FROM results r JOIN users u ON r.user_id = u.id WHERE u.role = 'user'")
    total_attended = cursor.fetchone()[0]

    # Total Passed
    cursor.execute("SELECT COUNT(*) FROM results WHERE UPPER(status)='PASS'")
    total_passed = cursor.fetchone()[0]

    # Topper
    cursor.execute("""
    SELECT u.first_name, u.last_name, MAX(r.percentage) as max_percentage
    FROM results r
    JOIN users u ON r.user_id = u.id
    WHERE u.role = 'user'
    GROUP BY r.user_id
    ORDER BY max_percentage DESC
    LIMIT 10
    """)


    topper = cursor.fetchall()
    print(topper)
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
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM questions ORDER BY id ASC")
    questions = cursor.fetchall()
    conn.close()

    return render_template("manage_questions.html", questions=questions)

#delete question 
@app.route('/delete_question/<int:id>')
def delete_question(id):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM questions WHERE id = %s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    flash("Question deleted successfully!", "success")
    return redirect(url_for('manage_questions'))

#view users admin side 
@app.route('/view_users')
def view_users():
    if 'user_id' not in session or session['role'] != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
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
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT r.id as result_id,
           r.user_id,
           u.first_name,
           u.last_name,
           u.email,
           r.score,
           r.percentage,
           r.status,
           r.exam_date
    FROM results r
    JOIN users u ON r.user_id = u.id
    WHERE u.role = 'user'
    ORDER BY r.exam_date DESC
    """)

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('admin_results.html', results=results)

#Add Questions
@app.route('/add_question', methods=['GET', 'POST'])
def add_question():

    # Admin check
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
        mark=request.form['mark']

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO questions 
            (question, option_a, option_b, option_c, option_d, correct_option,mark)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (question, option_a, option_b, option_c, option_d, correct_option, mark))

        conn.commit()
        cursor.close()
        conn.close()

        flash("Question Added Successfully!")
        return redirect(url_for('add_question'))

    return render_template('add_question.html')

@app.route('/edit_question/<int:id>', methods=['GET', 'POST'])
def edit_question(id):
    # Admin check
    if session.get('role') != 'admin':
        flash("Unauthorized Access", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Fetch question by id
    cursor.execute("SELECT * FROM questions WHERE id=%s", (id,))
    question = cursor.fetchone()

    if not question:
        flash("Question not found!", "danger")
        cursor.close()
        conn.close()
        return redirect(url_for('admin_dashboard'))

    if request.method == 'POST':
        # Get updated data from form
        question_text = request.form['question']
        option_a = request.form['option_a']
        option_b = request.form['option_b']
        option_c = request.form['option_c']
        option_d = request.form['option_d']
        correct_option = request.form['correct_option']
        mark=request.form['mark']

        # Update in DB
        cursor.execute("""
            UPDATE questions
            SET question=%s, option_a=%s, option_b=%s, option_c=%s, option_d=%s, correct_option=%s,mark=%s
            WHERE id=%s
        """, (question_text, option_a, option_b, option_c, option_d, correct_option, mark, id))
        conn.commit()
        flash("Question updated successfully!", "success")
        cursor.close()
        conn.close()
        return redirect(url_for('admin_dashboard'))

    cursor.close()
    conn.close()
    return render_template('edit_question.html', question=question)
#violation_log
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
    cursor.close()
    conn.close()

    return {"status": "logged"}

#Admin Side View
@app.route("/admin/violations")
def view_violations():

    if "user_id" not in session or session.get("role") != "admin":
        flash("Access Denied", "danger")
        return redirect(url_for("login"))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ev.*, 
           CONCAT(u.first_name, ' ', u.last_name) AS full_name,
                   u.email
        FROM exam_violations ev
        JOIN users u ON ev.user_id = u.id
        ORDER BY ev.violation_time DESC
    """)
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("admin_violations.html", data=data)

#student route
@app.route('/student')
def student_dashboard():
    if 'user_id' not in session or session['role'] != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    return "Welcome Student!"

#exam procedure
@app.route('/exam_procedure')
def exam_procedure():
    if 'user_id' not in session or session.get('role','').strip().lower() != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))
    #checking exam start disable back 
    #if 'exam_questions' in session:
        # If exam already started, don't allow going back
        #return redirect(url_for('start_exam'))
    # Dynamic instructions
    instructions = [
        "The exam consists of Multiple Choice Questions (MCQs) only.",
        "Each question carries specific marks.",
        "All questions must be attempted within the given time.",
        "Once submitted, answers cannot be changed.",
        "Ensure a stable internet connection throughout the exam.",
        "Follow all exam rules and maintain academic integrity.",
        "Timer starts when you click Start Exam.",
        "Exam will auto-submit when time ends.",
        "Correct answer: 25 (1  marks per question)",
        "Wrong answer: 0 marks.",
        "Total score = sum of marks of all correctly answered questions",
        "Click Submit Exam once you finish.",
        "After submission, you can view results (depending on rules).",
        "Make sure all questions are answered before submitting."
        "No cheating / plagiarism.",
        "Do not share questions or answers.",
        "Follow the exam rules strictly"
    ]

    duration_minutes = 10  # exam duration
    return render_template('exam_procedure.html', instructions=instructions, duration=duration_minutes)

@app.route('/start_exam',methods=['GET','POST'])
def start_exam():

    if 'user_id' not in session or session.get('role', '').lower() != 'user':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))
    
    # 🔒 If exam already completed in this login session
    if session.get('exam_completed'):
        flash("You already completed the exam in this session.", "warning")
        return redirect(url_for('exam_procedure'))

    if 'current_question_index' not in session:
        session['current_question_index'] = 0

    # If first time starting exam
    if not session.get("exam_questions"):
        #  DELETE OLD ANSWERS BEFORE STARTING NEW EXAM
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
                DELETE FROM student_answers
                WHERE user_id=%s
            """, (session["user_id"],))

        conn.commit()
        cursor.close()
        conn.close()
        #fetch questions 
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT * FROM questions
            ORDER BY RAND()
            LIMIT 10
        """)
        questions = cursor.fetchall()

        session['exam_questions'] = [q['id'] for q in questions]

        # 🔥 STORE START TIME
        session['exam_start_time'] = datetime.now().timestamp()
        session['exam_duration'] = 600   # 10 minutes in seconds

        cursor.close()
        conn.close()

    # 🔥 CALCULATE REMAINING TIME
    start_time = session.get('exam_start_time')
    duration = session.get('exam_duration')
    
    if not start_time or not duration:
        return redirect(url_for('start_exam'))

    elapsed = datetime.now().timestamp() - start_time
    remaining_time = int(duration - elapsed)
    if remaining_time <= 0:
        flash("Exam time has expired!", "warning")
        return redirect(url_for('submit_exam'))

    # Fetch same questions
    question_ids = session['exam_questions']
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    format_strings = ','.join(['%s'] * len(question_ids))
    query = f"""
        SELECT * FROM questions
        WHERE id IN ({format_strings})
        ORDER BY FIELD(id, {format_strings})
    """

    cursor.execute(query, tuple(question_ids + question_ids))
    questions = cursor.fetchall()

    cursor.close()
    conn.close()
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
    SELECT question_id, selected_option 
    FROM student_answers
    WHERE user_id=%s
    """, (session["user_id"],))
    
    saved_data = cursor.fetchall()
    saved_answers = {row['question_id']: row['selected_option'] for row in saved_data}
    
    cursor.close()
    conn.close()

    current_index = session.get('current_question_index', 0)
    
    return render_template(
        'start_exam.html',
        questions=questions,
        remaining_time=remaining_time,
        saved_answers=saved_answers,
        current_index=current_index
    )

#Prevent Back Button Cache
@app.after_request
def add_header(response):
    # response.headers["Cache-Control"] = "no-store"
    response.headers["Cache-Control"] = "no-store"
    return response

@app.route("/save_answer", methods=["POST"])
def save_answer():
    if "user_id" not in session:
        return {"status": "error"}, 401

    data = request.get_json()

    user_id = session["user_id"]
    question_id = int(request.json.get("question_id"))
    selected_option = request.json.get("selected_option")
    current_index = data.get("current_index") 
    
    # Save current question index in session
    session['current_question_index'] = current_index

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        INSERT INTO student_answers 
        (user_id, question_id, selected_option)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE selected_option=%s
    """, (user_id, question_id, selected_option, selected_option))
    conn.commit()  
    cursor.close()
    conn.close()
    
    return {"status": "saved"}

#submit exam 
@app.route('/submit_exam', methods=['POST','GET'])
def submit_exam():

    if 'exam_questions' not in session:
        flash("Session expired. Please start exam again.", "danger")
        return redirect(url_for('start_exam'))

    total_score = 0

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    question_ids = session['exam_questions']

    format_strings = ','.join(['%s'] * len(question_ids))
    query = f"""
        SELECT * FROM questions 
        WHERE id IN ({format_strings})
        ORDER BY FIELD(id, {format_strings})
        """

    cursor.execute(query, tuple(question_ids + question_ids))
    questions = cursor.fetchall()

    # Calculate total score
    for q in questions:
        question_id = q['id']
        correct_option = q['correct_option']
        mark = q['mark']

        selected_option = request.form.get(f"question_{question_id}")

        if selected_option == correct_option:
            total_score += mark

    total_questions = len(questions)
    total_possible_marks = sum(q['mark'] for q in questions)

    percentage = (total_score / total_possible_marks) * 100 if total_possible_marks > 0 else 0
    result_status = "PASS" if percentage >= 40 else "FAIL"

    user_id = session['user_id']

    # ✅ Insert result
    cursor.execute("""
        INSERT INTO results 
        (user_id, score, percentage, status)
        VALUES (%s, %s, %s, %s)
    """, (user_id, total_score, percentage, result_status))
    conn.commit()

    # 🧹 Clear session after exam
    session['exam_completed'] = True
    session.pop('exam_questions', None)

    # Get the id of the newly inserted result
    result_id = cursor.lastrowid
     
    # Clear all exam session data
    session.pop('exam_questions', None)
    session.pop('exam_start_time', None)
    session.pop('exam_duration', None)


    # ✅ Insert each answer into results_answers
    for q in questions:
        question_id = q['id']
        selected_option = request.form.get(f"question_{question_id}") or None

        cursor.execute("""
            INSERT INTO results_answers (result_id, question_id, answer)
            VALUES (%s, %s, %s)
        """, (result_id, question_id, selected_option))

    conn.commit()

    # 🧹 Clear session after exam
    session.pop('exam_questions', None)
    session.pop('current_question_index', None)

    cursor.close()
    conn.close()

    return render_template(
        "result.html",
        score=total_score,
        total=total_questions,
        percentage=percentage,
        status=result_status,
        user_id=user_id
    )

@app.route('/review/<int:user_id>')
def review_answers(user_id):

    if 'user_id' not in session:
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 🔥 Get latest result of that user
    cursor.execute("""
        SELECT * FROM results 
        WHERE user_id=%s 
        ORDER BY id DESC 
        LIMIT 1
    """, (user_id,))
    result = cursor.fetchone()

    if not result:
        flash("No exam found to review!", "warning")
        return redirect(url_for('admin_results'))

    # 🔥 Get answers
    cursor.execute("""
        SELECT q.question, q.option_a, q.option_b, 
               q.option_c, q.option_d, 
               q.correct_option, r.answer
        FROM results_answers r
        JOIN questions q ON r.question_id = q.id
        WHERE r.result_id=%s
    """, (result['id'],))

    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('review.html', answers=answers,user_id=user_id)

@app.route('/send_review_pdf/<int:user_id>')
def send_review_pdf(user_id):

    if session.get('role') != 'admin':
        flash("Access Denied!", "danger")
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get user details
    cursor.execute("SELECT first_name, email FROM users WHERE id=%s", (user_id,))
    user = cursor.fetchone()

    # Get latest result
    cursor.execute("""
        SELECT * FROM results
        WHERE user_id=%s
        ORDER BY id DESC
        LIMIT 1
    """, (user_id,))
    result = cursor.fetchone()

    # Get answers
    cursor.execute("""
        SELECT q.question, q.option_a, q.option_b, 
               q.option_c, q.option_d, 
               q.correct_option, r.answer
        FROM results_answers r
        JOIN questions q ON r.question_id = q.id
        WHERE r.result_id=%s
    """, (result['id'],))

    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    # 🔥 Create PDF
    file_path = f"review_{user_id}.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []

    styles = getSampleStyleSheet()

    elements.append(Paragraph(f"Exam Review - {user['first_name']}", styles['Title']))
    elements.append(Spacer(1, 0.3 * inch))

    for i, ans in enumerate(answers, 1):
        elements.append(Paragraph(f"Q{i}: {ans['question']}", styles['Normal']))
        elements.append(Paragraph(f"Your Answer: {ans['answer']}", styles['Normal']))
        elements.append(Paragraph(f"Correct Answer: {ans['correct_option']}", styles['Normal']))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    # 🔥 Email Config
    sender_email = "yourgmail@gmail.com"
    sender_password = "your_app_password"

    receiver_email = "fixedrealmail@gmail.com"  # FIXED MAIL

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Student Exam Review PDF"

    message.attach(MIMEText("Please find attached review PDF.", "plain"))

    with open(file_path, "rb") as f:
        part = MIMEApplication(f.read(), Name=file_path)
        part['Content-Disposition'] = f'attachment; filename="{file_path}"'
        message.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)
        server.quit()

        flash("PDF Mail Sent Successfully!", "success")

    except Exception as e:
        print(e)
        flash("Mail Sending Failed!", "danger")

    return redirect(url_for('admin_results'))

#object detection
@app.route("/detect", methods=["POST"])
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
            cls_id = int(box.cls[0])
            class_name = model.names[cls_id]

            if class_name == "cell phone":
                violations.append("mobile_detected")

            if class_name == "person":
                person_count += 1

    if person_count > 1:
        violations.append("multiple_person_detected")

    print("Detected Violations:", violations)

    if len(violations) > 0:

        # 🔥 Save Screenshot
        filename = f"{uuid.uuid4()}.jpg"
        filepath = os.path.join("static/violations", filename)
        cv2.imwrite(filepath, frame)

        conn = get_db_connection()
        cursor = conn.cursor()

        for v in violations:
            cursor.execute("""
                INSERT INTO exam_violations 
                (user_id, violation_type, screenshot_path)
                VALUES (%s, %s, %s)
            """, (session["user_id"], v, filepath))

        conn.commit()
        cursor.close()
        conn.close()

    return jsonify({"violations": violations})

if __name__=='__main__':
    app.run(debug=True)