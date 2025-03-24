### Patient
| Attribut               | Type     | Clé         |
|------------------------|----------|-------------|
| id                     | Int      | PK          |
| name                   | Varchar  |             |
| surname                | Varchar  |             |
| age                    | Int      |             |
| sex                    | Int      | FK (Sexe)   |
| bmi                    | Float    |             |
| children               | Int      |             |
| smoker                 | Int      | FK (Fumeur) |
| region                 | Int      | FK (Région) |
| charges                | Float    |             |

### Sexe
| Attribut               | Type     | Clé         |
|------------------------|----------|-------------|
| id_sex                 | Int      | PK          |
| sexe                   | Varchar  |             |

### Fumeur
| Attribut               | Type     | Clé         |
|------------------------|----------|-------------|
| id_smoker              | Int      | PK          |
| fumeur                 | Varchar  |             |

### Région
| Attribut               | Type     | Clé         |
|------------------------|----------|-------------|
| id_region              | Int      | PK          |
| region                 | Varchar  |             |