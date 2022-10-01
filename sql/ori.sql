-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.9.2-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- saesol-api 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `saesol-api` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `saesol-api`;

-- 테이블 saesol-api.log 구조 내보내기
CREATE TABLE IF NOT EXISTS `log` (
  `user_id` varchar(10) DEFAULT NULL,
  `notifi_title` varchar(30) DEFAULT NULL,
  `notifi_content` varchar(100) DEFAULT NULL,
  `upload_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.log:~0 rows (대략적) 내보내기
DELETE FROM `log`;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` (`user_id`, `notifi_title`, `notifi_content`, `upload_time`) VALUES
	('admin', 'test1', 'test1', '2022-09-07 13:26:40');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;

-- 테이블 saesol-api.one_used_account 구조 내보내기
CREATE TABLE IF NOT EXISTS `one_used_account` (
  `user_id` varchar(13) DEFAULT NULL,
  `acc_id` varchar(10) DEFAULT NULL,
  `pw` varchar(15) DEFAULT NULL,
  `pw_hash` varchar(64) DEFAULT NULL,
  `used` tinyint(4) DEFAULT 0,
  `login_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.one_used_account:~0 rows (대략적) 내보내기
DELETE FROM `one_used_account`;
/*!40000 ALTER TABLE `one_used_account` DISABLE KEYS */;
/*!40000 ALTER TABLE `one_used_account` ENABLE KEYS */;

-- 테이블 saesol-api.user_data 구조 내보내기
CREATE TABLE IF NOT EXISTS `user_data` (
  `user_name` varchar(6) DEFAULT NULL,
  `user_id` varchar(13) DEFAULT NULL,
  `pw_hash` varchar(64) DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  `permision` varchar(50) DEFAULT NULL,
  `auto_login` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='input_user data';

-- 테이블 데이터 saesol-api.user_data:~4 rows (대략적) 내보내기
DELETE FROM `user_data`;
/*!40000 ALTER TABLE `user_data` DISABLE KEYS */;
INSERT INTO `user_data` (`user_name`, `user_id`, `pw_hash`, `class`, `permision`, `auto_login`) VALUES
	('admin', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin', 'admin', 0),
	('1', '1', '1', '1', '1', 0),
	('user1', 'user1_id', 'this pw_hash', 'noclass', 'nopermission', 0);
/*!40000 ALTER TABLE `user_data` ENABLE KEYS */;

-- 테이블 saesol-api.user_email 구조 내보내기
CREATE TABLE IF NOT EXISTS `user_email` (
  `user_id` varchar(13) DEFAULT NULL,
  `user_email` varchar(30) DEFAULT NULL,
  `confirm` tinyint(4) NOT NULL DEFAULT 0,
  `confirm_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.user_email:~1 rows (대략적) 내보내기
DELETE FROM `user_email`;
/*!40000 ALTER TABLE `user_email` DISABLE KEYS */;
INSERT INTO `user_email` (`user_id`, `user_email`, `confirm`, `confirm_date`) VALUES
	('admin', 'jiseop1008@gmail.com', 0, '2022-09-26 16:38:46');
/*!40000 ALTER TABLE `user_email` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
