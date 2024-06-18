-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: std_2405_exam
-- ------------------------------------------------------
-- Server version	8.0.37

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

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `book_id` int NOT NULL,
  `genre_id` int NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `genre_idx` (`genre_id`),
  KEY `book_genre_idx` (`genre_id`),
  CONSTRAINT `book` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `genre` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (8,1),(21,1),(23,1),(24,1),(19,4),(21,4),(8,5),(21,5),(22,5),(23,5),(22,6),(23,6),(24,6),(23,7);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `description` text NOT NULL,
  `year` year NOT NULL,
  `publisher` varchar(45) NOT NULL,
  `author` varchar(45) NOT NULL,
  `volume` int NOT NULL,
  `image_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `book_image_idx` (`image_id`),
  CONSTRAINT `book_image` FOREIGN KEY (`image_id`) REFERENCES `images` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (8,'7','<a href=\"1\">милое место</a>',2003,'2','6',111,15),(19,'2','2',1997,'2','2',2,20),(21,'3','4',2003,'3','3',3,20),(22,'15555','Ну туда сьда',2020,'Я','Я',1114,21),(23,'Gfd','Asddd',1999,'1','A',1554,22),(24,'Saddd','Asd',1977,'Gfdg','Sadasd',16,20);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int NOT NULL AUTO_INCREMENT,
  `genre` varchar(45) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `genrescol_UNIQUE` (`genre`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (6,'Повесть'),(5,'Поэма'),(7,'Роман'),(1,'Романтика'),(4,'Сказка'),(2,'Фентези'),(3,'Эпос');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` int NOT NULL AUTO_INCREMENT,
  `file_name` varchar(256) NOT NULL,
  `mime_type` varchar(128) NOT NULL,
  `md5_hash` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES (15,'2a7290f41569dec9c055bba5aa32e01f.JPG','image/jpeg','2a7290f41569dec9c055bba5aa32e01f'),(20,'2283edc03bd4ba689534156417b8490d.jpg','image/jpeg','2283edc03bd4ba689534156417b8490d'),(21,'8fc04e81bb2460b94a72068cec8d4ed4.jpeg','image/jpeg','8fc04e81bb2460b94a72068cec8d4ed4'),(22,'f51ce7b6049d6247e260c73273eb6aaa.jpg','image/jpeg','f51ce7b6049d6247e260c73273eb6aaa');
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int NOT NULL AUTO_INCREMENT,
  `book_id` int NOT NULL,
  `user_id` int NOT NULL,
  `rating` int NOT NULL,
  `text` text NOT NULL,
  `added_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `review_user_idx` (`user_id`),
  KEY `review_book_idx` (`book_id`),
  CONSTRAINT `review_book` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `review_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (2,8,2,1,'Увы','2024-06-17 22:04:13'),(3,8,4,4,'А мне понравилось','2024-06-17 22:15:27'),(4,8,3,5,'<a href=\"\">asdasd</a>','2024-06-17 23:38:08');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int NOT NULL AUTO_INCREMENT,
  `role` varchar(45) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Пользователь','Обычный пользователь, может только смотреть на книги'),(2,'Модератор','Может редактировать книги'),(3,'Администратор','Может добавлять и удалять книги');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(45) NOT NULL,
  `pass_hash` varchar(256) NOT NULL,
  `surname` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `patronymic` varchar(45) DEFAULT NULL,
  `role_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_role_idx` (`role_id`),
  CONSTRAINT `user_role` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (2,'admin','c79d09cdddb46ea9634a6ed83631ff950fa488fe39762f5ccd8573c4fcdea8ad','adminov','admin','adminovich',3),(3,'moder','26d58d1f740d18afb17843bde5619c20ecb840834d8d50d8d8635bb4470c756b','moderove','moder','moderovich',2),(4,'biba','c7d53ee64d57e783b539c09923069280b95a212a36e84b308e15ad6f09a6fd6e','bibov','biba','bibovich',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-18  4:11:24
