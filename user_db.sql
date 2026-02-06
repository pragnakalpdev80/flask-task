CREATE TABLE IF NOT EXISTS registration_details (
	registration_id SERIAL PRIMARY KEY,
    first_name VARCHAR (30) NOT NULL,
    last_name VARCHAR (30) NOT NULL,
    email VARCHAR (30) UNIQUE NOT NULL,
    password VARCHAR (256) NOT NULL,
    address VARCHAR (500) NOT NULL,
    hobbies VARCHAR (50) NOT NULL,
    gender VARCHAR (50) NOT NULL
);