-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: coffeetrack
-- ------------------------------------------------------
-- Server version	8.0.33

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
  KEY `idx_alertas_activa` (`activa`),
  KEY `idx_alertas_fecha` (`fecha_alerta`),
  CONSTRAINT `alertas_inventario_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `alertas_inventario_ibfk_2` FOREIGN KEY (`bebida_id`) REFERENCES `bebidas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alertas_inventario`
--

LOCK TABLES `alertas_inventario` WRITE;
/*!40000 ALTER TABLE `alertas_inventario` DISABLE KEYS */;
INSERT INTO `alertas_inventario` VALUES (1,NULL,1,'bebida_agotada','La bebida \"Café Mocha con Chocolate Blanco\" esta agotada',0,'2026-04-08 06:07:29','2026-04-17 21:27:24'),(2,NULL,2,'stock_bajo_bebida','Stock bajo de \"Café de Caramelo\": -1 unidades',1,'2026-04-13 20:27:45',NULL),(3,NULL,3,'stock_bajo_bebida','Stock bajo de \"Café de Coco\": -1 unidades',1,'2026-04-13 20:27:45',NULL),(4,NULL,4,'stock_bajo_bebida','Stock bajo de \"Café con Leche de Almendra\": -1 unidades',1,'2026-04-13 20:27:45',NULL);
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
  PRIMARY KEY (`id`),
  KEY `idx_nombre` (`nombre`),
  KEY `idx_categoria` (`categoria_id`),
  KEY `idx_disponible` (`disponible`),
  KEY `idx_bebidas_nombre` (`nombre`),
  KEY `idx_bebidas_categoria` (`categoria_id`),
  KEY `idx_bebidas_disponible` (`disponible`),
  KEY `idx_bebidas_categoria_disponible` (`categoria_id`,`disponible`),
  CONSTRAINT `bebidas_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categoria_bebidas` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `bebidas`
--

LOCK TABLES `bebidas` WRITE;
/*!40000 ALTER TABLE `bebidas` DISABLE KEYS */;
INSERT INTO `bebidas` VALUES (1,'Café Mocha con Chocolate Blanco','Delicioso café con chocolate blanco y espresso',1,355,65.00,NULL,1,-1,5,1,'2026-04-08 06:06:32','2026-04-13 20:27:45'),(2,'Café de Caramelo','Café espresso con jarabe de caramelo',1,355,60.00,NULL,1,-1,5,1,'2026-04-08 06:06:32','2026-04-13 20:27:45'),(3,'Café de Coco','Café con leche de coco y jarabe de coco',1,355,65.00,NULL,1,-1,5,1,'2026-04-08 06:06:32','2026-04-13 20:27:45'),(4,'Café con Leche de Almendra','Café espresso con leche de almendra',3,355,60.00,NULL,1,-1,5,1,'2026-04-08 06:06:32','2026-04-13 20:27:45'),(5,'Café Clásico','Café tradicional con leche y azúcar',2,355,45.00,NULL,1,0,5,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(6,'Café Americano','Espresso con agua caliente',2,355,40.00,NULL,1,0,5,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(7,'Café Moka','Café con chocolate y leche',1,355,60.00,NULL,1,0,5,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(8,'Café de Olla','Café tradicional mexicano con piloncillo',2,355,50.00,NULL,1,0,5,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(9,'Café de Vainilla','Café con jarabe de vainilla',1,355,55.00,NULL,1,0,5,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(10,'Café Latte','Espresso con leche vaporizada',3,355,55.00,NULL,1,0,5,1,'2026-04-08 06:06:32','2026-04-08 06:06:32');
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
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria_bebidas`
--

LOCK TABLES `categoria_bebidas` WRITE;
/*!40000 ALTER TABLE `categoria_bebidas` DISABLE KEYS */;
INSERT INTO `categoria_bebidas` VALUES (1,'Cafés  Especiales','Bebidas de café con sabores únicos','2026-04-08 06:06:32'),(2,'Cafés  Clasicos','Bebidas de café tradicionales','2026-04-08 06:06:32'),(3,'Cafés con Leche','Bebidas de café con diferentes tipos de leche ','2026-04-08 06:06:32');
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
INSERT INTO `categorias_materia_prima` VALUES (1,'Café','Tipos de café  granos o molido','2026-04-08 06:06:32'),(2,'Lácteos','Leche y derivados','2026-04-08 06:06:32'),(3,'Endulzantes','Azúcar  y jarabes','2026-04-08 06:06:32'),(4,'Saborizantes','Chocolates, vainilla y otros sabores','2026-04-08 06:06:32'),(5,'Otros','Hielo y otros insumos','2026-04-08 06:06:32');
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
  `expira_en` timestamp NOT NULL,
  `usado` tinyint(1) DEFAULT '0',
  `fecha_creacion` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `codigos_verificacion_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `codigos_verificacion`
--

LOCK TABLES `codigos_verificacion` WRITE;
/*!40000 ALTER TABLE `codigos_verificacion` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedidos`
--

