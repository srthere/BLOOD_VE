-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: BLOOD_VE
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `articles`
--

DROP TABLE IF EXISTS `articles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `articles` (
  `id` int(12) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) DEFAULT NULL,
  `author` varchar(100) DEFAULT NULL,
  `body` text,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `articles`
--

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;
INSERT INTO `articles` VALUES (3,'Search the longest contiguous elements','srthere','<p>vgvgvgvkv bhvhvhvhv hjkhhkh ughkk h</p>','2019-08-12 14:25:13');
/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cities`
--

DROP TABLE IF EXISTS `cities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cities` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `EMAIL` varchar(40) DEFAULT NULL,
  `CITY` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cities`
--

LOCK TABLES `cities` WRITE;
/*!40000 ALTER TABLE `cities` DISABLE KEYS */;
INSERT INTO `cities` VALUES (1,'mi.manishpathak@gmail.com','Kolkata'),(2,'jnjlkljsx','Delhi'),(3,'mi.manishpathak@gmail.com','KOLKATA'),(4,'hsjjaghs@gmail.com','KOLKATA'),(5,'shubhangi.singh29@gmail.com','GOA'),(6,'mi.manishpathak@gmail.com','KOLKATA'),(7,'shubhangi.singh29@gmail.com','KOLKATA'),(8,'mdjndsj@gmai.com','Delhi'),(10,'xiveho@vmailcloud.com','kolkata'),(11,'wozer@freemailnow.net','kolkata'),(12,'wozer@freemailnow.net','KOLKATA'),(13,'dixazoduve@direct-mail.top','kolkata'),(14,'dixazoduve@direct-mail.top','Delhi'),(15,'ayanlaha10@gmail.com','KOLKATA'),(16,'sodomamij@fastmailnow.com','Goa'),(17,'sodomamij@fastmailnow.com','Delhi'),(18,'mi.manishpathak@gmail.com','Kolkata'),(19,'mi.manishpathak@gmail.com','Kolkata');
/*!40000 ALTER TABLE `cities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(100) DEFAULT NULL,
  `USERNAME` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(100) DEFAULT NULL,
  `EMAIL` varchar(40) DEFAULT NULL,
  `BLOOD_GROUP` varchar(20) DEFAULT NULL,
  `PHONE_NUMBER` varchar(10) DEFAULT NULL,
  `ADDRESS` varchar(200) DEFAULT NULL,
  `REGISTER_DATA` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `CITY` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (8,'Manish','srthere','$5$rounds=535000$I58B3j.wDzQcwQXm$zIUINAFaXtj64.DgD3ud9Yv6l4vkk3EcwgXFiX7UXQ/','mi.manishpathak@gmail.com','O+','1234567890','dnkjndsjknfjknffs','2019-08-08 03:50:01','KOLKATA'),(9,'Manish','srkl','$5$rounds=535000$uAdH3APLvMqnhhCc$K7tfSf8p9g/xVu/G4PNh2NylKdKfSCk/b.f4k7wGiZ0','shubhangi.singh29@gmail.com','O+','1234567890','dnkjndsjknfjknffs','2019-08-08 03:50:31','KOLKATA'),(10,'Manish','hello','$5$rounds=535000$tKbchBTBeDSMXabb$qui3KD97COY6upq96J.NWTZvyu1ISSdgbgWUDDSvQz0','mdjndsj@gmai.com','A+','1234567890','dnkjndsjknfjknffs','2019-08-08 04:14:15','Delhi'),(12,'Manish','mjkl','$5$rounds=535000$wTjT/tXIcRYLQtTa$FYTmz/g4X01AzIXSwzBfRgD8OeQj53QFGDTXPswcVt.','xiveho@vmailcloud.com','A+','1234567890','dnkjndsjknfjknffs','2019-08-08 17:01:52','kolkata'),(13,'Manish','mjkl','$5$rounds=535000$32TDNh2PREf1qSdc$BTNaLcb7Zxr82UcfJZXZnWMcHPMrZdr2tGwzIe60Z6/','wozer@freemailnow.net','A+','1234567890','dnkjndsjknfjknffs','2019-08-08 17:13:32','kolkata'),(14,'Manish','mjkl','$5$rounds=535000$QFtkHmBDr0k3eSrC$nMgERp83F2bJa/cUplnqsm5ByhfHHEUomY6MjE/Hao7','wozer@freemailnow.net','O+','1234567890','dnkjndsjknfjknffs','2019-08-08 17:15:04','KOLKATA'),(15,'Manish','mjkl','$5$rounds=535000$tQmNaB2iIZCwM.2C$foByaKk0hEGOwIjc0YeIwG7PWe.C26BzP8fUhTaJun9','dixazoduve@direct-mail.top','O+','1234567890','dnkjndsjknfjknffs','2019-08-08 17:16:11','kolkata'),(16,'Manish','mjkl','$5$rounds=535000$mT8XbM.nTIHtumVL$juQNrzfPZOcsBqXC0pyoivKp4tWbmDSwCozz0AF/bX2','dixazoduve@direct-mail.top','A+','1234567890','dnkjndsjknfjknffs','2019-08-09 14:21:26','Delhi'),(17,'Ayan','ayanlaha10','$5$rounds=535000$IRIabQjiH0EZmHSs$tWQie2HpD9dvqlrn0cUgAzIraqBatzOge9ps7QhSKCB','ayanlaha10@gmail.com','AB+','9933984403','dhanbad','2019-08-09 14:25:27','KOLKATA'),(18,'Kishore','srth','$5$rounds=535000$G17Au1ETBGkpUtia$U9GK1P6u6REP1/bG7pm8jMI14eJn.hLaAFMmE1.rgQD','sodomamij@fastmailnow.com','A+','1234567890','dnkjndsjknfjknffs','2019-08-09 14:28:48','Goa'),(19,'manish','srthere','$5$rounds=535000$cISv7/bRMZB88C2C$pXKGqPR4KW5k3E/r47Rt3UbX/tStC98bu0k5q3KIajA','sodomamij@fastmailnow.com','AB+','1234567890','dnkjndsjknfjknffs','2019-08-09 14:34:59','Delhi'),(20,'Manish','manish','$5$rounds=535000$/pWJlOuUFIdagvql$7pMR0a4TgEATcBFRGtAbe.K6fSl.YhX3Ik8Y8xEBgG6','mi.manishpathak@gmail.com','O+','1234567890','dnkjndsjknfjknffs','2019-08-12 18:03:59','Kolkata'),(21,'Manish','mjkl','$5$rounds=535000$MXzXkziwk2UyUjGn$zUTnbAnmyULXQy/T/Lne1QghwiQCYNWyva8BH80VC64','mi.manishpathak@gmail.com','O+','1234567890','dnkjndsjknfjknffs','2019-08-12 18:09:34','Kolkata');
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

-- Dump completed on 2019-08-14 15:01:28
