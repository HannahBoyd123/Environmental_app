-- create Database user_login_details;
-- USE user_login_details;

-- CREATE TABLE `user_account` (
-- 	`id` int NOT NULL AUTO_INCREMENT,
--   	`First_Name` varchar(25) NOT NULL,
--   	`password` varchar(60) NOT NULL,
--   	`email` varchar(60) NOT NULL,
--     PRIMARY KEY (`id`)
-- );

-- create saved_searches table

-- USE user_login_details;

-- CREATE TABLE saved_searches(
-- id int NOT NULL, 
-- City varchar(25),
-- FOREIGN KEY (id) REFERENCES user_account(id)
-- );

-- CREATE procedure to add searches to database

-- SET GLOBAL log_bin_trust_function_creators = 1;


-- SET DELIMITER = //

-- DELIMITER //

-- CREATE PROCEDURE InsertCity (Checkid int, InsertCity varchar(25))

-- BEGIN

-- SET @checkRecord = (SELECT COUNT(id) from saved_searches where id = Checkid and City = InsertCity);
-- IF @checkRecord = 0
-- THEN INSERT INTO saved_searches(id, City) VALUES(Checkid, InsertCity);

-- ELSE IF @checkRecord > 0
-- THEN
-- SET @checkCity = (SELECT COUNT(ID) from saved_searches where id = Checkid and City != InsertCity);
-- IF @checkCity = 1
-- THEN UPDATE saved_searches SET City = InsertCity WHERE id = Checkid;

-- END IF;

-- END IF;
--  
-- END IF; 
--  
--  END; //

-- SET DELIMITER = ;


-- Procedure for creating log table for users--

-- SET DELIMITER = //

-- DELIMITER //

-- CREATE PROCEDURE CreateWeatherLog(Checkid int)

-- BEGIN

-- SET @createTab=CONCAT("CREATE TABLE ","Weather_", Checkid, "(id int NOT NULL, 
-- Country_Code varchar(4),
-- City varchar(25),
-- Temp°C decimal(18,2),
-- Pressure int,
-- Humidity int,
-- Date_time datetime NOT NULL,
-- indx int NOT NULL AUTO_INCREMENT,
-- PRIMARY KEY (indx),
-- FOREIGN KEY (id) REFERENCES user_account(id)
-- )");

-- PREPARE stmtCreate FROM @createTab;
-- EXECUTE stmtCreate;
-- DEALLOCATE PREPARE stmtCreate;

-- END; //

-- SET DELIMITER = ;

-- create procedure to insert weather data in table--

-- SET DELIMITER = //

-- DELIMITER //


-- CREATE PROCEDURE InsertWeatherLog(Checkid int, CountryCode varchar(4), CityName varchar(25), Temperature decimal, press int, humidity int)

-- BEGIN 

-- SET @insertTab=CONCAT("INSERT INTO ", "weather_", Checkid, "(id, Country_Code, City, Temp°C, Pressure, Humidity, Date_Time) VALUES(", Checkid, ", '", CountryCode, "', '", CityName, "', ", Temperature, ", ", press, ", ", humidity, ", ", "now()", ")");

-- PREPARE stmtInsert FROM @insertTab;
-- EXECUTE stmtInsert;
-- DEALLOCATE PREPARE stmtInsert;

-- END; //

-- SET DELIMITER = ;

select * from user_account