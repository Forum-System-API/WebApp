SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Drop the existing `webapp` schema if it exists
DROP SCHEMA IF EXISTS `webapp`;

-- Create a new `webapp` schema
CREATE SCHEMA IF NOT EXISTS `webapp` DEFAULT CHARACTER SET latin1 ;
USE `webapp` ;

-- -----------------------------------------------------
-- Table structure for `categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`categories` (
  `category_id` INT(11) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT(4) NOT NULL DEFAULT 0,
  `is_locked` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table structure for `users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` TEXT NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table structure for `categories_has_users`
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
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table structure for `messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`messages` (
  `message_id` INT(11) NOT NULL,
  `text` TEXT NOT NULL,
  `timestamp` DATETIME NOT NULL,
  `sender_id` INT(11) NOT NULL,
  `recipient_id` INT(11) NOT NULL,
  PRIMARY KEY (`message_id`),
  INDEX `fk_messages_users1_idx` (`sender_id` ASC) VISIBLE,
  INDEX `fk_messages_users2_idx` (`recipient_id` ASC) VISIBLE,
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
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table structure for `topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`topics` (
  `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  `is_locked` TINYINT(4) NOT NULL DEFAULT 0,
  `date_time` DATETIME NOT NULL,
  `is_private` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`topic_id`),
  UNIQUE INDEX `best_reply_id_UNIQUE` (`best_reply_id` ASC) VISIBLE,
  INDEX `fk_topics_categories1_idx` (`category_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`user_id` ASC) VISIBLE,
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
AUTO_INCREMENT = 4
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table structure for `replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `topic_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `date_time` DATETIME NOT NULL,
  PRIMARY KEY (`reply_id`),
  INDEX `fk_replies_topics1_idx` (`topic_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`user_id` ASC) VISIBLE,
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
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table structure for `votes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`votes` (
  `user_id` INT(11) NOT NULL,
  `reply_id` INT(11) NOT NULL,
  `type_of_vote` INT(11) NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`, `reply_id`),
  INDEX `fk_users_has_replies_replies1_idx` (`reply_id` ASC) VISIBLE,
  INDEX `fk_users_has_replies_users1_idx` (`user_id` ASC) VISIBLE,
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
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

-- Insert sample data
INSERT INTO `webapp`.`categories` (`category_id`,`name`,`is_private`,`is_locked`) VALUES (1,'Arts',0,0);
INSERT INTO `webapp`.`categories` (`category_id`,`name`,`is_private`,`is_locked`) VALUES (2,'Sports',0,0);
INSERT INTO `webapp`.`categories` (`category_id`,`name`,`is_private`,`is_locked`) VALUES (3,'Science',0,0);
INSERT INTO `webapp`.`categories` (`category_id`,`name`,`is_private`,`is_locked`) VALUES (4,'News',0,0);
INSERT INTO `webapp`.`categories` (`category_id`,`name`,`is_private`,`is_locked`) VALUES (5,'Nature',0,0);
INSERT INTO `webapp`.`categories` (`category_id`,`name`,`is_private`,`is_locked`) VALUES (6,'Cooking',0,0);

INSERT INTO `webapp`.`users` (`user_id`, `username`,`password`,`role`) VALUES 
(1, 'admin','9cd34e3d1cdef8d5bab590f05b00dcbc9c7e20d7625b069d72aed16566a59ca7','admin'),
(2, 'Joey_Ramone','dda69783f28fdf6f1c5a83e8400f2472e9300887d1dffffe12a07b92a3d0aa25','basic_user'),
(3, 'MoSalah','8eff929c533e9a6ef1261ed11572b17dfac3947722808a3d3803a781cafdc186','basic_user'),
(4, 'Sherlock','f90c0f69179ced9c447b111dd5235f5279b28674463a0a607ef8dda5909a8747','basic_user');

INSERT INTO `webapp`.`topics` (`topic_id`,`title`,`category_id`,`user_id`,`best_reply_id`,`is_locked`,`date_time`,`is_private`) VALUES (1,'F1 Miami GP FP1',2,1,NULL,0,'2024-05-02 10:00:00',0);
INSERT INTO `webapp`.`topics` (`topic_id`,`title`,`category_id`,`user_id`,`best_reply_id`,`is_locked`,`date_time`,`is_private`) VALUES (2,'F1 Miami GP Sprint Quali',2,1,1,0,'2024-05-02 10:00:00',0);

INSERT INTO `webapp`.`replies` (`reply_id`,`text`,`topic_id`,`user_id`,`date_time`) VALUES (1,'Max Pole - Sprint Quali',2,1,'2024-05-04 00:20:00');
INSERT INTO `webapp`.`replies` (`reply_id`,`text`,`topic_id`,`user_id`,`date_time`) VALUES (2,'Ferrari fans are crying again.',1,2,'2024-05-03 17:00:00');

-- Set back SQL_MODE
SET SQL_MODE=@OLD_SQL_MODE;
