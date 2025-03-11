-- Table Sexe
CREATE TABLE Sexe (
    id_sex INT AUTO_INCREMENT PRIMARY KEY,
    sexe VARCHAR(10) NOT NULL -- Homme ou Femme
);

-- Table Fumeur
CREATE TABLE Fumeur (
    id_smoker INT AUTO_INCREMENT PRIMARY KEY,
    fumeur VARCHAR(3) NOT NULL -- Oui ou Non
);

-- Table Region
CREATE TABLE Region (
    id_region INT AUTO_INCREMENT PRIMARY KEY,
    region VARCHAR(255) NOT NULL -- Nom de la région
);

-- Table Patient
CREATE TABLE Patient (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    surname VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    id_sex INT,
    bmi FLOAT,
    children INT,
    smoker INT,
    region INT,
    charges FLOAT,
    FOREIGN KEY (id_sex) REFERENCES Sexe(id_sex),
    FOREIGN KEY (smoker) REFERENCES Fumeur(id_smoker),
    FOREIGN KEY (region) REFERENCES Region(id_region)
);