LOCK TABLES `detalle_pedidos` WRITE;
/*!40000 ALTER TABLE `detalle_pedidos` DISABLE KEYS */;
INSERT INTO `detalle_pedidos` VALUES (1,1,1,1,65.00,65.00,'caliente'),(2,1,2,1,60.00,60.00,'frio'),(3,1,3,1,65.00,65.00,'caliente'),(4,1,4,1,60.00,60.00,'frio');
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
  KEY `idx_historial_materia` (`materia_prima_id`),
  KEY `idx_historial_fecha` (`fecha_movimiento`),
  KEY `idx_historial_tipo` (`tipo_movimiento`),
  CONSTRAINT `historial_inventario_ibfk_1` FOREIGN KEY (`materia_prima_id`) REFERENCES `materias_primas` (`id`),
  CONSTRAINT `historial_inventario_ibfk_2` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_inventario`
--

LOCK TABLES `historial_inventario` WRITE;
/*!40000 ALTER TABLE `historial_inventario` DISABLE KEYS */;
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
  KEY `idx_materias_nombre` (`nombre`),
  KEY `idx_materias_categoria` (`categoria_id`),
  CONSTRAINT `materias_primas_ibfk_1` FOREIGN KEY (`categoria_id`) REFERENCES `categorias_materia_prima` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `materias_primas`
--

LOCK TABLES `materias_primas` WRITE;
/*!40000 ALTER TABLE `materias_primas` DISABLE KEYS */;
INSERT INTO `materias_primas` VALUES (1,'Espresso',1,'ml',10000.00,1000.00,0.080,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(2,'Café  molido',1,'gr',10000.00,1000.00,0.120,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(3,'Leche',2,'ml',20000.00,2000.00,0.022,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(4,'Leche de almendra ',2,'ml',20000.00,2000.00,0.040,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(5,'Leche de coco',2,'ml',20000.00,2000.00,0.038,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(6,'Leche vaporizada',2,'ml',20000.00,2000.00,0.022,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(7,'Chocolate blanco',4,'ml',30000.00,3000.00,0.120,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(8,'Chocolate',4,'ml',30000.00,3000.00,0.100,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(9,'Jarabe de caramelo',4,'ml',30000.00,3000.00,0.080,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(10,'Jarabe de coco',4,'ml',20000.00,2000.00,0.075,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(11,'Jarabe de vainilla',4,'ml',20000.00,2000.00,0.080,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(12,'Azúcar',3,'gr',10000.00,1000.00,0.022,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(13,'Agua',5,'ml',10000.00,1000.00,0.010,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(14,'Hielo/Agua fria',5,'gr',5000.00,500.00,0.015,1,'2026-04-08 06:06:32','2026-04-08 06:06:32'),(15,'Piloncillo',3,'ml',2000.00,200.00,0.045,1,'2026-04-08 06:06:32','2026-04-08 06:06:32');
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
  PRIMARY KEY (`id`),
  KEY `idx_usuario` (`usuario_id`),
  KEY `idx_fecha` (`fecha_pedido`),
  KEY `idx_estado` (`estado`),
  KEY `idx_pedidos_usuario` (`usuario_id`),
  KEY `idx_pedidos_fecha` (`fecha_pedido`),
  KEY `idx_pedidos_estado` (`estado`),
  KEY `idx_pedidos_usuario_estado` (`usuario_id`,`estado`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,5,'2026-04-08 23:25:51',250.00,0.00,250.00,'confirmado','san agostino roscelli 117','4771522100','casa de un piso | REF: CT-20260408-001',NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccion`
--

