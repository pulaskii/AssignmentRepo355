INSERT INTO users (Email, First_Name, Last_Name, PatientOrProvider, PasswordHash)

VALUES  ('bob@bob.com', 'Bobf', 'Bobl', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO'),  
        ('sally@sally.com', 'Sallyf', 'Sallyl', 'provider', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO'),
        ('jimothy@jimothy.com', 'jimothyf', 'jimmothyl', 'patient', '$2b$12$Vam60GL5xHEvpq/6EfMINOByfVe/7.tBwWBY/jhIPgroXT28yxUmO');



INSERT INTO accessMap (connectionUID, doctor, patient)

VALUES  ('1', 'sally@sally.com','bob@bob.com'),
        ('2','sally@sally.com','jimothy@jimothy.com');

