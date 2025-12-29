FROM jsreport/jsreport:4.7.0

USER root

# Installer Google Chrome avec toutes les dépendances
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxss1 \
    --no-install-recommends

# Ajouter la clé GPG de Google et installer Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# Variables d'environnement pour Puppeteer
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/google-chrome-stable
ENV PUPPETEER_ARGS="--no-sandbox --disable-setuid-sandbox"
ENV PUPPETEER_CACHE_DIR=/app/.puppeteer-cache

# Créer le cache Puppeteer accessible
RUN mkdir -p /app/.puppeteer-cache && chown -R jsreport:jsreport /app/.puppeteer-cache

# Copier la configuration JSReport
COPY jsreport.config.json /app/jsreport.config.json

# Copier le fichier d'export des templates
COPY export.jsrexport /app/export.jsrexport

# Copier le script de démarrage
COPY start-jsreport.sh /app/start-jsreport.sh

# Rendre le script exécutable
RUN chmod +x /app/start-jsreport.sh

# Changer les permissions pour l'utilisateur jsreport
RUN chown -R jsreport:jsreport /app

USER jsreport

# Exposer le port
EXPOSE 5488

# Utiliser le script de démarrage au lieu de la commande par défaut
CMD ["/app/start-jsreport.sh"]