CREATE DATABASE Fitness_Center_DB;

CREATE TABLE Members(
	id INT PRIMARY KEY auto_increment,
    name VARCHAR(255) NOT NULL,
	age INT NULL);
    
CREATE TABLE WorkoutSessions (
    session_id INT PRIMARY KEY auto_increment,
    member_id INT,
    session_date DATE NOT NULL,
    session_time VARCHAR(50) NOT NULL,
    activity VARCHAR(255) NULL,
    FOREIGN KEY (member_id) REFERENCES Members(id)
);

select * from members;

select * from workoutsessions;