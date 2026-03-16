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
-- Table structure for table `exam_violations`
--

DROP TABLE IF EXISTS `exam_violations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_violations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `violation_type` varchar(100) DEFAULT NULL,
  `violation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `screenshot_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=44 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_violations`
--

LOCK TABLES `exam_violations` WRITE;
/*!40000 ALTER TABLE `exam_violations` DISABLE KEYS */;
INSERT INTO `exam_violations` VALUES (1,4,'Tab Switch','2026-02-23 16:16:38',NULL),(2,1,'Tab Switch','2026-02-23 16:39:46',NULL),(3,1,'Tab Switch','2026-02-23 16:40:19',NULL),(4,1,'Tab Switch','2026-02-23 16:46:24',NULL),(5,1,'Tab Switch','2026-02-23 16:49:27',NULL),(6,1,'Tab Switch','2026-02-23 16:49:47',NULL),(7,1,'Tab Switch','2026-02-23 16:50:37',NULL),(8,1,'Tab Switch','2026-02-23 16:52:15',NULL),(9,1,'Tab Switch','2026-02-23 16:52:19',NULL),(10,1,'Tab Switch','2026-02-23 16:52:44',NULL),(11,1,'Tab Switch','2026-02-23 16:53:49',NULL),(12,1,'Tab Switch','2026-02-24 11:11:22',NULL),(13,1,'Tab Switch','2026-02-24 11:27:56',NULL),(14,1,'Tab Switch','2026-02-24 11:33:00',NULL),(15,1,'Tab Switch','2026-02-24 11:37:45',NULL),(16,1,'Tab Switch','2026-02-24 11:54:07',NULL),(17,1,'Tab Switch','2026-02-24 11:58:03',NULL),(18,1,'Tab Switch','2026-02-24 11:58:49',NULL),(19,1,'Tab Switch','2026-02-24 12:00:29',NULL),(20,1,'Tab Switch','2026-02-24 12:00:46',NULL),(21,1,'Tab Switch','2026-02-24 12:01:47',NULL),(22,1,'DevTools Opened','2026-02-24 14:05:08',NULL),(23,1,'Tab Switch','2026-02-24 14:37:51',NULL),(24,4,'Tab Switch','2026-02-24 15:29:52',NULL),(25,1,'Tab Switch','2026-02-24 15:36:42',NULL),(26,1,'Tab Switch','2026-02-24 15:53:17',NULL),(27,1,'mobile_detected','2026-02-24 16:04:09',NULL),(28,1,'mobile_detected','2026-02-24 16:04:09',NULL),(29,1,'multiple_person_detected','2026-02-24 16:04:33',NULL),(30,1,'multiple_person_detected','2026-02-24 16:04:37',NULL),(31,1,'multiple_person_detected','2026-02-24 16:31:26','static/violations\\cdfc7212-ce4a-4fd1-997c-4cb72596f5b7.jpg'),(32,1,'mobile_detected','2026-02-24 16:31:26','static/violations\\6a47cb66-342d-449d-83e2-68b09972a397.jpg'),(33,1,'multiple_person_detected','2026-02-24 16:31:26','static/violations\\6a47cb66-342d-449d-83e2-68b09972a397.jpg'),(34,1,'mobile_detected','2026-02-24 16:31:27','static/violations\\8cb279fb-3516-44cb-a03a-f595f2d39b45.jpg'),(35,1,'multiple_person_detected','2026-02-24 16:31:28','static/violations\\8cb279fb-3516-44cb-a03a-f595f2d39b45.jpg'),(36,1,'mobile_detected','2026-02-24 16:31:28','static/violations\\242a6e03-8cab-4681-a551-11613ba740e2.jpg'),(37,1,'multiple_person_detected','2026-02-24 16:31:28','static/violations\\6c6dfe6b-3f9c-4382-9c85-bca7287c4cd9.jpg'),(38,1,'mobile_detected','2026-02-24 16:31:28','static/violations\\242a6e03-8cab-4681-a551-11613ba740e2.jpg'),(39,1,'multiple_person_detected','2026-02-24 16:31:28','static/violations\\242a6e03-8cab-4681-a551-11613ba740e2.jpg'),(40,1,'multiple_person_detected','2026-02-24 16:31:51','static/violations\\fbdecec8-d6fa-4f6f-9b00-214e25c31949.jpg'),(41,1,'multiple_person_detected','2026-02-24 16:31:54','static/violations\\ff81b580-2e7b-4af3-927e-b7d066aa66c2.jpg'),(42,1,'multiple_person_detected','2026-02-24 16:31:56','static/violations\\8c1f4e71-e28b-4275-9bb4-f7273431ba99.jpg'),(43,1,'multiple_person_detected','2026-02-24 16:32:00','static/violations\\9a1b0262-64ea-46f8-9c99-411e769a7023.jpg');
/*!40000 ALTER TABLE `exam_violations` ENABLE KEYS */;
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

-- Dump completed on 2026-02-24 17:00:58