LOCK TABLES `produccion` WRITE;
/*!40000 ALTER TABLE `produccion` DISABLE KEYS */;
INSERT INTO `produccion` VALUES (1,1,4,'2026-04-08',63.84,2,'','completada','2026-04-08 12:06:55',0),(2,1,4,'2026-04-08',69.84,2,'','completada','2026-04-08 12:07:14',1),(3,1,1,'2026-04-08',16.96,2,'Generado automáticamente por Pedido #1','planificada','2026-04-09 02:15:11',0),(4,2,1,'2026-04-08',14.29,2,'Generado automáticamente por Pedido #1','planificada','2026-04-09 02:15:11',1),(5,3,1,'2026-04-08',12.40,2,'Generado automáticamente por Pedido #1','planificada','2026-04-09 02:15:11',0),(6,4,1,'2026-04-08',17.41,2,'Generado automáticamente por Pedido #1','planificada','2026-04-09 02:15:11',1);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedores`
--

LOCK TABLES `proveedores` WRITE;
/*!40000 ALTER TABLE `proveedores` DISABLE KEYS */;
INSERT INTO `proveedores` VALUES (2,'La Concha Repostería ','Gerente de Sucursal (Miguel Alemán)','477 713 2005','ventas.centro@laconcha.com.mx','Av. Miguel Alemán 140, Locales 5 y 6, Centro','LCO850101ABC',1,'2026-04-08 22:47:54','2026-04-08 22:47:54'),(3,'Café Punta del Cielo','Administrador de ventas','555 516 8020','contacto@puntadelcielo.com.mx','Blvd. Juan Alonso de Torres 1315, San José','CPC0402187H5',1,'2026-04-08 22:48:55','2026-04-08 22:48:55'),(4,'Nestlé','Ejecutivo de Cuenta','477 710 7100','servicio.clientes@nestle.com','Av. del Tecnológico 308, Julián de Obregón','NES920331S12',1,'2026-04-08 22:49:36','2026-04-08 22:49:36'),(5,'Bonafont León','Coord. Logística','477 792 2922','institucional.leon@bonafont.com','Rafael Corrales Ayala 2107, Industrial','BON9206159A5',1,'2026-04-08 22:50:53','2026-04-08 22:50:53'),(6,'City Abasto','Atención Mayoristas','477 763 5196','ventas.centro@laconcha.com.mx','Central de Abastos, Hnos. Aldama 4102','CAB120520UX2',1,'2026-04-08 22:51:37','2026-04-08 22:51:37'),(7,'Walmart León','Jefe de Perecederos','800 925 6278','atencion.clientes@walmart.com','Blvd. Juan Alonso de Torres Pte. 1325, San José del Consuelo.','WWM951201TR4',1,'2026-04-08 22:52:35','2026-04-08 22:52:35'),(8,'Hielo Crystal de Leon','Alejandro González Coordinador de Ventas','4777120931','redesociales24crystal@gmail.com','VENUSTIANO CARRANZA 1101 SAN MIGUEL, LEON, GUANAJUATO 37390','HCL0204128X4',1,'2026-04-08 23:00:36','2026-04-08 23:01:23'),(9,'Grupo Lala, S.A.B. de C.V.','Departamento de Atención Edgar salinas','477 710 7100','edgar.salinas@grupolala.com','Blvd. Hermanos Aldama 5975, Industrial','GLA8502016A1',1,'2026-04-08 23:02:27','2026-04-08 23:02:27');
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
) ENGINE=InnoDB AUTO_INCREMENT=39 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `recetas`
--

LOCK TABLES `recetas` WRITE;
/*!40000 ALTER TABLE `recetas` DISABLE KEYS */;
INSERT INTO `recetas` VALUES (1,'Café Mocha con Chocolate Blanco',1,1,60.00,'ml'),(2,'Café Mocha con Chocolate Blanco',1,7,30.00,'ml'),(3,'Café Mocha con Chocolate Blanco',1,9,20.00,'ml'),(4,'Café Mocha con Chocolate Blanco',1,6,15.00,'ml'),(5,'Café Mocha con Chocolate Blanco',1,13,87.00,'ml'),(6,'Café Mocha con Chocolate Blanco',1,3,240.00,'ml'),(7,'Café de Caramelo',2,1,60.00,'ml'),(8,'Café de Caramelo',2,3,230.00,'ml'),(9,'Café de Caramelo',2,9,30.00,'ml'),(10,'Café de Caramelo',2,14,35.00,'ml'),(11,'Café de Coco',3,1,60.00,'ml'),(12,'Café de Coco',3,3,240.00,'ml'),(13,'Café de Coco',3,10,25.00,'ml'),(14,'Café de Coco',3,14,30.00,'ml'),(15,'Café de leche de almendra',4,1,60.00,'ml'),(16,'Café de leche de almendra',4,4,260.00,'ml'),(17,'Café de leche de almendra',4,14,25.00,'ml'),(18,'Café de leche de almendra',4,12,15.00,'gr'),(19,'Café clasico ',5,2,165.00,'gr'),(20,'Café clasico ',5,3,175.00,'ml'),(21,'Café clasico ',5,12,15.00,'gr'),(22,'Café Americano',6,1,60.00,'ml'),(23,'Café Americano',6,13,295.00,'ml'),(24,'Café Moka',7,1,60.00,'ml'),(25,'Café Moka',7,3,230.00,'ml'),(26,'Café Moka',7,8,35.00,'ml'),(27,'Café Moka',7,14,40.00,'ml'),(28,'Café de olla',8,2,4.40,'gr'),(29,'Café de olla',8,15,25.00,'ml'),(30,'Café de olla',8,13,10.00,'ml'),(31,'Café de Vainilla',9,1,60.00,'ml'),(32,'Café de Vainilla',9,3,240.00,'ml'),(33,'Café de Vainilla',9,11,25.00,'ml'),(34,'Café de Vainilla',9,14,30.00,'ml'),(35,'Café de Latte',10,1,60.00,'ml'),(36,'Café de Latte',10,3,15.00,'ml'),(37,'Café de Latte',10,6,280.00,'ml'),(38,'Café Mocha con Chocolate Blanco',1,2,4.00,'gr');
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
  KEY `idx_rol` (`rol`),
  KEY `idx_usuarios_email` (`email`),
  KEY `idx_usuarios_rol` (`rol`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'Carlos','Rios Ramirez','carlosriosrmz17@gmail.com','pbkdf2:sha256:600000$mGr2pvXLntf2EBQw$c230c629753b05b5c2f2ecaff0d77f0565f5f7ca705d245ea702c2a24239eca4','479-225-81-84','Eucaliptos #304','admin',1,'2026-04-08 06:06:31','2026-04-08 06:15:42',1),(2,'Lluvia','Teran Mares','lluviacoffe@gmail.com','pbkdf2:sha256:600000$KBB5pq4tuZ9itoyn$d857e4d6e6f3fe861fb99b0f5e3a63278c0e063d202ee6444d17dd71a008478e','477-635-2193','León, Gto.','admin',1,'2026-04-08 06:06:32','2026-04-08 06:15:42',1),(3,'Nestor','Muñoz Garcia','nestorcoffee@gmail.com.com','pbkdf2:sha256:600000$30iUuradTjlJGC9H$dff468ef31022d6cfdbab3822c7c6595f4ebe415f2341662f13337a848e3b0e9','477-618-6479','León, Gto.','admin',1,'2026-04-08 06:06:32','2026-04-08 06:15:42',1),(5,'Rosario','Teran Mares','teran@gmail.com','scrypt:32768:8:1$bVHJOqfnBcb4BZcJ$84ba3b022b3de93771e88871416b1c8eba9556bd84aa140e83ca66d1034a35ad766eb4081c0bd3d5a64f97cc07786b00f6e571198ef3791818b2cf6f1d0c0bf9','4771522100',NULL,'cliente',1,'2026-04-08 23:09:08','2026-04-08 23:09:08',1);
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ventas`
--

