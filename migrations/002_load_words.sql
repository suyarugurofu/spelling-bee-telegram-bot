INSERT INTO words (word, initial_level) VALUES 
('cat', 1), ('dog', 1), ('sun', 1), ('run', 1), ('hat', 1),
('cup', 1), ('pen', 1), ('bed', 1), ('red', 1), ('big', 1),
('map', 1), ('car', 1), ('box', 1), ('leg', 1), ('eye', 1),
('arm', 1), ('lip', 1), ('fan', 1), ('jam', 1), ('key', 1),
('milk', 1), ('book', 1), ('hand', 1), ('door', 1), ('tree', 1),
('bird', 1), ('fish', 1), ('jump', 1), ('play', 1), ('sing', 1),
('rain', 1), ('snow', 1), ('star', 1), ('moon', 1), ('ship', 1),
('frog', 1), ('duck', 1), ('bear', 1), ('lion', 1), ('wolf', 1)
ON CONFLICT (word) DO NOTHING;

INSERT INTO words (word, initial_level) VALUES
('apple', 2), ('chair', 2), ('water', 2), ('light', 2), ('night', 2),
('brush', 2), ('clock', 2), ('dance', 2), ('eagle', 2), ('flame', 2),
('grape', 2), ('horse', 2), ('knife', 2), ('lemon', 2), ('music', 2),
('ocean', 2), ('piano', 2), ('queen', 2), ('robot', 2), ('snake', 2),
('tiger', 2), ('umbrella', 2), ('voice', 2), ('whale', 2), ('zebra', 2),
('butter', 2), ('candle', 2), ('dragon', 2), ('engine', 2), ('flower', 2),
('guitar', 2), ('hammer', 2), ('island', 2), ('jungle', 2), ('kitten', 2),
('ladder', 2), ('mirror', 2), ('number', 2), ('orange', 2), ('pencil', 2)
ON CONFLICT (word) DO NOTHING;

INSERT INTO words (word, initial_level) VALUES
('beautiful', 3), ('necessary', 3), ('separate', 3), ('definitely', 3), ('accommodate', 3),
('embarrass', 3), ('occurrence', 3), ('privilege', 3), ('recommend', 3), ('harass', 3),
('conscience', 3), ('rhythm', 3), ('schedule', 3), ('foreign', 3), ('weird', 3),
('height', 3), ('receipt', 3), ('colonel', 3), ('yacht', 3), ('queue', 3)
ON CONFLICT (word) DO NOTHING;
