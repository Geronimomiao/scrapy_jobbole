/*
 Navicat Premium Data Transfer

 Source Server         : local
 Source Server Type    : MySQL
 Source Server Version : 50724
 Source Host           : localhost:3306
 Source Schema         : article_spider

 Target Server Type    : MySQL
 Target Server Version : 50724
 File Encoding         : 65001

 Date: 03/01/2019 21:10:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for article
-- ----------------------------
DROP TABLE IF EXISTS `article`;
CREATE TABLE `article` (
  `title` varchar(200) DEFAULT NULL,
  `create_date` varchar(20) DEFAULT NULL,
  `url` varchar(300) DEFAULT NULL,
  `url_object_id` varchar(50) NOT NULL,
  `praise_nums` int(11) DEFAULT NULL,
  `fav_nums` int(11) DEFAULT NULL,
  `comment_nums` int(11) DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `content` longtext,
  `front_image_url` varchar(300) DEFAULT NULL,
  `front_image_path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`url_object_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

SET FOREIGN_KEY_CHECKS = 1;