LOCK TABLES `ventas` WRITE;
/*!40000 ALTER TABLE `ventas` DISABLE KEYS */;
/*!40000 ALTER TABLE `ventas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_alertas_activas`
--

DROP TABLE IF EXISTS `vista_alertas_activas`;
/*!50001 DROP VIEW IF EXISTS `vista_alertas_activas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_alertas_activas` AS SELECT 
 1 AS `id`,
 1 AS `tipo_alerta`,
 1 AS `mensaje`,
 1 AS `fecha_alerta`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_bebidas`
--

DROP TABLE IF EXISTS `vista_bebidas`;
/*!50001 DROP VIEW IF EXISTS `vista_bebidas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_bebidas` AS SELECT 
 1 AS `id`,
 1 AS `nombre`,
 1 AS `categoria`,
 1 AS `precio`,
 1 AS `stock_actual`,
 1 AS `disponible`,
 1 AS `activo`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_historial_inventario`
--

DROP TABLE IF EXISTS `vista_historial_inventario`;
/*!50001 DROP VIEW IF EXISTS `vista_historial_inventario`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_historial_inventario` AS SELECT 
 1 AS `id`,
 1 AS `materia_prima`,
 1 AS `tipo_movimiento`,
 1 AS `cantidad`,
 1 AS `stock_anterior`,
 1 AS `stock_nuevo`,
 1 AS `fecha_movimiento`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_materias_primas`
--

DROP TABLE IF EXISTS `vista_materias_primas`;
/*!50001 DROP VIEW IF EXISTS `vista_materias_primas`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_materias_primas` AS SELECT 
 1 AS `id`,
 1 AS `nombre`,
 1 AS `categoria`,
 1 AS `stock_actual`,
 1 AS `stock_minimo`,
 1 AS `precio_unitario`,
 1 AS `activo`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_pedidos`
--

DROP TABLE IF EXISTS `vista_pedidos`;
/*!50001 DROP VIEW IF EXISTS `vista_pedidos`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_pedidos` AS SELECT 
 1 AS `id`,
 1 AS `cliente`,
 1 AS `email`,
 1 AS `total`,
 1 AS `estado`,
 1 AS `fecha_pedido`,
 1 AS `direccion_entrega`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `vista_usuarios`
--

DROP TABLE IF EXISTS `vista_usuarios`;
/*!50001 DROP VIEW IF EXISTS `vista_usuarios`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_usuarios` AS SELECT 
 1 AS `id`,
 1 AS `nombre`,
 1 AS `apellidos`,
 1 AS `email`,
 1 AS `rol`,
 1 AS `activo`,
 1 AS `verificado`,
 1 AS `fecha_registro`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vista_alertas_activas`
--

/*!50001 DROP VIEW IF EXISTS `vista_alertas_activas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_alertas_activas` AS select `alertas_inventario`.`id` AS `id`,`alertas_inventario`.`tipo_alerta` AS `tipo_alerta`,`alertas_inventario`.`mensaje` AS `mensaje`,`alertas_inventario`.`fecha_alerta` AS `fecha_alerta` from `alertas_inventario` where (`alertas_inventario`.`activa` = true) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_bebidas`
--

/*!50001 DROP VIEW IF EXISTS `vista_bebidas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_bebidas` AS select `b`.`id` AS `id`,`b`.`nombre` AS `nombre`,`c`.`nombre` AS `categoria`,`b`.`precio` AS `precio`,`b`.`stock_actual` AS `stock_actual`,`b`.`disponible` AS `disponible`,`b`.`activo` AS `activo` from (`bebidas` `b` join `categoria_bebidas` `c` on((`b`.`categoria_id` = `c`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_historial_inventario`
--

/*!50001 DROP VIEW IF EXISTS `vista_historial_inventario`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_historial_inventario` AS select `h`.`id` AS `id`,`m`.`nombre` AS `materia_prima`,`h`.`tipo_movimiento` AS `tipo_movimiento`,`h`.`cantidad` AS `cantidad`,`h`.`stock_anterior` AS `stock_anterior`,`h`.`stock_nuevo` AS `stock_nuevo`,`h`.`fecha_movimiento` AS `fecha_movimiento` from (`historial_inventario` `h` join `materias_primas` `m` on((`h`.`materia_prima_id` = `m`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_materias_primas`
--

/*!50001 DROP VIEW IF EXISTS `vista_materias_primas`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_materias_primas` AS select `mp`.`id` AS `id`,`mp`.`nombre` AS `nombre`,`c`.`nombre` AS `categoria`,`mp`.`stock_actual` AS `stock_actual`,`mp`.`stock_minimo` AS `stock_minimo`,`mp`.`precio_unitario` AS `precio_unitario`,`mp`.`activo` AS `activo` from (`materias_primas` `mp` join `categorias_materia_prima` `c` on((`mp`.`categoria_id` = `c`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_pedidos`
--

/*!50001 DROP VIEW IF EXISTS `vista_pedidos`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_pedidos` AS select `p`.`id` AS `id`,`u`.`nombre` AS `cliente`,`u`.`email` AS `email`,`p`.`total` AS `total`,`p`.`estado` AS `estado`,`p`.`fecha_pedido` AS `fecha_pedido`,`p`.`direccion_entrega` AS `direccion_entrega` from (`pedidos` `p` join `usuarios` `u` on((`p`.`usuario_id` = `u`.`id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `vista_usuarios`
--

/*!50001 DROP VIEW IF EXISTS `vista_usuarios`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_usuarios` AS select `usuarios`.`id` AS `id`,`usuarios`.`nombre` AS `nombre`,`usuarios`.`apellidos` AS `apellidos`,`usuarios`.`email` AS `email`,`usuarios`.`rol` AS `rol`,`usuarios`.`activo` AS `activo`,`usuarios`.`verificado` AS `verificado`,`usuarios`.`fecha_registro` AS `fecha_registro` from `usuarios` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-04-17 21:11:26
