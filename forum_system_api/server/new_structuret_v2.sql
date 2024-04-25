-- MySQL Workbench Synchronization
-- Generated: 2024-04-25 13:06
-- Model: New Model
-- Version: 1.0
-- Project: Name of the project
-- Author: Vlad

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

ALTER TABLE `webapp`.`messages` 
DROP FOREIGN KEY `fk_message_user1`;

ALTER TABLE `webapp`.`topics` 
DROP FOREIGN KEY `fk_topics_users1`,
DROP FOREIGN KEY `fk_topic_category1`;

ALTER TABLE `webapp`.`replies` 
DROP FOREIGN KEY `fk_replies_users1`,
DROP FOREIGN KEY `fk_reply_topic1`;

ALTER TABLE `webapp`.`categories_has_users` 
DROP FOREIGN KEY `fk_categories_has_users_users1`,
DROP FOREIGN KEY `fk_categories_has_users_categories1`;

ALTER TABLE `webapp`.`users` 
CHANGE COLUMN `role` `role` VARCHAR(45) NOT NULL ;

ALTER TABLE `webapp`.`messages` 
DROP COLUMN `user_user_id`,
ADD COLUMN `sender_id` INT(11) NOT NULL AFTER `timestamp`,
ADD COLUMN `recipient_id` INT(11) NOT NULL AFTER `sender_id`,
CHANGE COLUMN `message_id` `message_id` INT(11) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`message_id`),
ADD INDEX `fk_messages_users1_idx` (`sender_id` ASC) VISIBLE,
ADD INDEX `fk_messages_users2_idx` (`recipient_id` ASC) VISIBLE,
DROP INDEX `fk_message_user1_idx` ,
DROP INDEX `timestamp_UNIQUE` ;
;

ALTER TABLE `webapp`.`categories` 
CHANGE COLUMN `category_id` `category_id` INT(11) NOT NULL ;

ALTER TABLE `webapp`.`topics` 
DROP COLUMN `category_category_id`,
ADD COLUMN `category_id` INT(11) NOT NULL AFTER `title`,
ADD COLUMN `best_reply_id` INT(11) NOT NULL AFTER `user_id`,
CHANGE COLUMN `users_user_id` `user_id` INT(11) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`topic_id`),
ADD INDEX `fk_topics_categories1_idx` (`category_id` ASC) VISIBLE,
ADD INDEX `fk_topics_users1_idx` (`user_id` ASC) VISIBLE,
DROP INDEX `fk_topics_users1_idx` ,
DROP INDEX `fk_topic_category1_idx` ;
;

ALTER TABLE `webapp`.`replies` 
DROP COLUMN `topic_category_category_id`,
DROP COLUMN `topic_topic_id`,
ADD COLUMN `topic_id` INT(11) NOT NULL AFTER `downvotes`,
CHANGE COLUMN `reply_id` `reply_id` INT(11) NOT NULL ,
CHANGE COLUMN `text` `text` VARCHAR(45) NOT NULL ,
CHANGE COLUMN `upvotes` `upvotes` INT(11) NULL DEFAULT 0 ,
CHANGE COLUMN `downvotes` `downvotes` VARCHAR(45) NULL DEFAULT 0 ,
CHANGE COLUMN `users_user_id` `user_id` INT(11) NOT NULL ,
DROP PRIMARY KEY,
ADD PRIMARY KEY (`reply_id`),
ADD INDEX `fk_replies_topics1_idx` (`topic_id` ASC) VISIBLE,
ADD INDEX `fk_replies_users1_idx` (`user_id` ASC) VISIBLE,
DROP INDEX `fk_replies_users1_idx` ,
DROP INDEX `fk_reply_topic1_idx` ;
;

ALTER TABLE `webapp`.`categories_has_users` 
ADD COLUMN `access_type` VARCHAR(45) NOT NULL AFTER `user_id`,
CHANGE COLUMN `categories_category_id` `category_id` INT(11) NOT NULL ,
CHANGE COLUMN `users_user_id` `user_id` INT(11) NOT NULL ,
ADD INDEX `fk_categories_has_users_users1_idx` (`user_id` ASC) VISIBLE,
ADD INDEX `fk_categories_has_users_categories_idx` (`category_id` ASC) VISIBLE,
DROP INDEX `fk_categories_has_users_categories1_idx` ,
DROP INDEX `fk_categories_has_users_users1_idx` ;
;

CREATE TABLE IF NOT EXISTS `webapp`.`votes` (
  `user_id` INT(11) NOT NULL,
  `reply_id` INT(11) NOT NULL,
  `type_of_vote` INT(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`, `reply_id`),
  INDEX `fk_users_has_replies_replies1_idx` (`reply_id` ASC) VISIBLE,
  INDEX `fk_users_has_replies_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_users_has_replies_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `webapp`.`users` (`user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_users_has_replies_replies1`
    FOREIGN KEY (`reply_id`)
    REFERENCES `webapp`.`replies` (`reply_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
DEFAULT CHARACTER SET = latin1;

ALTER TABLE `webapp`.`messages` 
ADD CONSTRAINT `fk_messages_users1`
  FOREIGN KEY (`sender_id`)
  REFERENCES `webapp`.`users` (`user_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_messages_users2`
  FOREIGN KEY (`recipient_id`)
  REFERENCES `webapp`.`users` (`user_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `webapp`.`topics` 
ADD CONSTRAINT `fk_topics_categories1`
  FOREIGN KEY (`category_id`)
  REFERENCES `webapp`.`categories` (`category_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_topics_users1`
  FOREIGN KEY (`user_id`)
  REFERENCES `webapp`.`users` (`user_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `webapp`.`replies` 
ADD CONSTRAINT `fk_replies_topics1`
  FOREIGN KEY (`topic_id`)
  REFERENCES `webapp`.`topics` (`topic_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_replies_users1`
  FOREIGN KEY (`user_id`)
  REFERENCES `webapp`.`users` (`user_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;

ALTER TABLE `webapp`.`categories_has_users` 
ADD CONSTRAINT `fk_categories_has_users_categories`
  FOREIGN KEY (`category_id`)
  REFERENCES `webapp`.`categories` (`category_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION,
ADD CONSTRAINT `fk_categories_has_users_users1`
  FOREIGN KEY (`user_id`)
  REFERENCES `webapp`.`users` (`user_id`)
  ON DELETE NO ACTION
  ON UPDATE NO ACTION;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
