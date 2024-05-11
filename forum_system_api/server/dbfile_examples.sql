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
    

INSERT INTO `webapp`.`topics` (`title`,`date_time`,`category_id`,`user_id`) VALUES ('F1 Miami GP FP1','2024-05-03 10:00:00',2,5);
INSERT INTO `webapp`.`topics` (`title`,`date_time`,`category_id`,`user_id`) VALUES ('F1 Miami GP Sprint Quali','2024-05-03 12:00:00',2,5);
INSERT INTO `webapp`.`topics` (`title`,`date_time`,`category_id`,`user_id`) VALUES ('Cooking with Heisenberg','2024-05-03 12:00:00',3,5);
INSERT INTO `webapp`.`topics` (`title`,`date_time`,`category_id`,`user_id`) VALUES ('F1 Miami GP Sprint','2024-05-04 10:00:00',2,5);
INSERT INTO `webapp`.`topics` (`title`,`date_time`,`category_id`,`user_id`) VALUES ('F1 Miami GP Quali','2024-05-04 12:00:00',2,5);
INSERT INTO `webapp`.`topics` (`title`,`date_time`,`category_id`,`user_id`) VALUES ('F1 Miami GP ','2024-05-05 12:00:00',2,5);


INSERT INTO `webapp`.`messages` (`text`,`timestamp`,`sender_id`,`recipient_id`) VALUES ('Example message','2024-05-03 10:00:00', 2,7);
INSERT INTO `webapp`.`messages` (`text`,`timestamp`,`sender_id`,`recipient_id`) VALUES ('Another message','2024-05-03 10:00:00', 2,7);
INSERT INTO `webapp`.`messages` (`text`,`timestamp`,`sender_id`,`recipient_id`) VALUES ('Last example','2024-05-03 10:00:00', 3,2);


INSERT INTO `webapp`.`replies` (`text`,`date_time`,`topic_id`,`user_id`) VALUES ('Ferrari fans are crying again.','2024-05-03 12:00:00',1,5);
INSERT INTO `webapp`.`replies` (`text`,`date_time`,`topic_id`,`user_id`) VALUES ('Max Pole - Sprint Quali','2024-05-03 17:00:00',2,4);
INSERT INTO `webapp`.`replies` (`text`,`date_time`,`topic_id`,`user_id`) VALUES ('Max Vestappen wins the sprint race.','2024-05-04 11:00:00',3,4);
INSERT INTO `webapp`.`replies` (`text`,`date_time`,`topic_id`,`user_id`) VALUES ('Daniel Ricciardo P4 and points for the RB pilot.','2024-05-04 11:10:00',3,5);
INSERT INTO `webapp`.`replies` (`text`,`date_time`,`topic_id`,`user_id`) VALUES ('Lando Norris first victory in F1 with the McLaren team.','2024-05-05 17:00:00',5,4);