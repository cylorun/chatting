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

CREATE TABLE channels(channel_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        date INTEGER,
                        name VARCHAR(255),
                        password VARCHAR(255),
                        user_id INTEGER  --owner
                        );


DROP TABLE channels







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
INSERT INTO messages (user_id, channel_id, content, date) VALUES
(1, 1, 'Hello, this is user 1 in Channel 1!', 1643758800),
(5, 1, 'User 5 says something in Channel 1.', 1643758810),
(10, 1, 'Message from user 10 in Channel 1.', 1643758820),
(7, 1, 'Another message in Channel 1.', 1643758830),
(9, 1, 'User 9 joined Channel 1.', 1643758840),
(14, 1, 'Hello from user 14 in Channel 1.', 1643758850),
(6, 1, 'User 6 posted in Channel 1.', 1643758860),
(11, 1, 'Message by user 11 in Channel 1.', 1643758870),
(4, 1, 'User 4 reporting in Channel 1!', 1643758880),
(16, 1, 'Another message from user 16 in Channel 1.', 1643758890),
(13, 1, 'User 13 posted in Channel 1.', 1643758900),
(20, 1, 'Message by user 20 in Channel 1.', 1643758910),
(2, 1, 'User 2 says hi in Channel 1.', 1643758920),
(19, 1, 'Hello, it''s user 19 in Channel 1.', 1643758930),
(17, 1, 'User 17 reporting in Channel 1.', 1643758940),
(8, 1, 'Message from user 8 in Channel 1.', 1643758950),
(12, 1, 'User 12 says something in Channel 1.', 1643758960),
(15, 1, 'Hello from user 15 in Channel 1.', 1643758970),
(3, 1, 'User 3 posted in Channel 1.', 1643758980),
(18, 1, 'Message by user 18 in Channel 1.', 1643758990),
(21, 1, 'User 21 joined Channel 1.', 1643759000);

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

INSERT INTO channels (date, name, password, user_id) VALUES
(1643758880, 'TEst RoomM OnE', NULL, 12),
(1643738880, 'TEst RoomM DOS','wassy',23),
(1643733380, 'TEst RoomM THRE!!!!!!!!','passy',2);


