<<<<<<< HEAD
# TO FOLLOW
=======
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
  `category_id` INT(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webapp`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`users` (
  `user_id` INT(11) NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `role` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webapp`.`categories_has_users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`categories_has_users` (
  `categories_category_id` INT(11) NOT NULL,
  `users_user_id` INT(11) NOT NULL,
  PRIMARY KEY (`categories_category_id`, `users_user_id`),
  INDEX `fk_categories_has_users_users1_idx` (`users_user_id` ASC) VISIBLE,
  INDEX `fk_categories_has_users_categories1_idx` (`categories_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_categories_has_users_categories1`
    FOREIGN KEY (`categories_category_id`)
    REFERENCES `webapp`.`categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_categories_has_users_users1`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webapp`.`messages`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`messages` (
  `message_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `timestamp` DATE NOT NULL,
  `user_user_id` INT(11) NOT NULL,
  PRIMARY KEY (`message_id`, `user_user_id`),
  UNIQUE INDEX `timestamp_UNIQUE` (`timestamp` ASC) VISIBLE,
  INDEX `fk_message_user1_idx` (`user_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_message_user1`
    FOREIGN KEY (`user_user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webapp`.`topics`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`topics` (
  `topic_id` INT(11) NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `category_category_id` INT(11) NOT NULL,
  `users_user_id` INT(11) NOT NULL,
  PRIMARY KEY (`topic_id`, `category_category_id`, `users_user_id`),
  INDEX `fk_topic_category1_idx` (`category_category_id` ASC) VISIBLE,
  INDEX `fk_topics_users1_idx` (`users_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_topic_category1`
    FOREIGN KEY (`category_category_id`)
    REFERENCES `webapp`.`categories` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_topics_users1`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `webapp`.`replies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`replies` (
  `reply_id` INT(11) NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `upvotes` INT(11) NULL DEFAULT NULL,
  `downvotes` INT(11) NULL DEFAULT NULL,
  `topic_topic_id` INT(11) NOT NULL,
  `topic_category_category_id` INT(11) NOT NULL,
  `users_user_id` INT(11) NOT NULL,
  PRIMARY KEY (`reply_id`, `topic_topic_id`, `topic_category_category_id`, `users_user_id`),
  INDEX `fk_reply_topic1_idx` (`topic_topic_id` ASC, `topic_category_category_id` ASC) VISIBLE,
  INDEX `fk_replies_users1_idx` (`users_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_reply_topic1`
    FOREIGN KEY (`topic_topic_id` , `topic_category_category_id`)
    REFERENCES `webapp`.`topics` (`topic_id` , `category_category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_replies_users1`
    FOREIGN KEY (`users_user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
>>>>>>> 56abfa5ac99223672e9ea9ddf3b2341e16961480
