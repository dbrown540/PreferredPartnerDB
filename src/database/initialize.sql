-- Table: users

CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    users_name VARCHAR(255),
    email VARCHAR(100),
    location_of_user VARCHAR(255),
    profile_url TEXT NOT NULL
);

-- Table: education

CREATE TABLE education(
    education_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    degree VARCHAR(255),
    school_name VARCHAR(255),
    graduation_month INT,
    gradiation_year INT
);

-- Table: work_experience

CREATE TABLE work_experience(
    experience_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users(user_id),
    title VARCHAR(255),
    company VARCHAR(255),
    location_of_job VARCHAR(255),
    start_month INT,
    start_year INT,
    end_month INT,
    end_year INT,
    description_of_experience TEXT
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
    phone_number VARCHAR(20)
);

-- Table proxies

CREATE TABLE proxies(
    proxy_id SERIAL PRIMARY KEY,
    proxy VARCHAR(100)
);
INSERT INTO bots (bot_first_name, bot_last_name, bot_email_header, bot_email, bot_email_password, phone, status_)
        VALUES('Daniel', 'Brown', 'dbrown6', 'dbrown6@umbc.edu', 'Sp@ceghost12', '2403445937', 'OPERATIONAL');
INSERT INTO bots (bot_first_name, bot_last_name, bot_email_header, bot_email, bot_email_password, phone, status_)
        VALUES ('Francis', 'Wolf', 'francis_wolf91966', 'francis_wolf91966@proton.me', 'iqTza8fLOYBe', '3392731615', 'TBD');

INSERT INTO users (profile_url)
        VALUES ('https://www.linkedin.com/in/douglas-brown-6850a052/');

-- \i 'C://Users//Doug Brown//Desktop//Dannys Stuff//Job//PreferredPartnerDB//src//database//initialize.sql';
-- \i 'C:/Users/Daniel.Brown/Desktop/PreferredPartnerDB/src/database/initialize.sql'