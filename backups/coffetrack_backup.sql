CREATE DATABASE  IF NOT EXISTS `coffeetrack` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `coffeetrack`;
-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: localhost    Database: coffeetrack
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
-- Table structure for table `alertas_inventario`
--

DROP TABLE IF EXISTS `alertas_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alertas_inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia_prima_id` int DEFAULT NULL,
  `bebida_id` int DEFAULT NULL,
  `tipo_alerta` enum('stock_bajo_materia','stock_bajo_bebida','materia_agotada','bebida_agotada') NOT NULL,
  `mensaje` text NOT NULL,
  `activa` tinyint(1) DEFAULT '1',
  `fecha_alerta` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_resolucion` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `materia_prima_id` (`materia_prima_id`),
  KEY `bebida_id` (`bebida_id`),
  KEY `idx_activa` (`activa`),
  KEY `idx_fecha` (`fecha_alerta`),
  CONSTRAINT `alertas_inventario_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `alertas_inventario_ibfk_2` FOREIGN KEY (`bebida_id`) REFERENCES `bebidas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertas_inventario`
--

LOCK TABLES `alertas_inventario` WRITE;
/*!40000 ALTER TABLE `alertas_inventario` DISABLE KEYS */;
INSERT INTO `alertas_inventario` VALUES (1,NULL,1,'bebida_agotada','La bebida \"Café Mocha con Chocolate Blanco\" está agotada',1,'2026-04-14 01:03:10',NULL),(2,NULL,2,'bebida_agotada','La bebida \"Café de Caramelo\" está agotada',1,'2026-04-14 01:03:31',NULL),(3,NULL,3,'bebida_agotada','La bebida \"Café de Coco\" está agotada',1,'2026-04-14 01:03:50',NULL),(4,NULL,4,'bebida_agotada','La bebida \"Café con Leche de Almendra\" está agotada',1,'2026-04-14 01:04:16',NULL),(5,NULL,5,'bebida_agotada','La bebida \"Café Clásico\" está agotada',1,'2026-04-14 01:04:40',NULL),(6,NULL,6,'bebida_agotada','La bebida \"Café Americano\" está agotada',1,'2026-04-14 01:05:00',NULL),(7,NULL,7,'bebida_agotada','La bebida \"Café Moka\" está agotada',1,'2026-04-14 01:05:14',NULL),(8,NULL,8,'bebida_agotada','La bebida \"Café de Olla\" está agotada',1,'2026-04-14 01:05:35',NULL),(9,NULL,9,'bebida_agotada','La bebida \"Café de Vainilla\" está agotada',1,'2026-04-14 01:05:44',NULL),(10,NULL,10,'bebida_agotada','La bebida \"Café Latte\" está agotada',1,'2026-04-14 01:06:04',NULL),(11,NULL,11,'bebida_agotada','La bebida \"Frappe Moka\" está agotada',1,'2026-04-14 01:06:24',NULL),(12,NULL,12,'bebida_agotada','La bebida \"Frappe Oreo\" está agotada',1,'2026-04-14 01:06:48',NULL);
/*!40000 ALTER TABLE `alertas_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `bebidas`
--

DROP TABLE IF EXISTS `bebidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `bebidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `categoria_id` int NOT NULL,
  `volumen_ml` int NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `imagen_url` varchar(255) DEFAULT NULL,
  `disponible` tinyint(1) DEFAULT '1',
  `stock_actual` int DEFAULT '0',
  `stock_minimo` int DEFAULT '5',
  `activo` tinyint(1) DEFAULT '1',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `solo_caliente` tinyint(1) DEFAULT '0',
  `imagen_url_frio` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_nombre` (`nombre`),
  KEY `idx_categoria` (`categoria_id`),
  KEY `idx_disponible` (`disponible`),
  CONSTRAINT `bebidas_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categoria_bebidas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bebidas`
--

LOCK TABLES `bebidas` WRITE;
/*!40000 ALTER TABLE `bebidas` DISABLE KEYS */;
INSERT INTO `bebidas` VALUES (1,'Café Mocha con Chocolate Blanco','Delicioso café con chocolate blanco y espresso',1,355,65.00,'c54262a1f7ce4550b99462c49a9c9fba.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-15 23:32:27',0,'b8361610805b4ab181ba763faba6d165.png'),(2,'Café de Caramelo','Café espresso con jarabe de caramelo',1,355,60.00,'e63eba70daa34319bf75b3ad283212bd.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-16 00:32:52',0,'45dd03e8c3b74393a8c223c7ea137e1e.png'),(3,'Café de Coco','Café con leche de coco y jarabe de coco',1,355,65.00,'d1cd6db524664d1b9ce1371738b4b552.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-14 01:23:49',0,'381d7b66a60f49019f6f809ce21aee9c.png'),(4,'Café con Leche de Almendra','Café espresso con leche de almendra',3,355,60.00,'666124e5a7b1441992512960619fa6ce.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-15 23:32:25',0,'2cf795a793344159a53ca70ad05ed186.png'),(5,'Café Clásico','Café tradicional con leche y azúcar',2,355,45.00,'f67409b0b2b44cf68b2dd48f60cc5dc3.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-14 07:04:50',0,'af51c560cd64461094b5a6e61729bd12.png'),(6,'Café Americano','Espresso con agua caliente',2,355,40.00,'b62ba8fe48e3480b912d8b816bf976ea.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-14 02:01:42',1,NULL),(7,'Café Moka','Café con chocolate y leche',1,355,60.00,'5ebcf4d677a5456185e3a8dc3a80a855.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-16 03:24:13',0,'ccf0cb14eea046f98f1d15058e7bcddc.png'),(8,'Café de Olla','Café tradicional mexicano con piloncillo',2,355,50.00,'6f8349d9f6ac4a699ae5dfd94ee1cfac.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-14 07:05:35',1,NULL),(9,'Café de Vainilla','Café con jarabe de vainilla',1,355,55.00,'b82a6c796bd745b29ee3a4257f89cde3.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-15 22:52:38',0,'86410d792a124b479dbaa413f8f9b2f5.png'),(10,'Café Latte','Espresso con leche vaporizada',3,355,55.00,'5113216da7ed4fbe841c74098f711b1f.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-16 03:26:42',0,'9d6af588a7834412ab3e282e9a511102.png'),(11,'Frappe Moka','Frappé de Moka especialidad con hielo',4,355,65.00,'b3366b0767e54fd495786c09a7de20c1.png',1,1,5,1,'2026-04-14 00:51:00','2026-04-15 23:32:27',0,'a9c6ffd10e04483b936166baddd736ea.png'),(12,'Frappe Oreo','Frappé de Oreo especialidad con hielo',4,355,65.00,'52e2d81f96d04373b0236c8442dbb18a.png',1,0,5,1,'2026-04-14 00:51:00','2026-04-16 10:05:18',0,NULL),(13,'Chocofresa con Vainilla','',1,355,45.00,'b215694aac804759a5acde276ec02539.png',0,5,5,0,'2026-04-15 11:33:53','2026-04-15 11:37:53',0,'cc5c9f40bf304c1486ad5f2f9aecb64f.png');
/*!40000 ALTER TABLE `bebidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categoria_bebidas`
--

DROP TABLE IF EXISTS `categoria_bebidas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria_bebidas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `solo_frio` tinyint(1) DEFAULT '0',
  `sin_temperatura` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria_bebidas`
--

LOCK TABLES `categoria_bebidas` WRITE;
/*!40000 ALTER TABLE `categoria_bebidas` DISABLE KEYS */;
INSERT INTO `categoria_bebidas` VALUES (1,'Cafés Especiales','Bebidas de café con sabores únicos','2026-04-14 00:51:00',0,0),(2,'Cafés Clasicos','Bebidas de café tradicionales','2026-04-14 00:51:00',0,0),(3,'Cafés con Leche','Bebidas de café con diferentes tipos de leche','2026-04-14 00:51:00',0,0),(4,'Frappes','Bebidas frías especiales','2026-04-14 00:51:00',1,0);
/*!40000 ALTER TABLE `categoria_bebidas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias_materia_prima`
--

DROP TABLE IF EXISTS `categorias_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias_materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(150) NOT NULL,
  `descripcion` text,
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias_materia_prima`
--

LOCK TABLES `categorias_materia_prima` WRITE;
/*!40000 ALTER TABLE `categorias_materia_prima` DISABLE KEYS */;
INSERT INTO `categorias_materia_prima` VALUES (1,'Café','Tipos de café granos o molido','2026-04-14 00:51:00'),(2,'Lácteos','Leche y derivados','2026-04-14 00:51:00'),(3,'Endulzantes','Azúcar y jarabes','2026-04-14 00:51:00'),(4,'Saborizantes','Chocolates, vainilla y otros sabores','2026-04-14 00:51:00'),(5,'Otros','Hielo y otros insumos','2026-04-14 00:51:00');
/*!40000 ALTER TABLE `categorias_materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `codigos_verificacion`
--

DROP TABLE IF EXISTS `codigos_verificacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `codigos_verificacion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `codigo` varchar(6) NOT NULL,
  `expira_en` datetime NOT NULL,
  `usado` tinyint(1) DEFAULT NULL,
  `fecha_creacion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `codigos_verificacion_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos_verificacion`
--

LOCK TABLES `codigos_verificacion` WRITE;
/*!40000 ALTER TABLE `codigos_verificacion` DISABLE KEYS */;
INSERT INTO `codigos_verificacion` VALUES (2,10,'943109','2026-04-13 19:28:56',1,'2026-04-14 01:18:59'),(3,11,'267233','2026-04-13 19:46:29',1,'2026-04-14 01:36:33'),(4,12,'234914','2026-04-13 19:58:48',1,'2026-04-14 01:48:55'),(5,13,'611896','2026-04-15 16:53:36',1,'2026-04-15 22:43:40'),(6,14,'055564','2026-04-15 17:30:44',1,'2026-04-15 23:20:47'),(7,15,'758753','2026-04-15 17:33:02',1,'2026-04-15 23:23:05'),(8,16,'770611','2026-04-15 17:35:10',1,'2026-04-15 23:25:14'),(9,17,'904963','2026-04-15 18:36:30',1,'2026-04-16 00:26:35');
/*!40000 ALTER TABLE `codigos_verificacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `compras_materia_prima`
--

DROP TABLE IF EXISTS `compras_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compras_materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `proveedor_id` int NOT NULL,
  `fecha_compra` date NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','recibida','cancelada') DEFAULT 'pendiente',
  `notas` text,
  `usuario_registro_id` int NOT NULL,
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_registro_id` (`usuario_registro_id`),
  KEY `idx_fecha` (`fecha_compra`),
  KEY `idx_proveedor` (`proveedor_id`),
  CONSTRAINT `compras_materia_prima_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedores` (`id`),
  CONSTRAINT `compras_materia_prima_ibfk_2` FOREIGN KEY (`usuario_registro_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compras_materia_prima`
--

LOCK TABLES `compras_materia_prima` WRITE;
/*!40000 ALTER TABLE `compras_materia_prima` DISABLE KEYS */;
/*!40000 ALTER TABLE `compras_materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedidos`
--

DROP TABLE IF EXISTS `detalle_pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `bebida_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `temperatura` enum('caliente','frio') DEFAULT 'caliente',
  PRIMARY KEY (`id`),
  KEY `idx_pedido` (`pedido_id`),
  KEY `idx_bebida` (`bebida_id`),
  CONSTRAINT `detalle_pedidos_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`) ON DELETE CASCADE,
  CONSTRAINT `detalle_pedidos_ibfk_2` FOREIGN KEY (`bebida_id`) REFERENCES `bebidas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedidos`
--

LOCK TABLES `detalle_pedidos` WRITE;
/*!40000 ALTER TABLE `detalle_pedidos` DISABLE KEYS */;
INSERT INTO `detalle_pedidos` VALUES (1,1,1,2,65.00,130.00,'frio'),(2,1,3,1,65.00,65.00,'caliente'),(3,2,1,1,65.00,65.00,'caliente'),(4,2,10,1,55.00,55.00,'caliente'),(5,2,6,2,40.00,80.00,'caliente'),(6,3,11,1,65.00,65.00,'frio'),(7,3,12,2,65.00,130.00,'frio'),(8,4,11,1,65.00,65.00,'frio'),(9,5,11,1,65.00,65.00,'frio'),(10,5,12,3,65.00,195.00,'frio'),(11,5,9,1,55.00,55.00,'frio'),(12,6,11,3,65.00,195.00,'frio'),(13,7,1,2,65.00,130.00,'frio'),(14,7,11,1,65.00,65.00,'frio'),(15,7,12,1,65.00,65.00,'frio'),(16,8,11,2,65.00,130.00,'frio'),(17,9,4,1,60.00,60.00,'frio'),(18,9,7,1,60.00,60.00,'frio'),(19,10,2,1,60.00,60.00,'caliente'),(20,11,7,2,60.00,120.00,'caliente'),(21,12,10,2,55.00,110.00,'caliente');
/*!40000 ALTER TABLE `detalle_pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalles_compras_materia_prima`
--

DROP TABLE IF EXISTS `detalles_compras_materia_prima`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalles_compras_materia_prima` (
  `id` int NOT NULL AUTO_INCREMENT,
  `compras_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_compra` (`compras_id`),
  KEY `idx_materia_prima` (`materia_prima_id`),
  CONSTRAINT `detalles_compras_materia_prima_ibfk_1` FOREIGN KEY (`compras_id`) REFERENCES `compras_materia_prima` (`id`) ON DELETE CASCADE,
  CONSTRAINT `detalles_compras_materia_prima_ibfk_2` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalles_compras_materia_prima`
--

LOCK TABLES `detalles_compras_materia_prima` WRITE;
/*!40000 ALTER TABLE `detalles_compras_materia_prima` DISABLE KEYS */;
/*!40000 ALTER TABLE `detalles_compras_materia_prima` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_inventario`
--

DROP TABLE IF EXISTS `historial_inventario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_inventario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `materia_prima_id` int NOT NULL,
  `tipo_movimiento` enum('entrada','salida','ajuste') NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `stock_anterior` decimal(10,2) NOT NULL,
  `stock_nuevo` decimal(10,2) NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `motivo` text,
  `usuario_id` int NOT NULL,
  `fecha_movimiento` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  KEY `idx_materia_prima_id` (`materia_prima_id`),
  KEY `idx_fecha` (`fecha_movimiento`),
  KEY `idx_tipo` (`tipo_movimiento`),
  CONSTRAINT `historial_inventario_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `historial_inventario_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_inventario`
--

LOCK TABLES `historial_inventario` WRITE;
/*!40000 ALTER TABLE `historial_inventario` DISABLE KEYS */;
INSERT INTO `historial_inventario` VALUES (1,1,'salida',60.00,10000.00,9940.00,'PRODUCCION-2','Produccion de 1 unidades',1,'2026-04-14 01:23:49'),(2,5,'salida',240.00,20000.00,19760.00,'PRODUCCION-2','Produccion de 1 unidades',1,'2026-04-14 01:23:49'),(3,10,'salida',25.00,20000.00,19975.00,'PRODUCCION-2','Produccion de 1 unidades',1,'2026-04-14 01:23:49'),(4,14,'salida',30.00,5000.00,4970.00,'PRODUCCION-2','Produccion de 1 unidades',1,'2026-04-14 01:23:49'),(5,1,'salida',120.00,9940.00,9820.00,'PRODUCCION-1','Produccion de 2 unidades',1,'2026-04-14 01:24:47'),(6,3,'salida',480.00,20000.00,19520.00,'PRODUCCION-1','Produccion de 2 unidades',1,'2026-04-14 01:24:47'),(7,6,'salida',30.00,20000.00,19970.00,'PRODUCCION-1','Produccion de 2 unidades',1,'2026-04-14 01:24:47'),(8,7,'salida',60.00,20000.00,19940.00,'PRODUCCION-1','Produccion de 2 unidades',1,'2026-04-14 01:24:47'),(9,9,'salida',40.00,30000.00,29960.00,'PRODUCCION-1','Produccion de 2 unidades',1,'2026-04-14 01:24:47'),(10,13,'salida',70.00,10000.00,9930.00,'PRODUCCION-1','Produccion de 2 unidades',1,'2026-04-14 01:24:47'),(11,14,'salida',200.00,4970.00,4770.00,'PRODUCCION-1','Hielo para 2 unidades frias',1,'2026-04-14 01:24:47'),(12,1,'salida',60.00,9820.00,9760.00,'PRODUCCION-3','Produccion de 1 unidades',1,'2026-04-14 01:57:12'),(13,3,'salida',240.00,19520.00,19280.00,'PRODUCCION-3','Produccion de 1 unidades',1,'2026-04-14 01:57:12'),(14,6,'salida',15.00,19970.00,19955.00,'PRODUCCION-3','Produccion de 1 unidades',1,'2026-04-14 01:57:12'),(15,7,'salida',30.00,19940.00,19910.00,'PRODUCCION-3','Produccion de 1 unidades',1,'2026-04-14 01:57:12'),(16,9,'salida',20.00,29960.00,29940.00,'PRODUCCION-3','Produccion de 1 unidades',1,'2026-04-14 01:57:12'),(17,13,'salida',35.00,9930.00,9895.00,'PRODUCCION-3','Produccion de 1 unidades',1,'2026-04-14 01:57:12'),(18,1,'salida',60.00,9760.00,9700.00,'PRODUCCION-4','Produccion de 1 unidades',1,'2026-04-14 01:57:13'),(19,3,'salida',15.00,19280.00,19265.00,'PRODUCCION-4','Produccion de 1 unidades',1,'2026-04-14 01:57:13'),(20,6,'salida',280.00,19955.00,19675.00,'PRODUCCION-4','Produccion de 1 unidades',1,'2026-04-14 01:57:13'),(21,1,'salida',120.00,9700.00,9580.00,'PRODUCCION-5','Produccion de 2 unidades',1,'2026-04-14 02:01:42'),(22,12,'salida',30.00,10000.00,9970.00,'PRODUCCION-5','Produccion de 2 unidades',1,'2026-04-14 02:01:42'),(23,13,'salida',590.00,9895.00,9305.00,'PRODUCCION-5','Produccion de 2 unidades',1,'2026-04-14 02:01:42'),(24,1,'salida',25.00,9580.00,9555.00,'PRODUCCION-6','Produccion de 1 unidades',1,'2026-04-14 02:01:44'),(25,3,'salida',60.00,19265.00,19205.00,'PRODUCCION-6','Produccion de 1 unidades',1,'2026-04-14 02:01:44'),(26,8,'salida',25.00,30000.00,29975.00,'PRODUCCION-6','Produccion de 1 unidades',1,'2026-04-14 02:01:44'),(27,12,'salida',15.00,9970.00,9955.00,'PRODUCCION-6','Produccion de 1 unidades',1,'2026-04-14 02:01:44'),(28,14,'salida',150.00,4770.00,4620.00,'PRODUCCION-6','Produccion de 1 unidades',1,'2026-04-14 02:01:44'),(29,14,'salida',100.00,4620.00,4520.00,'PRODUCCION-6','Hielo para 1 unidades frias',1,'2026-04-14 02:01:44'),(30,3,'salida',400.00,19205.00,18805.00,'PRODUCCION-7','Produccion de 2 unidades',1,'2026-04-14 02:07:30'),(31,6,'salida',40.00,19675.00,19635.00,'PRODUCCION-7','Produccion de 2 unidades',1,'2026-04-14 02:07:30'),(32,8,'salida',20.00,29975.00,29955.00,'PRODUCCION-7','Produccion de 2 unidades',1,'2026-04-14 02:07:30'),(33,12,'salida',40.00,9955.00,9915.00,'PRODUCCION-7','Produccion de 2 unidades',1,'2026-04-14 02:07:30'),(34,14,'salida',300.00,4520.00,4220.00,'PRODUCCION-7','Produccion de 2 unidades',1,'2026-04-14 02:07:30'),(35,17,'salida',100.00,20000.00,19900.00,'PRODUCCION-7','Produccion de 2 unidades',1,'2026-04-14 02:07:30'),(36,14,'salida',200.00,4220.00,4020.00,'PRODUCCION-7','Hielo para 2 unidades frias',1,'2026-04-14 02:07:30'),(37,1,'salida',25.00,9555.00,9530.00,'PRODUCCION-8','Produccion de 1 unidades',1,'2026-04-14 03:08:40'),(38,3,'salida',60.00,18805.00,18745.00,'PRODUCCION-8','Produccion de 1 unidades',1,'2026-04-14 03:08:40'),(39,8,'salida',25.00,29955.00,29930.00,'PRODUCCION-8','Produccion de 1 unidades',1,'2026-04-14 03:08:40'),(40,12,'salida',15.00,9915.00,9900.00,'PRODUCCION-8','Produccion de 1 unidades',1,'2026-04-14 03:08:40'),(41,14,'salida',150.00,4020.00,3870.00,'PRODUCCION-8','Produccion de 1 unidades',1,'2026-04-14 03:08:40'),(42,14,'salida',100.00,3870.00,3770.00,'PRODUCCION-8','Hielo para 1 unidades frias',1,'2026-04-14 03:08:40'),(43,1,'salida',75.00,9530.00,9455.00,'PRODUCCION-12','Produccion de 3 unidades',1,'2026-04-15 22:52:37'),(44,3,'salida',180.00,18745.00,18565.00,'PRODUCCION-12','Produccion de 3 unidades',1,'2026-04-15 22:52:37'),(45,8,'salida',75.00,29930.00,29855.00,'PRODUCCION-12','Produccion de 3 unidades',1,'2026-04-15 22:52:37'),(46,12,'salida',45.00,9900.00,9855.00,'PRODUCCION-12','Produccion de 3 unidades',1,'2026-04-15 22:52:37'),(47,14,'salida',450.00,3770.00,3320.00,'PRODUCCION-12','Produccion de 3 unidades',1,'2026-04-15 22:52:37'),(48,14,'salida',300.00,3320.00,3020.00,'PRODUCCION-12','Hielo para 3 unidades frias',1,'2026-04-15 22:52:37'),(49,1,'salida',60.00,9455.00,9395.00,'PRODUCCION-11','Produccion de 1 unidades',1,'2026-04-15 22:52:38'),(50,3,'salida',240.00,18565.00,18325.00,'PRODUCCION-11','Produccion de 1 unidades',1,'2026-04-15 22:52:38'),(51,11,'salida',25.00,20000.00,19975.00,'PRODUCCION-11','Produccion de 1 unidades',1,'2026-04-15 22:52:38'),(52,14,'salida',100.00,3020.00,2920.00,'PRODUCCION-11','Hielo para 1 unidades frias',1,'2026-04-15 22:52:38'),(53,1,'salida',25.00,9395.00,9370.00,'PRODUCCION-9','Produccion de 1 unidades',1,'2026-04-15 22:53:06'),(54,3,'salida',60.00,18325.00,18265.00,'PRODUCCION-9','Produccion de 1 unidades',1,'2026-04-15 22:53:06'),(55,8,'salida',25.00,29855.00,29830.00,'PRODUCCION-9','Produccion de 1 unidades',1,'2026-04-15 22:53:06'),(56,12,'salida',15.00,9855.00,9840.00,'PRODUCCION-9','Produccion de 1 unidades',1,'2026-04-15 22:53:06'),(57,14,'salida',150.00,2920.00,2770.00,'PRODUCCION-9','Produccion de 1 unidades',1,'2026-04-15 22:53:06'),(58,14,'salida',100.00,2770.00,2670.00,'PRODUCCION-9','Hielo para 1 unidades frias',1,'2026-04-15 22:53:06'),(59,3,'salida',600.00,18265.00,17665.00,'PRODUCCION-10','Produccion de 3 unidades',1,'2026-04-15 22:53:07'),(60,6,'salida',60.00,19635.00,19575.00,'PRODUCCION-10','Produccion de 3 unidades',1,'2026-04-15 22:53:07'),(61,8,'salida',30.00,29830.00,29800.00,'PRODUCCION-10','Produccion de 3 unidades',1,'2026-04-15 22:53:07'),(62,12,'salida',60.00,9840.00,9780.00,'PRODUCCION-10','Produccion de 3 unidades',1,'2026-04-15 22:53:07'),(63,14,'salida',450.00,2670.00,2220.00,'PRODUCCION-10','Produccion de 3 unidades',1,'2026-04-15 22:53:07'),(64,17,'salida',150.00,19900.00,19750.00,'PRODUCCION-10','Produccion de 3 unidades',1,'2026-04-15 22:53:07'),(65,14,'salida',300.00,2220.00,1920.00,'PRODUCCION-10','Hielo para 3 unidades frias',1,'2026-04-15 22:53:07'),(66,1,'salida',60.00,9370.00,9310.00,'PRODUCCION-18','Produccion de 1 unidades',1,'2026-04-15 23:32:24'),(67,3,'salida',230.00,17665.00,17435.00,'PRODUCCION-18','Produccion de 1 unidades',1,'2026-04-15 23:32:24'),(68,8,'salida',35.00,29800.00,29765.00,'PRODUCCION-18','Produccion de 1 unidades',1,'2026-04-15 23:32:24'),(69,14,'salida',100.00,1920.00,1820.00,'PRODUCCION-18','Hielo para 1 unidades frias',1,'2026-04-15 23:32:24'),(70,1,'salida',60.00,9310.00,9250.00,'PRODUCCION-17','Produccion de 1 unidades',1,'2026-04-15 23:32:25'),(71,4,'salida',260.00,20000.00,19740.00,'PRODUCCION-17','Produccion de 1 unidades',1,'2026-04-15 23:32:25'),(72,12,'salida',15.00,9780.00,9765.00,'PRODUCCION-17','Produccion de 1 unidades',1,'2026-04-15 23:32:25'),(73,14,'salida',100.00,1820.00,1720.00,'PRODUCCION-17','Hielo para 1 unidades frias',1,'2026-04-15 23:32:25'),(74,1,'salida',50.00,9250.00,9200.00,'PRODUCCION-16','Produccion de 2 unidades',1,'2026-04-15 23:32:26'),(75,3,'salida',120.00,17435.00,17315.00,'PRODUCCION-16','Produccion de 2 unidades',1,'2026-04-15 23:32:26'),(76,8,'salida',50.00,29765.00,29715.00,'PRODUCCION-16','Produccion de 2 unidades',1,'2026-04-15 23:32:26'),(77,12,'salida',30.00,9765.00,9735.00,'PRODUCCION-16','Produccion de 2 unidades',1,'2026-04-15 23:32:26'),(78,14,'salida',300.00,1720.00,1420.00,'PRODUCCION-16','Produccion de 2 unidades',1,'2026-04-15 23:32:26'),(79,14,'salida',200.00,1420.00,1220.00,'PRODUCCION-16','Hielo para 2 unidades frias',1,'2026-04-15 23:32:26'),(80,3,'salida',200.00,17315.00,17115.00,'PRODUCCION-15','Produccion de 1 unidades',1,'2026-04-15 23:32:26'),(81,6,'salida',20.00,19575.00,19555.00,'PRODUCCION-15','Produccion de 1 unidades',1,'2026-04-15 23:32:26'),(82,8,'salida',10.00,29715.00,29705.00,'PRODUCCION-15','Produccion de 1 unidades',1,'2026-04-15 23:32:26'),(83,12,'salida',20.00,9735.00,9715.00,'PRODUCCION-15','Produccion de 1 unidades',1,'2026-04-15 23:32:26'),(84,14,'salida',150.00,1220.00,1070.00,'PRODUCCION-15','Produccion de 1 unidades',1,'2026-04-15 23:32:26'),(85,17,'salida',50.00,19750.00,19700.00,'PRODUCCION-15','Produccion de 1 unidades',1,'2026-04-15 23:32:26'),(86,14,'salida',100.00,1070.00,970.00,'PRODUCCION-15','Hielo para 1 unidades frias',1,'2026-04-15 23:32:26'),(87,1,'salida',25.00,9200.00,9175.00,'PRODUCCION-14','Produccion de 1 unidades',1,'2026-04-15 23:32:27'),(88,3,'salida',60.00,17115.00,17055.00,'PRODUCCION-14','Produccion de 1 unidades',1,'2026-04-15 23:32:27'),(89,8,'salida',25.00,29705.00,29680.00,'PRODUCCION-14','Produccion de 1 unidades',1,'2026-04-15 23:32:27'),(90,12,'salida',15.00,9715.00,9700.00,'PRODUCCION-14','Produccion de 1 unidades',1,'2026-04-15 23:32:27'),(91,14,'salida',150.00,970.00,820.00,'PRODUCCION-14','Produccion de 1 unidades',1,'2026-04-15 23:32:27'),(92,14,'salida',100.00,820.00,720.00,'PRODUCCION-14','Hielo para 1 unidades frias',1,'2026-04-15 23:32:27'),(93,1,'salida',120.00,9175.00,9055.00,'PRODUCCION-13','Produccion de 2 unidades',1,'2026-04-15 23:32:27'),(94,3,'salida',480.00,17055.00,16575.00,'PRODUCCION-13','Produccion de 2 unidades',1,'2026-04-15 23:32:27'),(95,6,'salida',30.00,19555.00,19525.00,'PRODUCCION-13','Produccion de 2 unidades',1,'2026-04-15 23:32:27'),(96,7,'salida',60.00,19910.00,19850.00,'PRODUCCION-13','Produccion de 2 unidades',1,'2026-04-15 23:32:27'),(97,9,'salida',40.00,29940.00,29900.00,'PRODUCCION-13','Produccion de 2 unidades',1,'2026-04-15 23:32:27'),(98,13,'salida',70.00,9305.00,9235.00,'PRODUCCION-13','Produccion de 2 unidades',1,'2026-04-15 23:32:27'),(99,14,'salida',200.00,720.00,520.00,'PRODUCCION-13','Hielo para 2 unidades frias',1,'2026-04-15 23:32:27'),(100,1,'salida',60.00,9055.00,8995.00,'PRODUCCION-19','Produccion de 1 unidades',1,'2026-04-16 00:32:52'),(101,3,'salida',230.00,16575.00,16345.00,'PRODUCCION-19','Produccion de 1 unidades',1,'2026-04-16 00:32:52'),(102,9,'salida',30.00,29900.00,29870.00,'PRODUCCION-19','Produccion de 1 unidades',1,'2026-04-16 00:32:52'),(103,1,'salida',120.00,8995.00,8875.00,'PRODUCCION-20','Produccion de 2 unidades',1,'2026-04-16 03:24:13'),(104,3,'salida',460.00,16345.00,15885.00,'PRODUCCION-20','Produccion de 2 unidades',1,'2026-04-16 03:24:13'),(105,8,'salida',70.00,29680.00,29610.00,'PRODUCCION-20','Produccion de 2 unidades',1,'2026-04-16 03:24:13'),(106,1,'salida',120.00,8875.00,8755.00,'PRODUCCION-21','Produccion de 2 unidades',1,'2026-04-16 03:26:42'),(107,3,'salida',30.00,15885.00,15855.00,'PRODUCCION-21','Produccion de 2 unidades',1,'2026-04-16 03:26:42'),(108,6,'salida',560.00,19525.00,18965.00,'PRODUCCION-21','Produccion de 2 unidades',1,'2026-04-16 03:26:42');
/*!40000 ALTER TABLE `historial_inventario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `materias_primas`
--

DROP TABLE IF EXISTS `materias_primas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `materias_primas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `categoria_id` int NOT NULL,
  `unidad_medida` varchar(20) NOT NULL,
  `stock_actual` decimal(10,2) DEFAULT '0.00',
  `stock_minimo` decimal(10,2) DEFAULT '0.00',
  `precio_unitario` decimal(10,3) DEFAULT '0.000',
  `activo` tinyint(1) DEFAULT '1',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_nombre` (`nombre`),
  KEY `idx_categoria` (`categoria_id`),
  CONSTRAINT `materias_primas_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias_materia_prima` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (1,'Espresso',1,'ml',8755.00,1000.00,0.080,1,'2026-04-14 00:51:00','2026-04-16 03:26:42'),(2,'Café molido',1,'gr',10000.00,1000.00,0.120,1,'2026-04-14 00:51:00','2026-04-14 00:51:00'),(3,'Leche',2,'ml',15855.00,2000.00,0.022,1,'2026-04-14 00:51:00','2026-04-16 03:26:42'),(4,'Leche de almendra',2,'ml',19740.00,2000.00,0.040,1,'2026-04-14 00:51:00','2026-04-15 23:32:25'),(5,'Leche de coco',2,'ml',19760.00,2000.00,0.038,1,'2026-04-14 00:51:00','2026-04-14 01:23:49'),(6,'Leche vaporizada',2,'ml',18965.00,2000.00,0.022,1,'2026-04-14 00:51:00','2026-04-16 03:26:42'),(7,'Chocolate blanco',4,'ml',19850.00,3000.00,0.120,1,'2026-04-14 00:51:00','2026-04-15 23:32:27'),(8,'Chocolate',4,'ml',29610.00,3000.00,0.100,1,'2026-04-14 00:51:00','2026-04-16 03:24:13'),(9,'Jarabe de caramelo',4,'ml',29870.00,3000.00,0.080,1,'2026-04-14 00:51:00','2026-04-16 00:32:52'),(10,'Jarabe de coco',4,'ml',19975.00,2000.00,0.075,1,'2026-04-14 00:51:00','2026-04-14 01:23:49'),(11,'Jarabe de vainilla',4,'ml',19975.00,2000.00,0.080,1,'2026-04-14 00:51:00','2026-04-15 22:52:38'),(12,'Azúcar',3,'gr',9700.00,1000.00,0.022,1,'2026-04-14 00:51:00','2026-04-15 23:32:27'),(13,'Agua',5,'ml',9235.00,1000.00,0.010,1,'2026-04-14 00:51:00','2026-04-15 23:32:27'),(14,'Hielo',5,'gr',520.00,500.00,0.015,1,'2026-04-14 00:51:00','2026-04-15 23:32:27'),(15,'Piloncillo',3,'ml',2000.00,200.00,0.045,1,'2026-04-14 00:51:00','2026-04-14 00:51:00'),(16,'Harina',5,'gr',10000.00,500.00,0.020,1,'2026-04-14 00:51:00','2026-04-14 00:51:00'),(17,'Galletas Oreo(bolsa de kilo)',5,'gr',19700.00,3000.00,0.050,1,'2026-04-14 07:58:35','2026-04-15 23:32:26'),(18,'Fresas',5,'gr',10000.00,5000.00,0.040,0,'2026-04-14 08:25:33','2026-04-15 11:36:30');
/*!40000 ALTER TABLE `materias_primas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `fecha_pedido` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `subtotal` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT '0.00',
  `total` decimal(10,2) NOT NULL,
  `estado` enum('pendiente','confirmado','en_preparacion','enviado','entregado','cancelado') DEFAULT 'pendiente',
  `direccion_entrega` text NOT NULL,
  `telefono_contacto` varchar(15) NOT NULL,
  `notas` text,
  `fecha_entrega_estimada` date DEFAULT NULL,
  `fecha_entrega_real` date DEFAULT NULL,
  `costo_envio` decimal(10,2) DEFAULT '0.00',
  `hora_estimada_entrega` varchar(10) DEFAULT NULL,
  `dia_entrega` date DEFAULT NULL,
  `metodo_pago_cliente` varchar(20) DEFAULT 'efectivo',
  PRIMARY KEY (`id`),
  KEY `idx_usuario` (`usuario_id`),
  KEY `idx_fecha` (`fecha_pedido`),
  KEY `idx_estado` (`estado`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,10,'2026-04-14 07:21:40',195.00,0.00,225.00,'entregado','Eucaliptos 304 col los pinos','4771252950',' | PAGADO | REF: CT-20260413-001',NULL,NULL,30.00,'19:46','2026-04-13','efectivo'),(2,11,'2026-04-14 07:39:39',200.00,0.00,200.00,'entregado','Recoger en sucursal','N/A',' | PAGADO | REF: CT-20260413-002',NULL,NULL,0.00,'20:04','2026-04-13','efectivo'),(3,12,'2026-04-14 07:51:58',195.00,0.00,225.00,'entregado','C.Independencia 1335, col.San Miguel','4776893554',' | PAGADO | REF: CT-20260413-003',NULL,NULL,30.00,'20:16','2026-04-13','efectivo'),(4,11,'2026-04-14 09:09:58',65.00,0.00,95.00,'entregado','Benito Alcaceres #218 col. San Sebastian ','4771252950',' | PAGADO | REF: CT-20260413-004',NULL,NULL,30.00,'21:22','2026-04-13','efectivo'),(5,13,'2026-04-16 04:45:46',315.00,0.00,315.00,'entregado','Recoger en sucursal','4771252950',' | PAGADO | REF: CT-20260415-005',NULL,NULL,0.00,'17:10','2026-04-15','efectivo'),(6,10,'2026-04-16 04:50:36',195.00,0.00,225.00,'entregado','Eucaliptos 304 col los pinos','4792258975',' | PAGADO | REF: CT-20260415-006',NULL,NULL,30.00,'17:15','2026-04-15','efectivo'),(7,14,'2026-04-16 05:27:44',260.00,0.00,290.00,'entregado','Acacias #208 col. Los Pinos','4776700093',' | PAGADO | REF: CT-20260415-007',NULL,NULL,30.00,'17:52','2026-04-15','efectivo'),(8,16,'2026-04-16 05:28:37',130.00,0.00,130.00,'entregado','Recoger en sucursal','4793622178',' | PAGADO | REF: CT-20260415-008',NULL,NULL,0.00,'17:53','2026-04-15','efectivo'),(9,15,'2026-04-16 05:29:50',120.00,0.00,120.00,'entregado','Recoger en sucursal','4775214769',' | PAGADO | REF: CT-20260415-009',NULL,NULL,0.00,'17:54','2026-04-15','efectivo'),(10,17,'2026-04-16 06:28:59',60.00,0.00,90.00,'entregado','Los Angeles #112 col. Las Americas','477 200 3710',' | PAGADO | REF: CT-20260415-010',NULL,NULL,30.00,'18:53','2026-04-15','efectivo'),(11,10,'2026-04-16 09:05:37',120.00,0.00,120.00,'entregado','Recoger en sucursal','4776893552',' | PAGADO | REF: CT-20260415-011',NULL,NULL,0.00,'21:30','2026-04-15','efectivo'),(12,14,'2026-04-16 09:23:22',110.00,0.00,110.00,'entregado','Recoger en sucursal','4792258975',' | PAGADO | REF: CT-20260415-012',NULL,NULL,0.00,'07:25','2026-04-16','efectivo');
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccion`
--

DROP TABLE IF EXISTS `produccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bebida_id` int NOT NULL,
  `cantidad_producida` int NOT NULL,
  `fecha_produccion` date NOT NULL,
  `costo_produccion` decimal(10,2) DEFAULT NULL,
  `usuario_registrado_id` int NOT NULL,
  `notas` text,
  `estado` enum('planificada','en proceso','completada','cancelada') DEFAULT 'planificada',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `es_frio` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `usuario_registrado_id` (`usuario_registrado_id`),
  KEY `idx_fecha` (`fecha_produccion`),
  KEY `idx_bebida` (`bebida_id`),
  KEY `idx_estado` (`estado`),
  CONSTRAINT `produccion_ibfk_1` FOREIGN KEY (`bebida_id`) REFERENCES `bebidas` (`id`),
  CONSTRAINT `produccion_ibfk_2` FOREIGN KEY (`usuario_registrado_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion`
--

LOCK TABLES `produccion` WRITE;
/*!40000 ALTER TABLE `produccion` DISABLE KEYS */;
INSERT INTO `produccion` VALUES (1,1,2,'2026-04-13',34.92,1,'Generado automáticamente por Pedido #1','completada','2026-04-14 07:23:42',1),(2,3,1,'2026-04-13',16.24,1,'Generado automáticamente por Pedido #1','completada','2026-04-14 07:23:42',0),(3,1,1,'2026-04-13',15.96,1,'Generado automáticamente por Pedido #2','completada','2026-04-14 07:41:41',0),(4,10,1,'2026-04-13',11.29,1,'Generado automáticamente por Pedido #2','completada','2026-04-14 07:41:41',0),(5,6,2,'2026-04-13',16.16,1,'Generado automáticamente por Pedido #2','completada','2026-04-14 07:41:41',0),(6,11,1,'2026-04-13',9.90,1,'Generado automáticamente por Pedido #3','completada','2026-04-14 07:53:11',1),(7,12,2,'2026-04-13',20.06,1,'Generado automáticamente por Pedido #3','completada','2026-04-14 07:53:11',1),(8,11,1,'2026-04-14',9.90,1,'','completada','2026-04-14 08:58:33',1),(9,11,1,'2026-04-15',9.90,1,'Generado automáticamente por Pedido #5','completada','2026-04-16 04:49:21',1),(10,12,3,'2026-04-15',37.59,1,'Generado automáticamente por Pedido #5','completada','2026-04-16 04:49:21',1),(11,9,1,'2026-04-15',13.58,1,'Generado automáticamente por Pedido #5','completada','2026-04-16 04:49:21',1),(12,11,3,'2026-04-15',29.70,1,'Generado automáticamente por Pedido #6','completada','2026-04-16 04:52:24',1),(13,1,2,'2026-04-15',34.92,1,'Generado automáticamente por Pedido #7','completada','2026-04-16 05:30:59',1),(14,11,1,'2026-04-15',9.90,1,'Generado automáticamente por Pedido #7','completada','2026-04-16 05:30:59',1),(15,12,1,'2026-04-15',12.53,1,'Generado automáticamente por Pedido #7','completada','2026-04-16 05:30:59',1),(16,11,2,'2026-04-15',19.80,1,'Generado automáticamente por Pedido #8','completada','2026-04-16 05:31:04',1),(17,4,1,'2026-04-15',17.03,1,'Generado automáticamente por Pedido #9','completada','2026-04-16 05:31:07',1),(18,7,1,'2026-04-15',14.86,1,'Generado automáticamente por Pedido #9','completada','2026-04-16 05:31:07',1),(19,2,1,'2026-04-15',12.26,1,'Generado automáticamente por Pedido #10','completada','2026-04-16 06:31:46',0),(20,7,2,'2026-04-15',26.72,1,'Generado automáticamente por Pedido #11','completada','2026-04-16 09:24:03',0),(21,10,2,'2026-04-15',22.58,1,'Generado automáticamente por Pedido #12','completada','2026-04-16 09:25:31',0);
/*!40000 ALTER TABLE `produccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre_empresa` varchar(150) NOT NULL,
  `contacto_nombre` varchar(100) DEFAULT NULL,
  `contacto_telefono` varchar(50) DEFAULT NULL,
  `contacto_email` varchar(100) DEFAULT NULL,
  `direccion` text,
  `rfc` varchar(50) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_nombre` (`nombre_empresa`),
  KEY `idx_rfc` (`rfc`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
/*!40000 ALTER TABLE `proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `recetas`
--

DROP TABLE IF EXISTS `recetas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `recetas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `bebida_id` int NOT NULL,
  `materia_prima_id` int NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `unidad_medida` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_receta` (`bebida_id`,`materia_prima_id`),
  KEY `idx_bebida` (`bebida_id`),
  KEY `idx_materia_prima` (`materia_prima_id`),
  CONSTRAINT `recetas_ibfk_1` FOREIGN KEY (`bebida_id`) REFERENCES `bebidas` (`id`) ON DELETE CASCADE,
  CONSTRAINT `recetas_ibfk_2` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,'Café Mocha con Chocolate Blanco',1,1,60.00,'ml'),(2,'Café Mocha con Chocolate Blanco',1,7,30.00,'ml'),(3,'Café Mocha con Chocolate Blanco',1,9,20.00,'ml'),(4,'Café Mocha con Chocolate Blanco',1,6,15.00,'ml'),(5,'Café Mocha con Chocolate Blanco',1,13,35.00,'ml'),(6,'Café Mocha con Chocolate Blanco',1,3,240.00,'ml'),(7,'Café de Caramelo',2,1,60.00,'ml'),(8,'Café de Caramelo',2,3,230.00,'ml'),(9,'Café de Caramelo',2,9,30.00,'ml'),(11,'Café de Coco',3,1,60.00,'ml'),(12,'Café de Coco',3,5,240.00,'ml'),(13,'Café de Coco',3,10,25.00,'ml'),(15,'Café con Leche de Almendra',4,1,60.00,'ml'),(16,'Café con Leche de Almendra',4,4,260.00,'ml'),(18,'Café con Leche de Almendra',4,12,15.00,'gr'),(19,'Café Clásico',5,2,165.00,'gr'),(20,'Café Clásico',5,3,175.00,'ml'),(21,'Café Clásico',5,12,15.00,'gr'),(22,'Café Americano',6,1,60.00,'ml'),(23,'Café Americano',6,13,295.00,'ml'),(24,'Café Moka',7,1,60.00,'ml'),(25,'Café Moka',7,3,230.00,'ml'),(26,'Café Moka',7,8,35.00,'ml'),(28,'Café de Olla',8,2,320.00,'gr'),(29,'Café de Olla',8,15,25.00,'ml'),(30,'Café de Olla',8,13,10.00,'ml'),(31,'Café de Vainilla',9,1,60.00,'ml'),(32,'Café de Vainilla',9,3,240.00,'ml'),(33,'Café de Vainilla',9,11,25.00,'ml'),(35,'Café Latte',10,1,60.00,'ml'),(36,'Café Latte',10,3,15.00,'ml'),(37,'Café Latte',10,6,280.00,'ml'),(38,'Frappe Moka',11,1,25.00,'ml'),(39,'Frappe Moka',11,3,60.00,'ml'),(40,'Frappe Moka',11,8,25.00,'ml'),(41,'Frappe Moka',11,12,15.00,'gr'),(43,'Frappe Oreo',12,3,200.00,'ml'),(44,'Frappe Oreo',12,6,20.00,'ml'),(45,'Frappe Oreo',12,8,10.00,'ml'),(46,'Frappe Oreo',12,12,20.00,'gr'),(47,'Frappe Oreo',12,14,150.00,'gr'),(48,'Café Americano',6,12,15.00,'gr'),(49,'Frappe Moka',11,14,150.00,'gr'),(50,'Frappe Oreo',12,17,50.00,'gr'),(56,'Café Mocha con Chocolate Blanco',1,14,100.00,'gr'),(57,'Café de Caramelo',2,14,100.00,'gr'),(58,'Café de Coco',3,14,100.00,'gr'),(59,'Café con Leche de Almendra',4,14,100.00,'gr'),(60,'Café Clásico',5,14,100.00,'gr'),(61,'Café Moka',7,14,100.00,'gr'),(62,'Café de Vainilla',9,14,100.00,'gr'),(63,'Café Latte',10,14,100.00,'gr');
/*!40000 ALTER TABLE `recetas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `telefono` varchar(15) DEFAULT NULL,
  `direccion` text,
  `rol` enum('admin','cliente') DEFAULT 'cliente',
  `activo` tinyint(1) DEFAULT '1',
  `fecha_registro` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_actualizacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `verificado` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `idx_email` (`email`),
  KEY `idx_rol` (`rol`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Carlos','Rios Ramirez','carlosriosrmz17@gmail.com','pbkdf2:sha256:600000$mGr2pvXLntf2EBQw$c230c629753b05b5c2f2ecaff0d77f0565f5f7ca705d245ea702c2a24239eca4','479-225-81-84','Eucaliptos #304','admin',1,'2026-04-14 00:42:33','2026-04-14 01:02:24',1),(2,'Lluvia','Teran Mares','lluviacoffe@gmail.com','pbkdf2:sha256:600000$KBB5pq4tuZ9itoyn$d857e4d6e6f3fe861fb99b0f5e3a63278c0e063d202ee6444d17dd71a008478e','477-635-2193','León, Gto.','admin',1,'2026-04-14 00:58:22','2026-04-14 00:58:22',1),(3,'Nestor','Muñoz Garcia','nestorcoffee@gmail.com','pbkdf2:sha256:600000$30iUuradTjlJGC9H$dff468ef31022d6cfdbab3822c7c6595f4ebe415f2341662f13337a848e3b0e9','477-618-6479','León, Gto.','admin',1,'2026-04-14 00:58:22','2026-04-14 00:58:22',1),(10,'Brenda Paola ','Ramirez','paolaramirez1328@gmail.com','scrypt:32768:8:1$yUw3rZVcox5OtguW$150ddf78350f35e172ed3b43c334800903b078d3af5949f0a878ab45b19bf2540e73e1078d12835e7e3b7415eacfc454eff5363784e9e9a30309305a03c8f25a',NULL,NULL,'cliente',1,'2026-04-14 07:18:56','2026-04-14 07:19:16',1),(11,'Miguel Angel ','Rangel Munoz','angelrangelmunoz123@gmail.com','scrypt:32768:8:1$jQTAtxjFRI7a9WmN$6ea7d126c0a3cabad183d2af26474a1d390a0813399cf9c84d59542a7519e96960d7fa6ff1b6a601bc121454c42c507222bf4d742a0aee9a4eb2cd3233c036eb',NULL,NULL,'cliente',1,'2026-04-14 07:36:29','2026-04-14 07:38:04',1),(12,'Vanessa de la Luz','Perez Martinez','brawlstarsdsm@gmail.com','scrypt:32768:8:1$Z0RFEXOs5XRCV0UN$a89996baf10edaa19704ffac055e26024b9540273f3884c9c7e512c2056103f9180f276735253fefae51462c5270c33cfd8d920259733e1ac4fe8952ea7c65b4',NULL,NULL,'cliente',1,'2026-04-14 07:48:48','2026-04-14 07:49:05',1),(13,'Rogelio',' Rios Reyes','rogeliorios502@gmail.com','scrypt:32768:8:1$dun2V5hAXVhizd0s$6660a918f004b496de5dd156fe22717ef9dd951bfed9c39c5cffc75bce4411d840f38500e7d0553b84b2a6f40383a910e749181cc733632f4c060d2c7643c2c9',NULL,NULL,'cliente',1,'2026-04-16 04:43:36','2026-04-16 04:44:01',1),(14,'Angel David','Grandos Rocha','riosangel305@gmail.com','scrypt:32768:8:1$4NFgWOvulOovDboj$753600bdb0ef2d443758e99322dadc4f76c4343668ddbeabdd3bf18870763b5359edea5f32296a2c67734f90ea5e654ec1b040ffc9fec0d8ddadfc273be31223',NULL,NULL,'cliente',1,'2026-04-16 05:20:44','2026-04-16 05:21:17',1),(15,'Salvador Ezquivel','Castillo Torres','esquivelsalvador241@gmail.com','scrypt:32768:8:1$hpADC9qSY6bl5gl7$304dcced4896c3543b1eafcd36ff1a589ccfad630c0e790dcc0ab0a91c79a820d8869a5be9cc123052912a1992d1529ec2b613a3b67e3c8f101ce10dfdc4611d',NULL,NULL,'cliente',1,'2026-04-16 05:23:02','2026-04-16 05:23:38',1),(16,'Yahir Daniel ','Rios Murillo','yahirrios153@gmail.com','scrypt:32768:8:1$LLNlkrN6rfPQnGbW$6bdf3cc9106184b4a0b9ebbc78845235caf95d30f34372583b67602bd5400760f90515e6a1cec943446f889ce7d21db7744022b505ad2b36819e8c6e29ea83cd',NULL,NULL,'cliente',1,'2026-04-16 05:25:10','2026-04-16 05:25:48',1),(17,'Diego AAron','Gonzales Anguiano','aaronglzang0802@gmail.com','scrypt:32768:8:1$knbu1mncDW0bVUiL$d24bf868c80b12d65512e915ae7f5e152a3e94e7b57c34bf17c6f0f78e977ec672e17eb3188ab98c21dbbad97d06bf3d57fb359bfe5b91001ddc0594a579b3e4',NULL,NULL,'cliente',1,'2026-04-16 06:26:30','2026-04-16 06:27:27',1);
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ventas`
--

DROP TABLE IF EXISTS `ventas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ventas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pedido_id` int NOT NULL,
  `fecha_venta` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `metodo_pago` enum('efectivo','tarjeta','transferencia','paypal') NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado_pago` enum('pendiente','pagado','reembolsado') DEFAULT 'pendiente',
  `referencia_pago` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_fecha` (`fecha_venta`),
  KEY `idx_pedido` (`pedido_id`),
  KEY `idx_estado_pago` (`estado_pago`),
  CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`pedido_id`) REFERENCES `pedidos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
INSERT INTO `ventas` VALUES (1,1,'2026-04-14 07:30:31','tarjeta',225.00,'pagado','CT-20260413-001'),(2,2,'2026-04-14 07:53:27','efectivo',200.00,'pagado','CT-20260413-002'),(3,3,'2026-04-14 08:07:54','transferencia',225.00,'pagado','CT-20260413-003'),(4,4,'2026-04-14 09:19:50','tarjeta',95.00,'pagado','CT-20260413-004'),(5,5,'2026-04-16 04:55:36','efectivo',315.00,'pagado','CT-20260415-005'),(6,6,'2026-04-16 04:55:49','tarjeta',225.00,'pagado','CT-20260415-006'),(7,7,'2026-04-16 05:32:36','tarjeta',290.00,'pagado','CT-20260415-007'),(8,8,'2026-04-16 05:32:49','efectivo',130.00,'pagado','CT-20260415-008'),(9,9,'2026-04-16 05:32:52','tarjeta',120.00,'pagado','CT-20260415-009'),(10,10,'2026-04-16 06:34:02','efectivo',90.00,'pagado','CT-20260415-010'),(11,11,'2026-04-16 09:24:23','efectivo',120.00,'pagado','CT-20260415-011'),(12,12,'2026-04-16 09:27:59','efectivo',110.00,'pagado','CT-20260415-012');
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-17 23:00:20
