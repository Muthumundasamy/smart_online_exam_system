-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: online_exam
-- ------------------------------------------------------
-- Server version	9.5.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ 'b149079f-f4f9-11f0-9133-9c5a443b51a0:1-1273';

--
-- Table structure for table `questions`
--

DROP TABLE IF EXISTS `questions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` text NOT NULL,
  `option_a` varchar(255) DEFAULT NULL,
  `option_b` varchar(255) DEFAULT NULL,
  `option_c` varchar(255) DEFAULT NULL,
  `option_d` varchar(255) DEFAULT NULL,
  `correct_option` varchar(1) DEFAULT NULL,
  `mark` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questions`
--

LOCK TABLES `questions` WRITE;
/*!40000 ALTER TABLE `questions` DISABLE KEYS */;
INSERT INTO `questions` VALUES (1,'What is the capital of India?','Mumbai ','Delhi','Kolkata','Chennai','B',1),(2,'what does html stand for ?','Hyper Trainer Marking Language','Hyper Text Markup Language','High Text Machine Language','Hyperlink Text Markup Level','B',1),(3,'Which data type is used to store true or false values in Python?','int','bool','float','str','B',1),(4,'Which of the following is a mutable data type in Python ?','list','string','int','tuple','D',1),(7,'What does DBMS stands for ?','Data Backup Management System','Database Management System','Digital Base Management System','Data Binary Management System','B',1),(8,'Which device is used to input data into a computer?','keyboard','speaker','printer','monitor','A',1),(9,'Which software is used to browse the internet?','excel','paint','chrome','MSword','C',1),(10,'What is the correct file extension for Python files?','.pt','.python','.pyt','.py','D',1),(11,'Which keyword is used to define a function in Python?\r\n','function','fun','def','define','C',1),(12,'What will be the output?\r\nprint(2 + 3 * 2)\r\n','10','12','8','7','C',1),(13,'Which symbol is used for comments in Python?','//','/* */','#','<--- --->','C',1),(14,'What will be the output?\r\nx = 5\r\nif x > 3:\r\n    print(\"Hello\")\r\n','hello','error','nothing','5','A',1),(15,'Which of the following is a Python loop?','for ','repeat','iterate','loop','A',1),(16,'Which keyword is used for conditional statements?','when','if','check','contion','B',1),(17,'What is the output?\r\nprint(type(10))\r\n','<class \'int\'>','int','number','interger','A',1),(18,'who is next CM in TN?','STALIN','EDAPADI','VIJAY','KAMAL','C',1);
/*!40000 ALTER TABLE `questions` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-24 17:01:00
