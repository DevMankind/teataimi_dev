-- Create admin account in teataimi database
-- Run this SQL in your MySQL client or phpMyAdmin

INSERT INTO users (name, email, phone, password, role, address, created_at) 
VALUES ('Admin User', 'admin@teataimi.com', '0000000000', 'admin123', 'Admin', 'Admin Office', NOW());

-- Verify the account was created:
-- SELECT * FROM users WHERE email='admin@teataimi.com';
