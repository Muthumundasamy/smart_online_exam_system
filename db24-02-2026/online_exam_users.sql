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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(100) DEFAULT NULL,
  `last_name` varchar(100) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'user',
  `last_login` datetime DEFAULT NULL,
  `last_logout` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Muthu','Selvi','muthu@gmail.com','9023232329','pbkdf2:sha256:600000$JVqLO8k7tzcrMOfQ$65659c4e053c60b15e57eb7873c57e71926e2e24adadd6b13b182115d199403b','user','2026-02-24 16:30:53','2026-02-24 16:32:16'),(2,'admin','admin','admin@gmail.com','XXXXXXXXX','pbkdf2:sha256:600000$odUusLJPLrg5DBnG$9a5b82dfc8aaf58d8792426766c53432ae0c69a3928ac50bd12bf8f3d6d03e01','admin','2026-02-24 16:32:38','2026-02-24 15:27:30'),(4,'sai','sri','sai@gmail.com','1232323343','pbkdf2:sha256:600000$xp1XQWHfTYAbf5wN$ec881987bfcf1e03d22b9c1e9b0773f45f0577e621d9372fbdc456931e3539f6','user','2026-02-24 15:27:40','2026-02-23 16:38:42'),(5,'sri','hari','hari@gmail.com','9023232329','pbkdf2:sha256:600000$zIr8nHbPdbOg99vP$44631e435c9c17604173dccc672f9a03bbc0846da9076cb9fd6403387d257342','user','2026-02-17 16:05:59','2026-02-17 12:05:28'),(6,'Ananthi','  ','ananthi@gmail.com','78978978','pbkdf2:sha256:600000$8Nw8v2vaU0VnDsuP$75d0f2c933924a2046c52cc5277f6defc26a2241d77bb1700ee0c61d60b8376f','user','2026-02-16 12:58:42','2026-02-16 12:59:56'),(7,'MEE','sri','meena@gmail.com','9944332277','pbkdf2:sha256:600000$mToMD2B4yn9VJafw$ce0d6bdad4863521810d2d51748b42d2701ca6069147ea00669cd3bb4e70f003','user','2026-02-19 14:43:03','2026-02-17 11:43:36'),(8,'hari','prasadh','prasadh@gmail.com','9838989889','pbkdf2:sha256:600000$igI3Nv8FXSUQLxnv$a59878a8b9cfa67e5b1e2926430377f2cefbcc69854e9a3743c296347ceb408d','user','2026-02-17 10:30:28','2026-02-17 11:27:14');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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

-- Dump completed on 2026-02-24 17:00:59
