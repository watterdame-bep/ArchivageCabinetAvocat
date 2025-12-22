module.exports = {
  // Configuration du port pour Railway
  httpPort: process.env.PORT || 5488,
  
  // Configuration d'authentification
  authentication: {
    enabled: true,
    admin: {
      username: process.env.JSREPORT_USERNAME || 'admin',
      password: process.env.JSREPORT_PASSWORD || 'admin123'
    },
    cookieSession: {
      secret: process.env.JSREPORT_COOKIE_SECRET || 'default-secret'
    }
  },
  
  // Configuration de stockage (filesystem)
  store: {
    provider: 'fs'
  },
  
  // Configuration de stockage des blobs
  blobStorage: {
    provider: 'fs'
  },
  
  // Configuration des workers pour Railway
  workers: {
    numberOfWorkers: 2,
    timeout: 120000
  },
  
  // Configuration de sécurité
  trustUserCode: false,
  allowLocalFilesAccess: false,
  
  // Configuration pour la production
  logger: {
    console: {
      transport: 'console',
      level: 'info'
    }
  },
  
  // Extensions à charger
  extensions: {
    'authentication': {
      enabled: true
    },
    'fs-store': {
      enabled: true
    }
  }
};