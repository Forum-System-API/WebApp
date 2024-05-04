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
CREATE SCHEMA IF NOT EXISTS `webapp` DEFAULT CHARACTER SET latin1 ;
USE `webapp` ;

-- -----------------------------------------------------
-- Table `webapp`.`categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`categories` (
  `category_id` INT(11) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `is_private` TINYINT(4) NOT NULL DEFAULT 0,
  `is_locked` TINYINT(4) NOT NULL DEFAULT 0,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

INSERT INTO categories (`category_id`,`name`,`is_private`,`is_locked`) VALUES (1,'Sport',0,0);


-- -----------------------------------------------------
-- Table `webapp`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = latin1;

INSERT INTO users (`username`,`password`,`role`) VALUES ('john_doe','securepassword123','basic_user');
INSERT INTO users (`username`,`password`,`role`) VALUES ('john_doe','securepassword123','basic_user');
INSERT INTO users (`username`,`password`,`role`) VALUES ('craig','securepassword1234','basic_user');
INSERT INTO users (`username`,`password`,`role`) VALUES ('steven','securepassword1234','basic_user');

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
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webapp`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`messages` (
  `message_id` INT(11) NOT NULL,
  `text` TEXT NOT NULL,
  `timestamp` DATE NOT NULL,
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
-- Table `webapp`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`topics` (
  `topic_id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(200) NOT NULL,
  `category_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `best_reply_id` INT(11) NULL DEFAULT NULL,
  `is_locked` TINYINT(4) NOT NULL DEFAULT 0,
  `date_time` DATE NOT NULL,
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

INSERT INTO topics (`topic_id`,`title`,`category_id`,`user_id`,`best_reply_id`,`is_locked`,`date_time`,`is_private`) VALUES (1,'F1 Miami GP ',1,3,NULL,0,'2024-05-02',0);
INSERT INTO topics (`topic_id`,`title`,`category_id`,`user_id`,`best_reply_id`,`is_locked`,`date_time`,`is_private`) VALUES (2,'F1 Miami GP Sprint Quali',1,3,NULL,0,'2024-05-03',0);
INSERT INTO topics (`topic_id`,`title`,`category_id`,`user_id`,`best_reply_id`,`is_locked`,`date_time`,`is_private`) VALUES (3,'F1 Miami GP Quali',1,3,NULL,0,'2024-05-03',0);


-- -----------------------------------------------------
-- Table `webapp`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `topic_id` INT(11) NOT NULL,
  `user_id` INT(11) NOT NULL,
  `date_time` DATE NOT NULL,
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

INSERT INTO replies (`reply_id`,`text`,`topic_id`,`user_id`,`date_time`) VALUES (1,'Max Pole - Sprint Quali.',2,3,'2024-05-03');
INSERT INTO replies (`reply_id`,`text`,`topic_id`,`user_id`,`date_time`) VALUES (2,'No point watching, Verstappen wins again.',2,5,'2024-05-03');

-- -----------------------------------------------------
-- Table `webapp`.`votes`
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


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
