CREATE TABLE IF NOT EXISTS Patient (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    age INTEGER,
    sex TEXT,
    bmi REAL,
    children INTEGER,
    smoker TEXT CHECK(smoker IN ('yes', 'no')),
    region TEXT,
    charges REAL
);

CREATE TABLE IF NOT EXISTS Médecin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Consultation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    consultation_date DATE,
    reason TEXT,
    FOREIGN KEY (patient_id) REFERENCES Patient(id),
    FOREIGN KEY (doctor_id) REFERENCES Médecin(id)
);

CREATE TABLE IF NOT EXISTS Diagnostique (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    consultation_id INTEGER,
    diagnostic_description TEXT,
    diagnosis_date DATE,
    FOREIGN KEY (consultation_id) REFERENCES Consultation(id)
);
