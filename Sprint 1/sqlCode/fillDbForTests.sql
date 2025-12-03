INSERT INTO users (Email, First_Name, Last_Name, PatientOrProvider, PasswordHash)

VALUES  ('bob@bob.com', 'Bobf', 'Bobl', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO'),  
        ('sally@sally.com', 'Sallyf', 'Sallyl', 'provider', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO'),
        ('jimothy@jimothy.com', 'jimothyf', 'jimmothyl', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO');


############################################


INSERT INTO accessMap (connectionUID, doctor, patient)

VALUES  ('1', 'sally@sally.com','bob@bob.com'),
        ('2','sally@sally.com','jimothy@jimothy.com');


###############################################


INSERT INTO accessMap (connectionUID, doctor, patient)
VALUES
('3',  'sally@sally.com', 'user17@example.com'),
('4',  'sally@sally.com', 'user3@example.com'),
('5',  'sally@sally.com', 'user12@example.com'),
('6',  'sally@sally.com', 'user8@example.com'),
('7',  'sally@sally.com', 'user21@example.com'),
('8',  'sally@sally.com', 'user1@example.com'),
('9',  'sally@sally.com', 'user14@example.com'),
('10', 'sally@sally.com', 'user5@example.com'),
('11', 'sally@sally.com', 'user19@example.com'),
('12', 'sally@sally.com', 'user10@example.com');



###############################################


INSERT INTO users 
(Email, First_Name, Last_Name, PatientOrProvider, PasswordHash, Age, Phone_Number,
 Sex, Weight, Height, Medications, Allergies, Active_Problems, Medical_History, 
 Family_History, Date_Updated)
VALUES
('user1@example.com', 'Alice', 'Johnson', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 28, '(123)-111-1111', 'F', '140', '65', 'Ibuprofen', '', '', '', '', '2025-01-01'),

('user2@example.com', 'Bob', 'Smith', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 34, '(123)-111-1112', 'M', '185', '70', '', 'Peanuts', 'Asthma', 'Broken Arm (2012)', 'Heart Disease', '2025-01-02'),

('user3@example.com', 'Carla', 'Perez', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 22, '(123)-111-1113', 'F', '125', '63', 'Zyrtec', 'Pollen', 'Seasonal Allergies', '', '', '2025-01-03'),

('user4@example.com', 'David', 'Nguyen', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 30, '(123)-111-1114', 'M', '170', '69', '', '', '', 'Tonsil Removal', 'Diabetes', '2025-01-04'),

('user5@example.com', 'Emma', 'Brown', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 41, '(123)-111-1115', 'F', '160', '66', 'Metformin', '', 'Type 2 Diabetes', '', 'High Cholesterol', '2025-01-05'),

('user6@example.com', 'Frank', 'Lopez', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 55, '(123)-111-1116', 'M', '200', '72', 'Lisinopril', '', 'Hypertension', '', 'Stroke', '2025-01-06'),

('user7@example.com', 'Grace', 'Miller', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 19, '(123)-111-1117', 'F', '130', '64', '', 'Shellfish', 'Eczema', '', '', '2025-01-07'),

('user8@example.com', 'Henry', 'Wilson', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 47, '(123)-111-1118', 'M', '195', '71', 'Atorvastatin', '', 'High Cholesterol', 'Knee Surgery', 'Heart Disease', '2025-01-08'),

('user9@example.com', 'Ivy', 'Davis', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 26, '(123)-111-1119', 'F', '150', '67', '', 'Gluten', 'Irritable Bowel Syndrome', '', '', '2025-01-09'),

('user10@example.com', 'Jack', 'Moore', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 38, '(123)-111-1120', 'M', '180', '70', 'Omeprazole', '', 'GERD', 'Appendectomy', '', '2025-01-10'),

('user11@example.com', 'Kara', 'Taylor', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 33, '(123)-111-1121', 'F', '155', '66', '', 'Latex', '', '', 'Cancer', '2025-01-11'),

('user12@example.com', 'Leo', 'Anderson', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 24, '(123)-111-1122', 'M', '165', '69', 'Adderall', '', 'ADHD', '', '', '2025-01-12'),

('user13@example.com', 'Mia', 'Thomas', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 29, '(123)-111-1123', 'F', '145', '65', '', '', '', '', 'High Blood Pressure', '2025-01-13'),

('user14@example.com', 'Nate', 'Jackson', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 63, '(123)-111-1124', 'M', '210', '73', 'Warfarin', '', 'Atrial Fibrillation', '', 'Stroke', '2025-01-14'),

('user15@example.com', 'Olivia', 'White', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 51, '(123)-111-1125', 'F', '170', '67', 'Levothyroxine', '', 'Hypothyroidism', '', 'Thyroid Disease', '2025-01-15'),

('user16@example.com', 'Paul', 'Harris', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 45, '(123)-111-1126', 'M', '190', '71', '', 'Bee Stings', '', '', '', '2025-01-16'),

('user17@example.com', 'Quinn', 'Martin', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 36, '(123)-111-1127', 'F', '160', '68', 'Prozac', '', 'Depression', '', 'Anxiety', '2025-01-17'),

('user18@example.com', 'Ryan', 'Thompson', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 20, '(123)-111-1128', 'M', '175', '70', '', '', '', '', '', '2025-01-18'),

('user19@example.com', 'Sara', 'Garcia', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 27, '(123)-111-1129', 'F', '135', '64', 'Birth Control', 'Penicillin', '', '', '', '2025-01-19'),

('user20@example.com', 'Tom', 'Martinez', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 48, '(123)-111-1130', 'M', '185', '70', 'Insulin', '', 'Type 1 Diabetes', '', 'Diabetes', '2025-01-20'),

('user21@example.com', 'Uma', 'Rodriguez', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 32, '(123)-111-1131', 'F', '150', '66', '', 'Cats', 'Asthma', '', 'Asthma', '2025-01-21'),

('user22@example.com', 'Victor', 'Lee', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO',
 44, '(123)-111-1132', 'M', '200', '72', '', '', 'Back Pain', 'Back Surgery', '', '2025-01-22');
