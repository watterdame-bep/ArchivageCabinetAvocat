"""
Service JSReport pour gérer les appels à JSReport de manière centralisée
"""
import requests
import logging
import base64
import os
from django.conf import settings
from django.http import HttpResponse
from typing import Dict, Any, Optional
import json

logger = logging.getLogger(__name__)

class JSReportService:
    """
    Service centralisé pour gérer les appels à JSReport
    """
    
    def __init__(self):
        self.base_url = getattr(settings, 'JSREPORT_URL', 'http://localhost:5488')
        self.username = getattr(settings, 'JSREPORT_USERNAME', None)
        self.password = getattr(settings, 'JSREPORT_PASSWORD', None)
        self.timeout = getattr(settings, 'JSREPORT_TIMEOUT', 120)  # 2 minutes au lieu de 60s
        self.api_url = f"{self.base_url}/api/report"
        
    def test_connection(self) -> bool:
        """
        Teste la connexion au service JSReport
        """
        try:
            # Test simple avec un ping vers l'API
            test_url = f"{self.base_url}/api/ping"
            headers = self._get_auth_headers()
            
            response = requests.get(test_url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.info(f"✅ Connexion JSReport réussie: {self.base_url}")
                return True
            else:
                logger.warning(f"⚠️ JSReport répond mais avec le code: {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Erreur de connexion JSReport ({self.base_url}): {str(e)}")
            return False
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """
        Génère les headers d'authentification pour JSReport
        """
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/pdf'
        }
        
        if self.username and self.password:
            # Authentification Basic
            credentials = f"{self.username}:{self.password}"
            encoded_credentials = base64.b64encode(credentials.encode()).decode()
            headers['Authorization'] = f'Basic {encoded_credentials}'
            
        return headers
    
    def generate_pdf(self, template_name: str, data: Dict[str, Any], 
                    options: Optional[Dict[str, Any]] = None) -> Optional[bytes]:
        """
        Génère un PDF via JSReport
        
        Args:
            template_name: Nom du template JSReport
            data: Données à injecter dans le template
            options: Options supplémentaires pour JSReport
            
        Returns:
            bytes: Contenu du PDF généré ou None en cas d'erreur
        """
        try:
            # Préparer le payload
            payload = {
                "template": {
                    "name": template_name
                },
                "data": data
            }
            
            # Ajouter les options si fournies
            if options:
                payload["options"] = options
                
            # Préparer les headers
            headers = self._get_auth_headers()
            
            logger.info(f"Génération PDF avec template: {template_name}")
            logger.debug(f"URL JSReport: {self.api_url}")
            
            # Appel à JSReport
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            logger.info(f"PDF généré avec succès. Taille: {len(response.content)} bytes")
            return response.content
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout lors de la génération du PDF (template: {template_name})")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Impossible de se connecter à JSReport: {self.base_url}")
            return None
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erreur HTTP JSReport: {e.response.status_code} - {e.response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la génération PDF: {str(e)}")
            return None
    
    def generate_pdf_response(self, template_name: str, data: Dict[str, Any], 
                            filename: str = "document.pdf",
                            options: Optional[Dict[str, Any]] = None,
                            disposition: str = "attachment") -> HttpResponse:
        """
        Génère un PDF et retourne une HttpResponse Django
        
        Args:
            template_name: Nom du template JSReport
            data: Données à injecter dans le template
            filename: Nom du fichier PDF
            options: Options supplémentaires pour JSReport
            disposition: "attachment" pour télécharger, "inline" pour afficher dans le navigateur
            
        Returns:
            HttpResponse: Réponse HTTP avec le PDF ou message d'erreur
        """
        pdf_content = self.generate_pdf(template_name, data, options)
        
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if disposition == "inline":
                response['Content-Disposition'] = f'inline; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            return HttpResponse(
                "Erreur lors de la génération du PDF. Veuillez réessayer plus tard.",
                status=500
            )
    
    def test_connection(self) -> bool:
        """
        Teste la connexion à JSReport
        
        Returns:
            bool: True si la connexion fonctionne, False sinon
        """
        try:
            ping_url = f"{self.base_url}/api/ping"
            response = requests.get(ping_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def get_templates(self) -> Optional[list]:
        """
        Récupère la liste des templates disponibles
        
        Returns:
            list: Liste des templates ou None en cas d'erreur
        """
        try:
            templates_url = f"{self.base_url}/odata/templates"
            headers = self._get_auth_headers()
            
            response = requests.get(templates_url, headers=headers, timeout=10)
            response.raise_for_status()
            
            return response.json().get('value', [])
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des templates: {str(e)}")
            return None
    
    def generate_pdf_by_shortid(self, template_shortid: str, data: Dict[str, Any], 
                               options: Optional[Dict[str, Any]] = None) -> Optional[bytes]:
        """
        Génère un PDF via JSReport en utilisant le shortid du template
        
        Args:
            template_shortid: Shortid du template JSReport (ex: "S1xK9Abc")
            data: Données à injecter dans le template
            options: Options supplémentaires pour JSReport
            
        Returns:
            bytes: Contenu du PDF généré ou None en cas d'erreur
        """
        try:
            # Préparer le payload avec shortid
            payload = {
                "template": {
                    "shortid": template_shortid
                },
                "data": data
            }
            
            # Ajouter les options si fournies
            if options:
                payload["options"] = options
                
            # Préparer les headers
            headers = self._get_auth_headers()
            
            logger.info(f"Génération PDF avec shortid: {template_shortid}")
            logger.debug(f"URL JSReport: {self.api_url}")
            
            # Appel à JSReport
            response = requests.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            logger.info(f"PDF généré avec succès. Taille: {len(response.content)} bytes")
            return response.content
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout lors de la génération du PDF (shortid: {template_shortid})")
            return None
            
        except requests.exceptions.ConnectionError:
            logger.error(f"Impossible de se connecter à JSReport: {self.base_url}")
            return None
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"Erreur HTTP JSReport: {e.response.status_code} - {e.response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Erreur inattendue lors de la génération PDF (shortid: {template_shortid}): {str(e)}")
            return None
    
    def generate_pdf_response_by_shortid(self, template_shortid: str, data: Dict[str, Any], 
                                        filename: str = "document.pdf",
                                        options: Optional[Dict[str, Any]] = None,
                                        disposition: str = "attachment") -> HttpResponse:
        """
        Génère un PDF avec shortid et retourne une HttpResponse Django
        
        Args:
            template_shortid: Shortid du template JSReport
            data: Données à injecter dans le template
            filename: Nom du fichier PDF
            options: Options supplémentaires pour JSReport
            disposition: "attachment" pour télécharger, "inline" pour afficher dans le navigateur
            
        Returns:
            HttpResponse: Réponse HTTP avec le PDF ou message d'erreur
        """
        pdf_content = self.generate_pdf_by_shortid(template_shortid, data, options)
        
        if pdf_content:
            response = HttpResponse(pdf_content, content_type='application/pdf')
            if disposition == "inline":
                response['Content-Disposition'] = f'inline; filename="{filename}"'
            else:
                response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
        else:
            return HttpResponse(
                "Erreur lors de la génération du PDF. Veuillez réessayer plus tard.",
                status=500
            )

# Instance globale du service
jsreport_service = JSReportService()

# Fonctions utilitaires pour compatibilité avec le code existant
def generate_pdf_jsreport(template_name: str, data: Dict[str, Any], 
                         filename: str = "document.pdf") -> HttpResponse:
    """
    Fonction utilitaire pour générer un PDF (compatibilité avec l'ancien code)
    """
    return jsreport_service.generate_pdf_response(template_name, data, filename)

def test_jsreport_connection() -> bool:
    """
    Fonction utilitaire pour tester la connexion JSReport
    """
    return jsreport_service.test_connection()