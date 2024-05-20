-- Create a new database with UTF-8 encoding
-- CREATE DATABASE psycotest WITH ENCODING 'UTF8';

-- Table: users

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    users_name VARCHAR(255),
    email VARCHAR(100),
    location_of_user VARCHAR(255),
    profile_url TEXT NOT NULL UNIQUE,
    estimated_net_worth DECIMAL(12, 2),
    estimated_age INT
);

-- Table: education

CREATE TABLE education(
    education_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    school_name VARCHAR(255),
    degree VARCHAR(255),
    grade VARCHAR(10),
    start_date DATE,
    end_date DATE,
    description_of_education TEXT,
    activities_and_societies TEXT
);

-- Table: work_experience

CREATE TABLE work_experience(
    experience_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    job_title VARCHAR(255),
    company VARCHAR(255),
    location_of_job VARCHAR(255),
    start_date DATE,
    end_date DATE,
    work_description TEXT,
    estimated_net_earnings DECIMAL(10, 2)
);

-- Table: skills

CREATE TABLE skills(
    skill_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    skill_name VARCHAR(255),
    endorsement_count INT
);

-- Table: bots
CREATE TABLE bots(
    bot_id SERIAL PRIMARY KEY,
    bot_first_name VARCHAR(100),
    bot_last_name VARCHAR(100),
    bot_email_header VARCHAR(255),
    bot_email VARCHAR(255),
    bot_email_password VARCHAR(50),
    phone VARCHAR(20),
    status_ VARCHAR(20)
);

-- Table: phone_numbers

CREATE TABLE phone_numbers(
    phone_number_id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) UNIQUE,
    assigned_to INTEGER REFERENCES Bots(bot_id)
);

-- Table cookies

CREATE TABLE cookies(
    cookie_id SERIAL PRIMARY KEY,
    bot_id INTEGER REFERENCES Bots(bot_id),
    website VARCHAR(255),
    cookie JSONB
);

CREATE TABLE salaries(
    salary_id SERIAL PRIMARY KEY,
    job_title VARCHAR(255),
    salary DECIMAL(12, 2),
    location VARCHAR(255),
    company VARCHAR(255),
    date DATE
);

INSERT INTO bots(bot_first_name, bot_last_name, bot_email, bot_email_password) 
VALUES('Danny', 'Brown', 'dbrown6@umbc.edu', 'Sp@ceghost12');

-- \i 'C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//scrapers//src//database//initialize.sql';
-- \i 'C:/Users/Daniel.Brown/Desktop/PreferredPartnerDB/src/database/initialize.sql'