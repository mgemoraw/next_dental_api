-- INSERTING DEFAULT ROLES INTO DATABASE

INSERT INTO role(name) values
('admin'),
('user'),
('secretary'),
('card'),
('triage'),
('nurse');


INSERT INTO users(username, email, password, role_id) values
('user', 'user@example.com', 'sgetme', 1),
('addis', 'user@example.com', '123456', 2),
('nolawit', 'user@example.com', 'sgetme', 2),
('admin', 'admin@example.com', 'admin', 1);
