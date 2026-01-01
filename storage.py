"""
Configuration de stockage personnalisée pour Railway
"""
from whitenoise.storage import CompressedStaticFilesStorage
import logging

logger = logging.getLogger(__name__)

class RailwayStaticFilesStorage(CompressedStaticFilesStorage):
    """
    Stockage personnalisé qui ignore les fichiers .map manquants
    """
    
    def post_process(self, paths, dry_run=False, **options):
        """
        Post-traitement des fichiers statiques avec gestion des erreurs
        """
        try:
            return super().post_process(paths, dry_run, **options)
        except Exception as e:
            # Log l'erreur mais continue le processus
            logger.warning(f"Erreur lors du post-traitement des fichiers statiques: {e}")
            # Retourner un générateur vide pour éviter l'erreur
            return []
    
    def url(self, name, force=False):
        """
        Générer l'URL avec gestion des fichiers manquants
        """
        try:
            return super().url(name, force)
        except Exception as e:
            logger.warning(f"Fichier statique manquant: {name} - {e}")
            # Retourner l'URL de base pour éviter l'erreur
            return f"{self.base_url}{name}"