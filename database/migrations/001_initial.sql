-- database/migrations/001_initial.sql
CREATE TABLE candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(100),
    birthdate DATE,
    education TEXT,
    job_history TEXT,
    skills JSON,
    score TINYINT,
    considerations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);