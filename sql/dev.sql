-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.8.3-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  12.0.0.6468
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- saesol-api 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `saesol-api` /*!40100 DEFAULT CHARACTER SET utf8mb3 */;
USE `saesol-api`;

-- 테이블 saesol-api.code 구조 내보내기
CREATE TABLE IF NOT EXISTS `code` (
  `code` varchar(5) DEFAULT NULL,
  `used` int(11) DEFAULT NULL,
  `user_id` varchar(13) DEFAULT NULL,
  `limit` int(11) DEFAULT NULL,
  `group` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.code:~2 rows (대략적) 내보내기
DELETE FROM `code`;
INSERT INTO `code` (`code`, `used`, `user_id`, `limit`, `group`) VALUES
	('abcde', 0, 'admin', 100, 'saesol'),
	('12345', 1, 'user1', 10, 'saesol');

-- 테이블 saesol-api.group_log 구조 내보내기
CREATE TABLE IF NOT EXISTS `group_log` (
  `group_name` varchar(50) DEFAULT NULL,
  `user` varchar(50) DEFAULT NULL,
  `log` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.group_log:~0 rows (대략적) 내보내기
DELETE FROM `group_log`;

-- 테이블 saesol-api.img 구조 내보내기
CREATE TABLE IF NOT EXISTS `img` (
  `group_name` varchar(50) DEFAULT NULL,
  `img_file` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.img:~1 rows (대략적) 내보내기
DELETE FROM `img`;
INSERT INTO `img` (`group_name`, `img_file`) VALUES
	('saesol', '	https://saesol.hs.kr/hosts/saesol/doc/image/1012/1012..1589520368.png');

-- 테이블 saesol-api.invite_group 구조 내보내기
CREATE TABLE IF NOT EXISTS `invite_group` (
  `user_id` varchar(13) DEFAULT NULL,
  `invite_code` varchar(5) DEFAULT NULL,
  `group_name` varchar(13) DEFAULT NULL,
  `used` tinyint(4) DEFAULT 0,
  `how_many` int(11) DEFAULT NULL,
  `invite_type` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.invite_group:~0 rows (대략적) 내보내기
DELETE FROM `invite_group`;
INSERT INTO `invite_group` (`user_id`, `invite_code`, `group_name`, `used`, `how_many`, `invite_type`) VALUES
	('admin', 'aaaaa', NULL, 0, 10, 'user');

-- 테이블 saesol-api.log 구조 내보내기
CREATE TABLE IF NOT EXISTS `log` (
  `user_id` varchar(10) DEFAULT NULL,
  `notifi_title` varchar(30) DEFAULT NULL,
  `notifi_content` varchar(300) DEFAULT NULL,
  `upload_time` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.log:~0 rows (대략적) 내보내기
DELETE FROM `log`;
INSERT INTO `log` (`user_id`, `notifi_title`, `notifi_content`, `upload_time`) VALUES
	('admin', 'test1', 'test1', '2022-09-07 13:26:40');

-- 테이블 saesol-api.one_used_account 구조 내보내기
CREATE TABLE IF NOT EXISTS `one_used_account` (
  `id` varchar(13) DEFAULT NULL,
  `pw_hash` varchar(64) DEFAULT NULL,
  `pw` varchar(10) DEFAULT NULL,
  `used` tinyint(4) DEFAULT 0,
  `login_date` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.one_used_account:~0 rows (대략적) 내보내기
DELETE FROM `one_used_account`;

-- 테이블 saesol-api.user_data 구조 내보내기
CREATE TABLE IF NOT EXISTS `user_data` (
  `user_name` varchar(6) DEFAULT NULL,
  `user_id` varchar(13) DEFAULT NULL,
  `pw_hash` varchar(64) DEFAULT NULL,
  `class` varchar(10) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `permision` varchar(50) DEFAULT NULL,
  `auto_login` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COMMENT='input_user data';

-- 테이블 데이터 saesol-api.user_data:~1 rows (대략적) 내보내기
DELETE FROM `user_data`;
INSERT INTO `user_data` (`user_name`, `user_id`, `pw_hash`, `class`, `email`, `permision`, `auto_login`) VALUES
	('admin', 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', 'admin', NULL, 'admin', 0),
	('일반적인유저', 'user1', '0a041b9462caa4a31bac3567e0b6e6fd9100787db2ab433d96f6d178cabfce90', 'user', NULL, 'user', 0),
	('a', 'a', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'user', NULL, 'user', 0),
	('t2', 't2', 'c44474038d459e40e4714afefa7bf8dae9f9834b22f5e8ec1dd434ecb62b512e', 'user', NULL, 'user', 0),
	('t1', 't1', 'ca978112ca1bbdcafac231b39a23dc4da786eff8147c4e72b9807785afee48bb', 'user', 'a@a', 'user', 0);

-- 테이블 saesol-api.user_group 구조 내보내기
CREATE TABLE IF NOT EXISTS `user_group` (
  `admin` varchar(50) DEFAULT NULL,
  `user` varchar(300) DEFAULT NULL,
  `group_name` varchar(50) DEFAULT NULL,
  `school_name` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

-- 테이블 데이터 saesol-api.user_group:~1 rows (대략적) 내보내기
DELETE FROM `user_group`;
INSERT INTO `user_group` (`admin`, `user`, `group_name`, `school_name`) VALUES
	('/admin', '/user1/user2', 'saesol', '새솔고등학교');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
