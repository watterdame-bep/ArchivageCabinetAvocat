# Utiliser Python 3.11 comme image de base
FROM python:3.11-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances système minimales
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier les requirements et installer les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY . .

# Rendre le script de démarrage exécutable
RUN chmod +x start.sh

# Créer le répertoire staticfiles
RUN mkdir -p staticfiles

# Exposer le port par défaut (Railway utilisera $PORT dynamiquement)
EXPOSE 8000

# Utiliser le script de démarrage
CMD ["./start.sh"]