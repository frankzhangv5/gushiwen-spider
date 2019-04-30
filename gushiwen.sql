DROP DATABASE gushiwen;
CREATE DATABASE gushiwen DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gushiwen;

DROP TABLE poem;
DROP TABLE poet;


CREATE TABLE poem(
    id int unsigned NOT NULL AUTO_INCREMENT,
    poem_url varchar(300) NOT NULL,
    poem_name varchar(50) NOT NULL,
    poem_dynasty varchar(50) NOT NULL,
    poem_content mediumtext NOT NULL,
    poem_label varchar(30) DEFAULT NULL,
    like_count varchar(20) DEFAULT NULL,
    translation mediumtext DEFAULT NULL,
    annotation mediumtext DEFAULT NULL,
    appreciation mediumtext DEFAULT NULL,
    poet_name varchar(50) DEFAULT NULL,
    poet_bio mediumtext DEFAULT NULL,
    poet_url varchar(300) DEFAULT NULL,
    primary key(id),
    KEY `poem_name` (`poem_name`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;


CREATE TABLE poet(
    id int unsigned NOT NULL AUTO_INCREMENT,
    poet_url varchar(300) NOT NULL,
    poet_name varchar(50) DEFAULT NULL,
    poet_bio mediumtext DEFAULT NULL,
    like_count varchar(20) DEFAULT NULL,
    others mediumtext DEFAULT NULL,
    primary key(id),
    KEY `poet_name` (`poet_name`)
)ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
