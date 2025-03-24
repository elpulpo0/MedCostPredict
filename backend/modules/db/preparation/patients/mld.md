# MLD - Modèle Logique de Données

## Tables

```sql
CREATE TABLE Patient (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    surname VARCHAR(255),
    age INT,
    sex INT,
    bmi FLOAT,
    children INT,
    smoker INT,
    region INT,
    charges FLOAT,
    FOREIGN KEY (sex) REFERENCES Sexe(id_sex),
    FOREIGN KEY (smoker) REFERENCES Fumeur(id_smoker),
    FOREIGN KEY (region) REFERENCES Region(id_region)
);
CREATE TABLE Sexe (
    id_sex INT PRIMARY KEY,
    sexe VARCHAR(10) -- Homme ou Femme
);
CREATE TABLE Fumeur (
    id_smoker INT PRIMARY KEY,
    fumeur VARCHAR(3) -- Oui ou Non
);
CREATE TABLE Region (
    id_region INT PRIMARY KEY,
    region VARCHAR(255) -- Nom de la région
);
```
## Relations

- Patient → sex → Sexe : Chaque patient est associé à un sexe.
- Patient → smoker → Fumeur : Chaque patient a un statut de fumeur.
- Patient → region → Région : Chaque patient est lié à une région.