CREATE DATABASE IF NOT EXISTS hr_ai;
USE hr_ai;

-- Create candidates table with constraints
CREATE TABLE IF NOT EXISTS candidates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL CHECK (LENGTH(name) >= 2),
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    city VARCHAR(100),
    birthdate VARCHAR(50),
    education TEXT,
    job_history TEXT,
    skills JSON,
    score INT CHECK (score >= 0 AND score <= 10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT unique_email UNIQUE (email),
    INDEX idx_name (name),
    INDEX idx_email (email),
    INDEX idx_score (score)
);

-- Create a trigger to validate email format
DELIMITER //
CREATE TRIGGER validate_email_before_insert
BEFORE INSERT ON candidates
FOR EACH ROW
BEGIN
    IF NEW.email NOT REGEXP '^[^@]+@[^@]+\\.[^@]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
END //
DELIMITER ;

-- Create a trigger to validate email format on update
DELIMITER //
CREATE TRIGGER validate_email_before_update
BEFORE UPDATE ON candidates
FOR EACH ROW
BEGIN
    IF NEW.email NOT REGEXP '^[^@]+@[^@]+\\.[^@]+$' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Invalid email format';
    END IF;
END //
DELIMITER ;
