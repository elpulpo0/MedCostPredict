# Utiliser une image Python de base plus récente
FROM python:3.11-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code de l'application backend dans le conteneur
COPY . ./backend

# Définir le chemin Python pour les imports
ENV PYTHONPATH=/app:$PYTHONPATH

# Commande d'exécution pour lancer l'application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
