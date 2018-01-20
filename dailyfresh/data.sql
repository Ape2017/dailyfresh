-- MySQL dump 10.13  Distrib 5.7.19, for Linux (x86_64)
--
-- Host: localhost    Database: dailyfresh
-- ------------------------------------------------------
-- Server version	5.7.19-0ubuntu0.16.04.1-log

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
-- Table structure for table `df_goods_category`
--

DROP TABLE IF EXISTS `df_goods_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods_category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(20) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `image` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods_category`
--

LOCK TABLES `df_goods_category` WRITE;
/*!40000 ALTER TABLE `df_goods_category` DISABLE KEYS */;
INSERT INTO `df_goods_category` VALUES (1,'2017-10-16 03:00:01.655105','2017-10-16 03:00:01.655201','新鲜水果','fruit','group1/M00/00/00/CtM3BVnkILGACHh0AAAmv27pX4k2790330'),(2,'2017-10-16 03:00:26.853310','2017-10-16 03:00:26.853397','海鲜水产','seafood','group1/M00/00/00/CtM3BVnkIMqAW9MwAABHr3RQqFs8076962'),(3,'2017-10-16 03:00:41.396890','2017-10-16 03:00:41.397121','猪牛羊肉','meet','group1/M00/00/00/CtM3BVnkINmAEIKKAAAy1Tlm9So4047150'),(4,'2017-10-16 03:00:55.190135','2017-10-16 03:00:55.190223','禽类蛋品','egg','group1/M00/00/00/CtM3BVnkIOeAG0B6AAAqR4DoSUg1061194'),(5,'2017-10-16 03:01:24.116307','2017-10-16 03:01:24.116640','新鲜蔬菜','vegetables','group1/M00/00/00/CtM3BVnkIQSARC1UAAA-0ZoYkpM7754350'),(6,'2017-10-16 03:01:54.662968','2017-10-16 03:01:54.663066','速冻食品','ice','group1/M00/00/00/CtM3BVnkISKAJwJqAAA3sZPrVzQ4838643');
/*!40000 ALTER TABLE `df_goods_category` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods`
--

DROP TABLE IF EXISTS `df_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  `desc` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods`
--

LOCK TABLES `df_goods` WRITE;
/*!40000 ALTER TABLE `df_goods` DISABLE KEYS */;
INSERT INTO `df_goods` VALUES (1,'2017-10-16 03:03:05.257969','2017-10-16 03:03:05.258130','草莓','<p><strong>很不错的草莓</strong></p>'),(2,'2017-10-16 03:05:36.964951','2017-10-16 03:05:36.965129','葡萄',''),(3,'2017-10-16 03:05:52.323866','2017-10-16 03:05:52.323949','柠檬',''),(4,'2017-10-16 03:06:01.267481','2017-10-16 03:06:01.267615','奇异果',''),(5,'2017-10-16 03:06:30.418683','2017-10-16 03:06:30.418789','大青虾',''),(6,'2017-10-16 03:06:35.994464','2017-10-16 03:06:35.994567','秋刀鱼',''),(7,'2017-10-16 03:06:48.115318','2017-10-16 03:06:48.115410','扇贝',''),(8,'2017-10-16 03:07:03.057514','2017-10-16 03:07:03.057601','基围虾',''),(9,'2017-10-16 03:07:36.306725','2017-10-16 03:07:36.306926','猪肉',''),(10,'2017-10-16 03:07:39.056064','2017-10-16 03:07:39.056145','牛肉',''),(11,'2017-10-16 03:07:41.955755','2017-10-16 03:07:41.955833','羊肉',''),(12,'2017-10-16 03:07:44.741474','2017-10-16 03:07:44.741574','牛排',''),(13,'2017-10-16 03:07:51.748699','2017-10-16 03:07:51.748828','鸡蛋',''),(14,'2017-10-16 03:07:56.413773','2017-10-16 03:07:56.413853','鸡肉',''),(15,'2017-10-16 03:07:59.568405','2017-10-16 03:07:59.568554','鸭蛋',''),(16,'2017-10-16 03:08:03.020608','2017-10-16 03:08:03.020764','鸡腿',''),(17,'2017-10-16 03:08:10.063820','2017-10-16 03:08:10.063898','白菜',''),(18,'2017-10-16 03:08:13.315906','2017-10-16 03:08:13.316025','芹菜',''),(19,'2017-10-16 03:08:16.351445','2017-10-16 03:08:16.351526','香菜',''),(20,'2017-10-16 03:08:24.232660','2017-10-16 03:08:24.232743','冬瓜',''),(21,'2017-10-16 03:08:36.939678','2017-10-16 03:08:36.940113','鱼丸',''),(22,'2017-10-16 03:08:43.194862','2017-10-16 03:08:43.194985','蟹棒',''),(23,'2017-10-16 03:08:50.771785','2017-10-16 03:08:50.771931','虾丸',''),(24,'2017-10-16 03:09:01.546052','2017-10-16 03:09:01.546152','速冻水饺','');
/*!40000 ALTER TABLE `df_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods_sku`
--

DROP TABLE IF EXISTS `df_goods_sku`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods_sku` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  `title` varchar(200) NOT NULL,
  `unit` varchar(10) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock` int(11) NOT NULL,
  `sales` int(11) NOT NULL,
  `default_image` varchar(100) NOT NULL,
  `status` tinyint(1) NOT NULL,
  `category_id` int(11) NOT NULL,
  `goods_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_goods_sku_category_id_c87ff048768edce_fk_df_goods_category_id` (`category_id`),
  KEY `df_goods_sku_goods_id_65edd041dfc86646_fk_df_goods_id` (`goods_id`),
  CONSTRAINT `df_goods_sku_category_id_c87ff048768edce_fk_df_goods_category_id` FOREIGN KEY (`category_id`) REFERENCES `df_goods_category` (`id`),
  CONSTRAINT `df_goods_sku_goods_id_65edd041dfc86646_fk_df_goods_id` FOREIGN KEY (`goods_id`) REFERENCES `df_goods` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods_sku`
--

LOCK TABLES `df_goods_sku` WRITE;
/*!40000 ALTER TABLE `df_goods_sku` DISABLE KEYS */;
INSERT INTO `df_goods_sku` VALUES (1,'2017-10-16 03:10:14.045538','2017-10-16 03:10:14.045649','草莓 500g','草莓简介','500g',10.00,98,0,'group1/M00/00/00/CtM3BVnkIxaAR7GHAAAljHPuXJg5431541',1,1,1),(2,'2017-10-16 03:11:04.490384','2017-10-16 03:11:04.490462','盒装草莓','草莓简介','盒',20.00,10,0,'group1/M00/00/00/CtM3BVnkI0iAUprjAAAljHPuXJg5371806',1,1,1),(3,'2017-10-16 03:12:32.165020','2017-10-16 03:12:32.165114','葡萄','葡萄简介','500g',20.00,7,0,'group1/M00/00/00/CtM3BVnkI6CAURm4AAAjjiYTEkw1194059',1,1,2),(4,'2017-10-16 03:13:16.457844','2017-10-16 03:13:16.457926','柠檬','简介','500g',32.00,12,0,'group1/M00/00/00/CtM3BVnkI8yAHR3YAAAgnaeGwNQ6779834',1,1,3),(5,'2017-10-16 03:14:05.799352','2017-10-16 03:14:05.799588','奇异果','简介','500g',12.12,12,0,'group1/M00/00/00/CtM3BVnkI_2AToqyAAAeuLYy0pU9946037',1,1,4),(6,'2017-10-16 03:15:09.971968','2017-10-16 03:15:09.972047','大青虾','简介','500g',34.00,12,0,'group1/M00/00/00/CtM3BVnkJD2AQx9zAAAk0DN4-yE8467862',1,2,5),(7,'2017-10-16 03:15:53.812181','2017-10-16 03:15:53.812292','北海道秋刀鱼','简介','500g',50.00,15,0,'group1/M00/00/00/CtM3BVnkJGmAecHxAAAkaP_7_181619603',1,2,6),(8,'2017-10-16 03:16:24.763232','2017-10-16 03:16:24.763324','扇贝','简介','500g',56.60,13,0,'group1/M00/00/00/CtM3BVnkJIiAd8kxAAAk8WCqqmI1965678',1,2,7),(9,'2017-10-16 03:17:13.426611','2017-10-16 03:17:13.426790','基围虾','简介','500g',100.90,14,0,'group1/M00/00/00/CtM3BVnkJLmAI1K-AAAkaP_7_189355042',1,2,8),(10,'2017-10-16 03:17:47.656066','2017-10-16 03:17:47.656152','猪肉','简介','500g',23.99,100,0,'group1/M00/00/00/CtM3BVnkJNuADLYAAAAWnwO6wpU7499459',1,3,9),(11,'2017-10-16 03:18:15.497630','2017-10-16 03:18:15.497764','牛肉','简介','500g',34.99,100,0,'group1/M00/00/00/CtM3BVnkJPeAc2aGAAAcLRyfMSc4681259',1,3,10),(12,'2017-10-16 03:18:44.453933','2017-10-16 03:18:44.454010','羊肉','简介','500g',56.99,100,0,'group1/M00/00/00/CtM3BVnkJRSAXMuGAAAgbU6nbaA2977481',1,3,11),(13,'2017-10-16 03:19:10.209472','2017-10-16 03:19:10.209556','牛排','简介','500g',99.99,100,0,'group1/M00/00/00/CtM3BVnkJS6AVSDWAAAgrKNKuOg9088924',1,3,12),(14,'2017-10-16 03:19:44.020204','2017-10-16 03:19:44.020284','盒装鸡蛋','简介','500g',23.00,100,0,'group1/M00/00/00/CtM3BVnkJVCAFDKSAAAk8WCqqmI8466582',1,4,13),(15,'2017-10-16 03:20:20.962831','2017-10-16 03:20:20.963038','鸡肉','简介','500g',32.00,100,0,'group1/M00/00/00/CtM3BVnkJXSAXbesAAAiQjDS7wA8116965',1,4,14),(16,'2017-10-16 03:20:53.724305','2017-10-16 03:20:53.724397','鸭蛋','简介','盒',45.00,121,0,'group1/M00/00/00/CtM3BVnkJZWAIwBOAAAiQjDS7wA4382174',1,4,15),(17,'2017-10-16 03:21:22.965398','2017-10-16 03:21:22.965474','鸡腿','简介','500g',45.00,12,0,'group1/M00/00/00/CtM3BVnkJbKADk2yAAAWnwO6wpU5481130',1,4,16),(18,'2017-10-16 03:22:04.462490','2017-10-16 03:22:04.462571','白菜','简介','500g',4.50,100,0,'group1/M00/00/00/CtM3BVnkJdyAKycGAAAaabPqzqc6717404',1,5,17),(19,'2017-10-16 03:22:31.745392','2017-10-16 03:22:31.745499','芹菜','简介','500g',3.50,12,0,'group1/M00/00/00/CtM3BVnkJfeAVv-jAAAjjiYTEkw8506724',1,5,18),(20,'2017-10-16 03:23:21.161526','2017-10-16 03:23:21.162070','香菜','简介','500g',7.90,100,0,'group1/M00/00/00/CtM3BVnkJimAEK7MAAAcLRyfMSc6464688',1,5,19),(21,'2017-10-16 03:23:46.986158','2017-10-16 03:23:46.986234','冬瓜','简介','500g',12.99,100,0,'group1/M00/00/00/CtM3BVnkJkKAQdJrAAAhst2hSFQ6848699',1,5,20),(22,'2017-10-16 03:24:10.445214','2017-10-16 03:24:10.445291','鱼丸','简介','500g',66.00,12,0,'group1/M00/00/01/CtM3BVnkJlqAePKjAAAcLRyfMSc8759431',1,6,21),(23,'2017-10-16 03:24:37.927158','2017-10-16 03:24:37.927235','蟹棒','简介','500g',68.00,100,0,'group1/M00/00/01/CtM3BVnkJnWAUV_LAAAljHPuXJg1247606',1,6,22),(24,'2017-10-16 03:25:18.235816','2017-10-16 03:25:18.235901','虾丸','简介','500g',89.99,100,0,'group1/M00/00/01/CtM3BVnkJp6AHVPPAAAZxC0XRLc2377246',1,6,23),(25,'2017-10-16 03:25:56.170531','2017-10-16 03:25:56.170611','速冻水饺','简介','袋',20.00,100,0,'group1/M00/00/01/CtM3BVnkJsSAYntSAAAcLRyfMSc1347281',1,6,24);
/*!40000 ALTER TABLE `df_goods_sku` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_goods_image`
--

DROP TABLE IF EXISTS `df_goods_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_goods_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `image` varchar(100) NOT NULL,
  `sku_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_goods_image_22ad5bca` (`sku_id`),
  CONSTRAINT `df_goods_image_sku_id_75ce8a33cdb24519_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_goods_image`
--

LOCK TABLES `df_goods_image` WRITE;
/*!40000 ALTER TABLE `df_goods_image` DISABLE KEYS */;
INSERT INTO `df_goods_image` VALUES (1,'2017-10-16 03:26:50.235040','2017-10-16 03:26:50.235119','group1/M00/00/01/CtM3BVnkJvqARg4OAAAm3lfXL-Q4989750',1),(2,'2017-10-16 03:26:58.043760','2017-10-16 03:26:58.043856','group1/M00/00/01/CtM3BVnkJwKAMbGgAAAm3lfXL-Q2310134',2);
/*!40000 ALTER TABLE `df_goods_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_index_goods`
--

DROP TABLE IF EXISTS `df_index_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_index_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `image` varchar(100) NOT NULL,
  `index` smallint(6) NOT NULL,
  `sku_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_index_goods_sku_id_59fb549b9bbac669_fk_df_goods_sku_id` (`sku_id`),
  CONSTRAINT `df_index_goods_sku_id_59fb549b9bbac669_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_index_goods`
--

LOCK TABLES `df_index_goods` WRITE;
/*!40000 ALTER TABLE `df_index_goods` DISABLE KEYS */;
INSERT INTO `df_index_goods` VALUES (1,'2017-10-16 03:27:56.534441','2017-10-16 03:27:56.534522','group1/M00/00/01/CtM3BVnkJzyASv1nAACpB-LsCdE4728457',0,3),(2,'2017-10-16 03:28:10.145716','2017-10-16 03:28:10.145795','group1/M00/00/01/CtM3BVnkJ0qARP2PAAC3B-z8J2c2451336',1,5),(3,'2017-10-16 03:28:30.520445','2017-10-16 03:28:30.520521','group1/M00/00/01/CtM3BVnkJ16AWegCAAETwXb_pso1012026',2,10),(4,'2017-10-16 03:32:40.934947','2017-10-16 03:32:40.935037','group1/M00/00/01/CtM3BVnkKFiAXsNcAAD0akkXmFo4487232',3,6);
/*!40000 ALTER TABLE `df_index_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_index_category_goods`
--

DROP TABLE IF EXISTS `df_index_category_goods`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_index_category_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `display_type` smallint(6) NOT NULL,
  `index` smallint(6) NOT NULL,
  `category_id` int(11) NOT NULL,
  `sku_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `df_index_cat_category_id_19bdee5083c88d5_fk_df_goods_category_id` (`category_id`),
  KEY `df_index_category_goo_sku_id_5a1bd13e4d7c3156_fk_df_goods_sku_id` (`sku_id`),
  CONSTRAINT `df_index_cat_category_id_19bdee5083c88d5_fk_df_goods_category_id` FOREIGN KEY (`category_id`) REFERENCES `df_goods_category` (`id`),
  CONSTRAINT `df_index_category_goo_sku_id_5a1bd13e4d7c3156_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_index_category_goods`
--

LOCK TABLES `df_index_category_goods` WRITE;
/*!40000 ALTER TABLE `df_index_category_goods` DISABLE KEYS */;
INSERT INTO `df_index_category_goods` VALUES (1,'2017-10-16 03:33:46.743381','2017-10-16 03:33:46.743473',1,0,1,1),(2,'2017-10-16 03:33:57.241666','2017-10-16 03:33:57.241795',1,1,1,3),(3,'2017-10-16 03:34:09.716055','2017-10-16 03:34:09.716135',1,3,1,4),(4,'2017-10-16 03:34:49.901895','2017-10-16 03:34:49.902017',1,2,1,5),(5,'2017-10-16 03:35:07.990622','2017-10-16 03:35:07.990702',0,0,1,3),(6,'2017-10-16 03:35:18.892346','2017-10-16 03:35:18.892427',0,1,1,2),(7,'2017-10-16 03:35:28.860398','2017-10-16 03:35:28.860473',1,0,2,6),(8,'2017-10-16 03:35:45.966738','2017-10-16 03:35:45.966841',1,1,2,7),(9,'2017-10-16 03:35:55.209654','2017-10-16 03:35:55.209735',1,2,2,7),(10,'2017-10-16 03:36:05.106142','2017-10-16 03:36:05.106274',1,2,2,8),(11,'2017-10-16 03:36:15.971654','2017-10-16 03:36:15.971736',1,3,2,9),(12,'2017-10-16 03:36:24.626355','2017-10-16 03:36:24.626430',0,0,2,8),(13,'2017-10-16 03:36:40.897798','2017-10-16 03:36:40.897887',0,1,2,9),(14,'2017-10-16 03:37:11.911978','2017-10-16 03:37:11.912057',1,0,3,10),(15,'2017-10-16 03:37:24.784141','2017-10-16 03:37:24.784249',1,1,3,11),(16,'2017-10-16 03:37:33.887044','2017-10-16 03:37:33.887126',1,2,3,12),(17,'2017-10-16 04:06:16.091371','2017-10-16 04:06:16.091567',1,3,3,13),(18,'2017-10-16 04:06:57.562512','2017-10-16 04:06:57.562601',0,0,3,12),(19,'2017-10-16 04:07:05.412979','2017-10-16 04:07:05.413066',0,1,3,11),(20,'2017-10-16 04:07:17.042627','2017-10-16 04:07:17.042708',1,0,4,14),(21,'2017-10-16 04:07:25.607347','2017-10-16 04:07:25.607439',1,1,4,15),(22,'2017-10-16 04:07:37.327826','2017-10-16 04:07:37.327903',1,2,4,16),(23,'2017-10-16 04:07:46.115468','2017-10-16 04:07:46.115679',1,3,4,17),(24,'2017-10-16 04:07:58.518953','2017-10-16 04:07:58.519085',0,0,4,15),(25,'2017-10-16 04:08:08.603445','2017-10-16 04:08:08.603576',1,0,5,18),(26,'2017-10-16 04:08:20.212045','2017-10-16 04:08:20.212207',1,1,5,19),(27,'2017-10-16 04:08:27.535621','2017-10-16 04:08:27.535700',1,2,5,20),(28,'2017-10-16 04:08:41.184969','2017-10-16 04:08:41.185046',1,3,5,21),(29,'2017-10-16 04:08:48.173697','2017-10-16 04:08:48.174095',0,0,5,21),(30,'2017-10-16 04:08:57.442308','2017-10-16 04:08:57.442389',1,0,6,22),(31,'2017-10-16 04:09:06.721210','2017-10-16 04:09:06.721292',1,1,6,23),(32,'2017-10-16 04:09:16.107585','2017-10-16 04:09:16.108236',1,2,6,24),(33,'2017-10-16 04:09:23.550951','2017-10-16 04:09:23.551031',1,3,6,25),(34,'2017-10-16 04:09:30.560733','2017-10-16 04:09:30.560816',0,0,6,23),(35,'2017-10-16 04:09:38.751619','2017-10-16 04:09:38.751712',0,1,6,22);
/*!40000 ALTER TABLE `df_index_category_goods` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `df_index_promotion`
--

DROP TABLE IF EXISTS `df_index_promotion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `df_index_promotion` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime(6) NOT NULL,
  `update_time` datetime(6) NOT NULL,
  `name` varchar(50) NOT NULL,
  `url` varchar(200) NOT NULL,
  `image` varchar(100) NOT NULL,
  `index` smallint(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `df_index_promotion`
--

LOCK TABLES `df_index_promotion` WRITE;
/*!40000 ALTER TABLE `df_index_promotion` DISABLE KEYS */;
INSERT INTO `df_index_promotion` VALUES (1,'2017-10-16 02:57:52.707965','2017-10-16 06:16:43.461496','吃货暑假趴','http://www.itcast.cn','group1/M00/00/00/CtM3BVnkIDGATx4aAAA2pLUeB600278858',1),(2,'2017-10-16 02:58:21.916410','2017-10-16 06:16:32.600365','盛夏尝鲜季','http://www.itheima.com','group1/M00/00/00/CtM3BVnkIE6AA2o8AAA98yvCs1I9520126',0);
/*!40000 ALTER TABLE `df_index_promotion` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-10-22  6:32:47
