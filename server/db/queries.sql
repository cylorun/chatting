CREATE TABLE users(user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(255),
                    password VARCHAR(255), 
                    email VARCHAR(255),
                    date INTEGER
                    );

CREATE TABLE messages(message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER, -- AKA message owner
                        channel_id INTEGER,
                        content TEXT,
                        date INTEGER);
                        









INSERT INTO users (name, email, password) VALUES 
('Sophia', 'sophia@example.com', 'password123'),
('Liam', 'liam@example.com', 'liamsPass456'),
('Olivia', 'olivia@example.com', 'oliviaPassword'),
('Noah', 'noah@example.com', 'noahSecure321'),
('Ava', 'ava@example.com', 'avasSecret'),
('William', 'william@example.com', 'william123'),
('Isabella', 'isabella@example.com', 'isabellaPass'),
('James', 'james@example.com', 'jamesPassword'),
('Emma', 'emma@example.com', 'emma456'),
('Lucas', 'lucas@example.com', 'lucasSecure'),
('Michael', 'michael@example.com', 'michaelsPassword'),
('Mia', 'mia@example.com', 'miaSecure123'),
('Benjamin', 'benjamin@example.com', 'benjaminPass'),
('Charlotte', 'charlotte@example.com', 'charlotte123'),
('Ethan', 'ethan@example.com', 'ethanSecure'),
('Amelia', 'amelia@example.com', 'ameliaPass321');


-- Inserts for Channel 1
INSERT INTO messages (user_id, channel_id, content) VALUES
(1, 1, 'Hello, this is user 1 in Channel 1!'),
(5, 1, 'User 5 says something in Channel 1.'),
(10, 1, 'Message from user 10 in Channel 1.');

-- Inserts for Channel 2
INSERT INTO messages (user_id, channel_id, content) VALUES
(2, 2, 'Greetings from user 2 in Channel 2!'),
(8, 2, 'User 8 posted in Channel 2.'),
(15, 2, 'Message by user 15 in Channel 2.');

-- Inserts for Channel 3
INSERT INTO messages (user_id, channel_id, content) VALUES
(3, 3, 'User 3 reporting in Channel 3!'),
(12, 3, 'Message from user 12 in Channel 3.'),
(18, 3, 'Hello, it''s user 18 in Channel 3.');
