DELETE FROM Classes;

INSERT INTO Class_types (class_title, type) VALUES ('State', 'select');
INSERT INTO Classes (title, value) VALUES ('State', 'Undefined');
INSERT INTO Classes (title, value) VALUES ('State', 'Prototype');
INSERT INTO Classes (title, value) VALUES ('State', 'Pre-Alpha');
INSERT INTO Classes (title, value) VALUES ('State', 'Alpha');
INSERT INTO Classes (title, value) VALUES ('State', 'Beta');
INSERT INTO Classes (title, value) VALUES ('State', 'Released');

INSERT INTO Class_types (class_title, type) VALUES ('Multiplayability', 'select');
INSERT INTO Classes (title, value) VALUES ('Multiplayability', 'Singleplayer');
INSERT INTO Classes (title, value) VALUES ('Multiplayability', 'Multiplayer');
INSERT INTO Classes (title, value) VALUES ('Multiplayability', 'Multiplayer and Singleplayer');

INSERT INTO Class_types (class_title, type) VALUES ('Desired feedback', 'checkbox');
INSERT INTO Classes (title, value) VALUES ('Desired feedback', 'Game testing');
INSERT INTO Classes (title, value) VALUES ('Desired feedback', 'Debugging');
INSERT INTO Classes (title, value) VALUES ('Desired feedback', 'Development ideas');
INSERT INTO Classes (title, value) VALUES ('Desired feedback', 'Review');
INSERT INTO Classes (title, value) VALUES ('Desired feedback', 'Price & Age feedback');
INSERT INTO Classes (title, value) VALUES ('Desired feedback', 'Other');
