-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema webapp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema webapp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `webapp` ;
USE `webapp` ;

-- -----------------------------------------------------
-- Table `webapp`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`categories` (
  `category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT(4) NOT NULL DEFAULT 0,
  `is_locked` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7;


-- -----------------------------------------------------
-- Table `webapp`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` TEXT NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5;


-- -----------------------------------------------------
-- Table `webapp`.`categories_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`categories_has_users` (
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `access_type` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`, `user_id`),
  INDEX `fk_categories_has_users_users1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_categories_has_users_categories_idx` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_users_categories`
    FOREIGN KEY (`category_id`)
    REFERENCES `webapp`.`categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`messages` (
  `message_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `sender_id` INT(11) NOT NULL,
  `recipient_id` INT(11) NOT NULL,
  PRIMARY KEY (`message_id`),
  INDEX `fk_messages_users1_idx` (`sender_id` ASC) ,
  INDEX `fk_messages_users2_idx` (`recipient_id` ASC) ,
  CONSTRAINT `fk_messages_users1`
    FOREIGN KEY (`sender_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_messages_users2`
    FOREIGN KEY (`recipient_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`topics` (
  `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  `date_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`topic_id`),
  INDEX `fk_topics_categories1_idx` (`category_id` ASC) ,
  INDEX `fk_topics_users1_idx` (`user_id` ASC) ,
  CONSTRAINT `fk_topics_categories1`
    FOREIGN KEY (`category_id`)
    REFERENCES `webapp`.`categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 7;


-- -----------------------------------------------------
-- Table `webapp`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `date_time` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP(),
  `topic_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  PRIMARY KEY (`reply_id`),
  INDEX `fk_replies_topics1_idx` (`topic_id` ASC) ,
  INDEX `fk_replies_users1_idx` (`user_id` ASC) ,
  CONSTRAINT `fk_replies_topics1`
    FOREIGN KEY (`topic_id`)
    REFERENCES `webapp`.`topics` (`topic_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 5;


-- -----------------------------------------------------
-- Table `webapp`.`votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`votes` (
  `user_id` INT(11) NOT NULL,
  `reply_id` INT(11) NOT NULL,
  `type_of_vote` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `reply_id`),
  INDEX `fk_users_has_replies_replies1_idx` (`reply_id` ASC) ,
  INDEX `fk_users_has_replies_users1_idx` (`user_id` ASC) ,
  CONSTRAINT `fk_users_has_replies_replies1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `webapp`.`replies` (`reply_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;


-- Insert sample data
INSERT INTO `webapp`.`categories` (`category_name`,`is_private`,`is_locked`) VALUES ('Arts',0,0);
INSERT INTO `webapp`.`categories` (`category_name`,`is_private`,`is_locked`) VALUES ('Sports',0,0);
INSERT INTO `webapp`.`categories` (`category_name`,`is_private`,`is_locked`) VALUES ('Science',0,0);
INSERT INTO `webapp`.`categories` (`category_name`,`is_private`,`is_locked`) VALUES ('News',0,0);
INSERT INTO `webapp`.`categories` (`category_name`,`is_private`,`is_locked`) VALUES ('Nature',0,0);
INSERT INTO `webapp`.`categories` (`category_name`,`is_private`,`is_locked`) VALUES ('Cooking',0,0);

INSERT INTO `webapp`.`users` ( `username`,`password`,`role`) VALUES 
('admin', '9cd34e3d1cdef8d5bab590f05b00dcbc9c7e20d7625b069d72aed16566a59ca7', 'admin'),
    ('Joey_Ramone', 'dda69783f28fdf6f1c5a83e8400f2472e9300887d1dffffe12a07b92a3d0aa25', 'basic_user'),
    ('MoSalah', '8eff929c533e9a6ef1261ed11572b17dfac3947722808a3d3803a781cafdc186', 'basic_user'),
    ('Sherlock', 'f90c0f69179ced9c447b111dd5235f5279b28674463a0a607ef8dda5909a8747', 'basic_user'),
    ('Eric', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', 'basic_user'),
    ('slave', '61e81a50ea9de3c9a48c95d6bb4aecc196de64d696fdd24f647afe18f9909d7c', 'basic_user'),
    ('skankhunt42', 'c4a1e6f3639a098e68060c2a31cfc3567bf68b3ec1bb4f843a34f7499caf2998', 'basic_user');

INSERT INTO `webapp`.`topics` (`title`,`category_id`,`user_id`) VALUES ('F1 Miami GP FP1',2,1);
INSERT INTO `webapp`.`topics` (`title`,`category_id`,`user_id`) VALUES ('F1 Miami GP Sprint Quali',2,1);

INSERT INTO `webapp`.`replies` (`text`,`topic_id`,`user_id`) VALUES ('Max Pole - Sprint Quali',2,1);
INSERT INTO `webapp`.`replies` (`text`,`topic_id`,`user_id`) VALUES ('Ferrari fans are crying again.',1,2);