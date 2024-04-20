-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema webapp
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema webapp
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `webapp` DEFAULT CHARACTER SET latin1 ;
USE `webapp` ;

-- -----------------------------------------------------
-- Table `webapp`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`user` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  `email` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`category` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`category_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`topic`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`topic` (
  `topic_id` INT NOT NULL,
  `title` VARCHAR(45) NOT NULL,
  `category_category_id` INT NOT NULL,
  PRIMARY KEY (`topic_id`, `category_category_id`),
  INDEX `fk_topic_category1_idx` (`category_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_topic_category1`
    FOREIGN KEY (`category_category_id`)
    REFERENCES `webapp`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`reply`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`reply` (
  `reply_id` INT NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `upvotes` INT NULL,
  `downvotes` INT NULL,
  `topic_topic_id` INT NOT NULL,
  `topic_category_category_id` INT NOT NULL,
  PRIMARY KEY (`reply_id`, `topic_topic_id`, `topic_category_category_id`),
  INDEX `fk_reply_topic1_idx` (`topic_topic_id` ASC, `topic_category_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_reply_topic1`
    FOREIGN KEY (`topic_topic_id` , `topic_category_category_id`)
    REFERENCES `webapp`.`topic` (`topic_id` , `category_category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`message`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`message` (
  `message_id` INT NOT NULL AUTO_INCREMENT,
  `text` TEXT NOT NULL,
  `timestamp` DATE NOT NULL,
  `user_user_id` INT NOT NULL,
  PRIMARY KEY (`message_id`, `user_user_id`),
  UNIQUE INDEX `timestamp_UNIQUE` (`timestamp` ASC) VISIBLE,
  INDEX `fk_message_user1_idx` (`user_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_message_user1`
    FOREIGN KEY (`user_user_id`)
    REFERENCES `webapp`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `webapp`.`user_has_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `webapp`.`user_has_category` (
  `user_user_id` INT NOT NULL,
  `category_category_id` INT NOT NULL,
  PRIMARY KEY (`user_user_id`, `category_category_id`),
  INDEX `fk_user_has_category_category1_idx` (`category_category_id` ASC) VISIBLE,
  INDEX `fk_user_has_category_user_idx` (`user_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_user_has_category_user`
    FOREIGN KEY (`user_user_id`)
    REFERENCES `webapp`.`user` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_user_has_category_category1`
    FOREIGN KEY (`category_category_id`)
    REFERENCES `webapp`.`category` (`category_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
