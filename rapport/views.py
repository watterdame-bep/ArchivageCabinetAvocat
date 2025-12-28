from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib import messages
from django.utils import timezone
from Dossier.models import client, dossier
from Agent.models import agent
from Structure.models import Juridiction, ServiceCabinet
from Adresse.models import commune
from django.db import models
import json
import requests
from datetime import date, datetime, timedelta
import logging
import os

# Import optionnel de reportlab pour la génération PDF
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

logger = logging.getLogger(__name__)

@login_required(login_url='Connexion')
def rapport_dashboard(request):
    """
    Dashboard principal des rapports avec statistiques générales
    """
    try:
        # Récupérer les statistiques générales
        user_cabinet = getattr(request.user, 'cabinet', None)
        user_company = getattr(request.user, 'company', None)
        
        # Compter les clients
        if user_cabinet:
            total_clients = client.objects.filter(cabinet=user_cabinet).count()
        else:
            total_clients = client.objects.count()
        
        # Compter les agents
        if user_company:
            total_agents = agent.objects.filter(company=user_company).count()
        else:
            total_agents = agent.objects.count()
        
        # Compter les dossiers
        if user_cabinet:
            total_dossiers = dossier.objects.filter(cabinet=user_cabinet).count()
        else:
            total_dossiers = dossier.objects.count()
        
        # Compter les juridictions
        if user_cabinet:
            total_juridictions = Juridiction.objects.filter(cabinet=user_cabinet).count()
        else:
            total_juridictions = Juridiction.objects.count()
        
        # Compter les communes
        if user_cabinet:
            total_communes = commune.objects.filter(cabinet=user_cabinet).count()
        else:
            total_communes = commune.objects.count()
        
        context = {
            'total_clients': total_clients,
            'total_agents': total_agents,
            'total_dossiers': total_dossiers,
            'total_juridictions': total_juridictions,
            'total_communes': total_communes,
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_dashboard.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_dashboard: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def track_rapport_generation(user, type_rapport, sujet, format_rapport='pdf'):
    """
    Utilitaire pour suivre la génération de rapports (peut être étendu avec une base de données)
    """
    try:
        # Pour l'instant, on peut juste logger
        logger.info(f"Rapport généré - User: {user.username}, Type: {type_rapport}, Sujet: {sujet}, Format: {format_rapport}")
        
        # TODO: Ajouter à une table de suivi des rapports si nécessaire
        # RapportHistory.objects.create(
        #     user=user,
        #     type_rapport=type_rapport,
        #     sujet=sujet,
        #     format_rapport=format_rapport,
        #     date_generation=datetime.now()
        # )
        
    except Exception as e:
        logger.error(f"Erreur tracking rapport: {str(e)}")

@login_required(login_url='Connexion')
def rapport_juridiction_interface(request):
    """
    Interface pour afficher la liste des juridictions et générer leurs rapports
    """
    try:
        # Récupérer les juridictions du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            juridictions = Juridiction.objects.filter(cabinet=user_cabinet).order_by('nom')
        else:
            juridictions = Juridiction.objects.all().order_by('nom')
        
        # Calculer les statistiques pour chaque juridiction
        juridictions_data = []
        for jur in juridictions:
            juridictions_data.append({
                'juridiction': jur,
                'lieu_nom': jur.lieu.nom if jur.lieu else 'Non défini'
            })
        
        context = {
            'juridictions_data': juridictions_data,
            'total_juridictions': len(juridictions_data),
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_juridiction.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_juridiction_interface: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def rapport_commune_interface(request):
    """
    Interface pour afficher la liste des communes et générer leurs rapports
    """
    try:
        # Récupérer les communes du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            communes = commune.objects.filter(cabinet=user_cabinet).order_by('nom')
        else:
            communes = commune.objects.all().order_by('nom')
        
        # Calculer les statistiques pour chaque commune
        communes_data = []
        for com in communes:
            communes_data.append({
                'commune': com,
                'date_ouverture': com.date_ouverture
            })
        
        context = {
            'communes_data': communes_data,
            'total_communes': len(communes_data),
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_commune.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_commune_interface: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
@login_required(login_url='Connexion')
def rapport_agent_interface(request):
    """
    Interface pour afficher la liste des agents et générer leurs rapports
    """
    try:
        # Récupérer les agents du cabinet
        user_company = getattr(request.user, 'company', None)
        
        if user_company:
            agents = agent.objects.filter(company=user_company).order_by('nom', 'prenom')
        else:
            agents = agent.objects.all().order_by('nom', 'prenom')
        
        # Calculer les statistiques pour chaque agent
        agents_data = []
        for ag in agents:
            # Compter les dossiers assignés à cet agent
            from Dossier.models import AvocatDossier
            dossiers_assignes = AvocatDossier.objects.filter(avocat=ag).count()
            dossiers_principaux = AvocatDossier.objects.filter(avocat=ag, role='Principal').count()
            
            # Calculer les activités récentes (si le système d'activités est activé)
            activites_recentes = 0
            try:
                from Agent.models_activity import ActivityLog
                from datetime import timedelta
                date_limite = datetime.now() - timedelta(days=30)
                # Trouver l'utilisateur associé à cet agent
                user_agent = None
                try:
                    from Authentification.models import CompteUtilisateur
                    user_agent = CompteUtilisateur.objects.get(agent=ag)
                    activites_recentes = ActivityLog.objects.filter(
                        user=user_agent,
                        timestamp__gte=date_limite
                    ).count()
                except CompteUtilisateur.DoesNotExist:
                    pass
            except:
                pass
            
            # Déterminer le statut
            statut_display = 'Inactif'
            try:
                from Authentification.models import CompteUtilisateur
                user_agent = CompteUtilisateur.objects.get(agent=ag)
                statut_display = 'Actif' if user_agent.is_active else 'Inactif'
            except CompteUtilisateur.DoesNotExist:
                statut_display = 'Pas de compte'
            
            agents_data.append({
                'agent': ag,
                'dossiers_assignes': dossiers_assignes,
                'dossiers_principaux': dossiers_principaux,
                'activites_recentes': activites_recentes,
                'statut_display': statut_display
            })
        
        context = {
            'agents_data': agents_data,
            'total_agents': len(agents_data),
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_agent.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_agent_interface: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def rapport_client_interface(request):
    """
    Interface pour générer les rapports clients
    """
    try:
        # Récupérer les clients du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            clients = client.objects.filter(cabinet=user_cabinet).order_by('nom', 'prenom')
        else:
            clients = client.objects.all().order_by('nom', 'prenom')
        
        # Calculer des statistiques supplémentaires pour chaque client
        clients_data = []
        for c in clients:
            # Compter les dossiers du client
            from Dossier.models import dossier
            dossiers_client = dossier.objects.filter(client=c)
            total_dossiers = dossiers_client.count()
            dossiers_ouverts = dossiers_client.filter(statut_dossier='Ouvert').count()
            dossiers_clotures = dossiers_client.filter(statut_dossier='Clôturé').count()
            dossiers_gagnes = dossiers_client.filter(score='gagne').count()
            
            # Calculer les montants
            montant_total_fc = sum(d.montant_fc_enreg or 0 for d in dossiers_client)
            montant_total_usd = sum(d.montant_dollars_enreg or 0 for d in dossiers_client)
            
            clients_data.append({
                'client': c,
                'total_dossiers': total_dossiers,
                'dossiers_ouverts': dossiers_ouverts,
                'dossiers_clotures': dossiers_clotures,
                'dossiers_gagnes': dossiers_gagnes,
                'montant_total_fc': montant_total_fc,
                'montant_total_usd': montant_total_usd,
                'derniere_activite': dossiers_client.order_by('-date_ouverture').first().date_ouverture if dossiers_client.exists() else None
            })
        
        context = {
            'clients': clients,
            'clients_data': clients_data,
            'total_clients': clients.count(),
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_client.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_client_interface: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def generer_rapport_client(request):
    """
    Génère un rapport client via JSReport
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        # Récupérer les paramètres
        client_id = request.POST.get('client_id')
        type_rapport = request.POST.get('type_rapport', 'complet')
        format_rapport = request.POST.get('format', 'pdf')
        
        if not client_id:
            return JsonResponse({'error': 'Client non spécifié'}, status=400)
        
        # Récupérer le client
        client_obj = get_object_or_404(client, id=client_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and client_obj.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Préparer les données pour le rapport
        rapport_data = preparer_donnees_rapport_client(client_obj, type_rapport, request)
        
        # Générer le rapport via JSReport
        rapport_url = generer_rapport_jsreport(rapport_data, type_rapport, format_rapport)
        
        if rapport_url:
            return JsonResponse({
                'success': True,
                'rapport_url': rapport_url,
                'client_nom': f"{client_obj.nom} {client_obj.prenom}",
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'jsreport'
            })
        else:
            # Mode démo si JSReport n'est pas disponible
            demo_url = generer_rapport_demo(rapport_data, type_rapport, format_rapport)
            return JsonResponse({
                'success': True,
                'rapport_url': demo_url,
                'client_nom': f"{client_obj.nom} {client_obj.prenom}",
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'demo',
                'message': 'Rapport généré en mode démo. Configurez JSReport pour la génération complète.'
            })
            
    except Exception as e:
        logger.error(f"Erreur génération rapport client: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

def preparer_donnees_rapport_client(client_obj, type_rapport, request):
    """
    Prépare les données pour le rapport client (format compatible JSReport Handlebars)
    """
    # Fonctions utilitaires (même pattern que dans paiement/views.py)
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Récupérer les dossiers du client
    dossiers_client = dossier.objects.filter(client=client_obj).order_by('-date_ouverture')
    
    dossiers_data = []
    total_fc = 0
    total_usd = 0
    dossiers_gagnes = 0
    dossiers_perdus = 0
    dossiers_ouverts = 0
    dossiers_clotures = 0
    
    for d in dossiers_client:
        # Récupérer l'avocat principal
        from Dossier.models import AvocatDossier
        avocat_principal = AvocatDossier.objects.filter(dossier=d, role='Principal').first()
        avocat_nom = f"{avocat_principal.avocat.nom} {avocat_principal.avocat.prenom}" if avocat_principal else "Non assigné"
        
        dossier_info = {
            'id': d.id,
            'titre': safe_str(d.titre),
            'numero_reference': safe_str(d.numero_reference_dossier),
            'type_affaire': safe_str(d.type_affaire.nom_type) if d.type_affaire else '',
            'statut': safe_str(d.statut_dossier),
            'score': safe_str(d.score),
            'date_ouverture': d.date_ouverture.strftime('%d/%m/%Y') if d.date_ouverture else '',
            'date_cloture': d.date_cloture.strftime('%d/%m/%Y') if d.date_cloture else 'En cours',
            'montant_fc': safe_float(d.montant_fc_enreg),
            'montant_usd': safe_float(d.montant_dollars_enreg),
            'avocat_principal': avocat_nom
        }
        
        # Calculs pour statistiques
        total_fc += safe_float(d.montant_fc_enreg)
        total_usd += safe_float(d.montant_dollars_enreg)
        
        if d.score == 'gagne':
            dossiers_gagnes += 1
        elif d.score == 'perdu':
            dossiers_perdus += 1
            
        if d.statut_dossier == 'Ouvert':
            dossiers_ouverts += 1
        elif d.statut_dossier == 'Clôturé':
            dossiers_clotures += 1
        
        dossiers_data.append(dossier_info)
    
    # Structure des données compatible avec JSReport Handlebars
    data = {
        "rapport": {
            "today": today,
            "type": type_rapport,
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
        },
        "client": {
            "id": client_obj.id,
            "nom": safe_str(client_obj.nom),
            "prenom": safe_str(client_obj.prenom),
            "nom_complet": f"{safe_str(client_obj.nom)} {safe_str(client_obj.prenom)}",
            "email": safe_str(client_obj.email),
            "telephone": safe_str(client_obj.telephone),
            "adresse": f"{client_obj.adresse.numero}, {client_obj.adresse.avenue}, {client_obj.adresse.quartier}, {client_obj.adresse.commune}, {client_obj.adresse.ville}" if client_obj.adresse else safe_str(client_obj.adresse),
            "date_creation": client_obj.date_creation.strftime('%d/%m/%Y') if client_obj.date_creation else '',
            "photo_url": client_obj.photo.url if client_obj.photo else None
        },
        "cabinet": {
            "nom": safe_str(client_obj.cabinet.nom) if client_obj.cabinet else safe_str(request.user.cabinet.nom),
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "dossiers": dossiers_data,
        "statistiques": {
            "total_dossiers": len(dossiers_data),
            "dossiers_ouverts": dossiers_ouverts,
            "dossiers_clotures": dossiers_clotures,
            "dossiers_gagnes": dossiers_gagnes,
            "dossiers_perdus": dossiers_perdus,
            "montant_total_fc": total_fc,
            "montant_total_usd": total_usd
        }
    }
    
    return data

def generer_rapport_jsreport(data, type_rapport, format_rapport):
    """
    Génère le rapport via JSReport Docker (utilise le service centralisé)
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Nom du template JSReport selon le type de rapport
        template_name = "Rapport"  # Utilisez votre template existant
        
        # Générer le PDF via le service centralisé
        pdf_content = jsreport_service.generate_pdf(template_name, data)
        
        # Créer le dossier rapports s'il n'existe pas
        import os
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Nom du fichier
        filename = f"rapport_client_{data['client']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier PDF
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except requests.RequestException as e:
        logger.error(f"Erreur lors de la génération du PDF JSReport: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Erreur génération JSReport: {str(e)}")
        return None

def generer_rapport_demo(data, type_rapport, format_rapport):
    """
    Génère un rapport démo en HTML quand JSReport n'est pas disponible
    """
    try:
        import os
        from django.template.loader import render_to_string
        
        # Créer le dossier rapports s'il n'existe pas
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Générer le contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Rapport Client - {data['client']['nom']} {data['client']['prenom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .section {{ margin: 20px 0; }}
                .stats {{ display: flex; justify-content: space-around; background: #f5f5f5; padding: 15px; }}
                .stat-item {{ text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="demo-notice">
                <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo. 
                Configurez JSReport Docker pour la génération complète des rapports.
            </div>
            
            <div class="header">
                <h1>Rapport Client - {type_rapport.title()}</h1>
                <h2>{data['client']['nom']} {data['client']['prenom']}</h2>
                <p>Généré le {data['rapport']['date_generation']} par {data['rapport']['genere_par']}</p>
            </div>
            
            <div class="section">
                <h3>📊 Statistiques</h3>
                <div class="stats">
                    <div class="stat-item">
                        <strong>{data['statistiques']['total_dossiers']}</strong><br>
                        Total Dossiers
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['dossiers_gagnes']}</strong><br>
                        Dossiers Gagnés
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['dossiers_perdus']}</strong><br>
                        Dossiers Perdus
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['montant_total_fc']:,} FC</strong><br>
                        Montant Total
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>👤 Informations Client</h3>
                <table>
                    <tr><th>Nom</th><td>{data['client']['nom']} {data['client']['prenom']}</td></tr>
                    <tr><th>Email</th><td>{data['client']['email']}</td></tr>
                    <tr><th>Téléphone</th><td>{data['client']['telephone']}</td></tr>
                    <tr><th>Adresse</th><td>{data['client']['adresse']}</td></tr>
                    <tr><th>Date création</th><td>{data['client']['date_creation']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>📁 Dossiers</h3>
                <table>
                    <tr>
                        <th>Titre</th>
                        <th>Type</th>
                        <th>Statut</th>
                        <th>Score</th>
                        <th>Montant FC</th>
                        <th>Avocat</th>
                    </tr>
        """
        
        for dossier in data['dossiers']:
            html_content += f"""
                    <tr>
                        <td>{dossier['titre']}</td>
                        <td>{dossier['type_affaire']}</td>
                        <td>{dossier['statut']}</td>
                        <td>{dossier['score']}</td>
                        <td>{dossier['montant_fc']:,} FC</td>
                        <td>{dossier['avocat_principal']}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div class="section">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        # Nom du fichier
        filename = f"demo_client_{data['client']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération rapport démo: {str(e)}")
        return None

@login_required(login_url='Connexion')
def imprimer_rapport_client(request, client_id):
    """
    Génère et retourne directement le PDF du rapport client (même approche que imprimer_facture_paiement)
    """
    try:
        # Récupérer le client
        client_obj = get_object_or_404(client, id=client_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and client_obj.cabinet != user_cabinet:
            return HttpResponse("Accès non autorisé", status=403)
        
        from utils.jsreport_service import jsreport_service
        
        # Récupérer le type de rapport depuis les paramètres GET
        type_rapport = request.GET.get('type', 'complet')
        
        # Préparer les données
        rapport_data = preparer_donnees_rapport_client(client_obj, type_rapport, request)
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_client_{client_obj.id}_{type_rapport}.pdf"
        return jsreport_service.generate_pdf_response(
            template_name="rapport",  # Votre template existant
            data=rapport_data,
            filename=filename
        )
        
    except requests.RequestException as e:
        return HttpResponse(f"Erreur lors de la génération du PDF : {e}", status=500)
    except Exception as e:
        logger.error(f"Erreur génération rapport client: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def generer_rapport_agent(request):
    """
    Génère un rapport agent via JSReport
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        # Récupérer les paramètres
        agent_id = request.POST.get('agent_id')
        type_rapport = request.POST.get('type_rapport', 'complet')
        format_rapport = request.POST.get('format', 'pdf')
        
        if not agent_id:
            return JsonResponse({'error': 'Agent non spécifié'}, status=400)
        
        # Récupérer l'agent
        agent_obj = get_object_or_404(agent, id=agent_id)
        
        # Vérifier les permissions
        user_company = getattr(request.user, 'company', None)
        if user_company and agent_obj.company != user_company:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Préparer les données pour le rapport
        rapport_data = preparer_donnees_rapport_agent(agent_obj, type_rapport, request)
        
        # Générer le rapport via JSReport
        rapport_url = generer_rapport_jsreport_agent(rapport_data, type_rapport, format_rapport)
        
        if rapport_url:
            return JsonResponse({
                'success': True,
                'rapport_url': rapport_url,
                'agent_nom': f"{agent_obj.nom} {agent_obj.prenom}",
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'jsreport'
            })
        else:
            # Mode démo si JSReport n'est pas disponible
            demo_url = generer_rapport_demo_agent(rapport_data, type_rapport, format_rapport)
            return JsonResponse({
                'success': True,
                'rapport_url': demo_url,
                'agent_nom': f"{agent_obj.nom} {agent_obj.prenom}",
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'demo',
                'message': 'Rapport généré en mode démo. Configurez JSReport pour la génération complète.'
            })
            
    except Exception as e:
        logger.error(f"Erreur génération rapport agent: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

def preparer_donnees_rapport_agent(agent_obj, type_rapport, request):
    """
    Prépare les données pour le rapport agent (format compatible JSReport Handlebars)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Récupérer les dossiers assignés à l'agent
    from Dossier.models import AvocatDossier
    dossiers_assignes = AvocatDossier.objects.filter(avocat=agent_obj).order_by('-dossier__date_ouverture')
    
    dossiers_data = []
    total_dossiers = 0
    dossiers_principaux = 0
    dossiers_secondaires = 0
    dossiers_gagnes = 0
    dossiers_perdus = 0
    dossiers_ouverts = 0
    dossiers_clotures = 0
    
    for ad in dossiers_assignes:
        d = ad.dossier
        
        dossier_info = {
            'id': d.id,
            'titre': safe_str(d.titre),
            'numero_reference': safe_str(d.numero_reference_dossier),
            'type_affaire': safe_str(d.type_affaire.nom_type) if d.type_affaire else '',
            'statut': safe_str(d.statut_dossier),
            'score': safe_str(d.score),
            'role': safe_str(ad.role),
            'date_ouverture': d.date_ouverture.strftime('%d/%m/%Y') if d.date_ouverture else '',
            'date_cloture': d.date_cloture.strftime('%d/%m/%Y') if d.date_cloture else 'En cours',
            'montant_fc': safe_float(d.montant_fc_enreg),
            'montant_usd': safe_float(d.montant_dollars_enreg),
            'client_nom': f"{d.client.nom} {d.client.prenom}" if d.client else "Client non défini"
        }
        
        # Calculs pour statistiques
        total_dossiers += 1
        
        if ad.role == 'Principal':
            dossiers_principaux += 1
        else:
            dossiers_secondaires += 1
        
        if d.score == 'gagne':
            dossiers_gagnes += 1
        elif d.score == 'perdu':
            dossiers_perdus += 1
            
        if d.statut_dossier == 'Ouvert':
            dossiers_ouverts += 1
        elif d.statut_dossier == 'Clôturé':
            dossiers_clotures += 1
        
        dossiers_data.append(dossier_info)
    
    # Récupérer les activités récentes si disponibles
    activites_data = []
    try:
        from Agent.models_activity import ActivityLog
        from datetime import timedelta
        from Authentification.models import CompteUtilisateur
        
        # Trouver l'utilisateur associé à cet agent
        user_agent = CompteUtilisateur.objects.get(agent=agent_obj)
        date_limite = datetime.now() - timedelta(days=30)
        
        activites = ActivityLog.objects.filter(
            user=user_agent,
            timestamp__gte=date_limite
        ).order_by('-timestamp')[:20]
        
        for activite in activites:
            activites_data.append({
                'action': safe_str(activite.action),
                'description': safe_str(activite.description),
                'timestamp': activite.timestamp.strftime('%d/%m/%Y %H:%M'),
                'model_name': safe_str(activite.model_name),
                'object_id': safe_str(activite.object_id)
            })
    except:
        pass
    
    # Informations sur l'utilisateur associé
    user_info = {}
    try:
        from Authentification.models import CompteUtilisateur
        user_agent = CompteUtilisateur.objects.get(agent=agent_obj)
        user_info = {
            'username': safe_str(user_agent.username),
            'email': safe_str(user_agent.email),
            'is_active': user_agent.is_active,
            'date_joined': user_agent.date_joined.strftime('%d/%m/%Y') if user_agent.date_joined else '',
            'last_login': user_agent.last_login.strftime('%d/%m/%Y %H:%M') if user_agent.last_login else 'Jamais connecté'
        }
    except CompteUtilisateur.DoesNotExist:
        user_info = {
            'username': 'Pas de compte',
            'email': '',
            'is_active': False,
            'date_joined': '',
            'last_login': 'Pas de compte'
        }
    
    # Structure des données compatible avec JSReport Handlebars
    data = {
        "rapport": {
            "today": today,
            "type": type_rapport,
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
        },
        "agent": {
            "id": agent_obj.id,
            "nom": safe_str(agent_obj.nom),
            "prenom": safe_str(agent_obj.prenom),
            "nom_complet": f"{safe_str(agent_obj.nom)} {safe_str(agent_obj.prenom)}",
            "email": safe_str(agent_obj.email),
            "telephone": safe_str(agent_obj.telephone),
            "poste": safe_str(agent_obj.poste),
            "specialite": safe_str(agent_obj.specialite.nom_specialite) if agent_obj.specialite else '',
            "adresse": f"{agent_obj.adresse.numero}, {agent_obj.adresse.avenue}, {agent_obj.adresse.quartier}, {agent_obj.adresse.commune}, {agent_obj.adresse.ville}" if agent_obj.adresse else safe_str(agent_obj.adresse),
            "date_creation": agent_obj.date_creation.strftime('%d/%m/%Y') if agent_obj.date_creation else '',
            "date_naissance": agent_obj.date_naissance.strftime('%d/%m/%Y') if agent_obj.date_naissance else '',
            "annee_experience": safe_str(agent_obj.annee_experience),
            "numero_identification": safe_str(agent_obj.numero_identification),
            "photo_url": agent_obj.photo.url if agent_obj.photo else None
        },
        "cabinet": {
            "nom": safe_str(agent_obj.company.nom) if agent_obj.company else safe_str(request.user.cabinet.nom),
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "dossiers": dossiers_data,
        "activites": activites_data,
        "user_info": user_info,
        "statistiques": {
            "total_dossiers": total_dossiers,
            "dossiers_principaux": dossiers_principaux,
            "dossiers_secondaires": dossiers_secondaires,
            "dossiers_ouverts": dossiers_ouverts,
            "dossiers_clotures": dossiers_clotures,
            "dossiers_gagnes": dossiers_gagnes,
            "dossiers_perdus": dossiers_perdus,
            "activites_recentes": len(activites_data)
        }
    }
    
    return data

def generer_rapport_jsreport_agent(data, type_rapport, format_rapport):
    """
    Génère le rapport agent via JSReport Docker (utilise le service centralisé)
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Nom du template JSReport selon le type de rapport
        template_name = "RapportAgent"  # Utilisez votre template existant ou créez-en un
        
        # Générer le PDF via le service centralisé
        pdf_content = jsreport_service.generate_pdf(template_name, data)
        
        # Créer le dossier rapports s'il n'existe pas
        import os
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Nom du fichier
        filename = f"rapport_agent_{data['agent']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier PDF
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération JSReport agent: {str(e)}")
        return None

def generer_rapport_demo_agent(data, type_rapport, format_rapport):
    """
    Génère un rapport démo agent en HTML quand JSReport n'est pas disponible
    """
    try:
        import os
        
        # Créer le dossier rapports s'il n'existe pas
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Générer le contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Rapport Agent - {data['agent']['nom']} {data['agent']['prenom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .section {{ margin: 20px 0; }}
                .stats {{ display: flex; justify-content: space-around; background: #f5f5f5; padding: 15px; }}
                .stat-item {{ text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="demo-notice">
                <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo. 
                Configurez JSReport Docker pour la génération complète des rapports.
            </div>
            
            <div class="header">
                <h1>Rapport Agent - {type_rapport.title()}</h1>
                <h2>{data['agent']['nom']} {data['agent']['prenom']}</h2>
                <p>Généré le {data['rapport']['date_generation']} par {data['rapport']['genere_par']}</p>
            </div>
            
            <div class="section">
                <h3>📊 Statistiques</h3>
                <div class="stats">
                    <div class="stat-item">
                        <strong>{data['statistiques']['total_dossiers']}</strong><br>
                        Total Dossiers
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['dossiers_principaux']}</strong><br>
                        Dossiers Principaux
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['dossiers_gagnes']}</strong><br>
                        Dossiers Gagnés
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['activites_recentes']}</strong><br>
                        Activités (30j)
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>👤 Informations Agent</h3>
                <table>
                    <tr><th>Nom</th><td>{data['agent']['nom']} {data['agent']['prenom']}</td></tr>
                    <tr><th>Poste</th><td>{data['agent']['poste']}</td></tr>
                    <tr><th>Spécialité</th><td>{data['agent']['specialite']}</td></tr>
                    <tr><th>Email</th><td>{data['agent']['email']}</td></tr>
                    <tr><th>Téléphone</th><td>{data['agent']['telephone']}</td></tr>
                    <tr><th>Expérience</th><td>{data['agent']['annee_experience']} ans</td></tr>
                    <tr><th>Date création</th><td>{data['agent']['date_creation']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>💼 Compte Utilisateur</h3>
                <table>
                    <tr><th>Nom d'utilisateur</th><td>{data['user_info']['username']}</td></tr>
                    <tr><th>Email</th><td>{data['user_info']['email']}</td></tr>
                    <tr><th>Statut</th><td>{'Actif' if data['user_info']['is_active'] else 'Inactif'}</td></tr>
                    <tr><th>Date d'inscription</th><td>{data['user_info']['date_joined']}</td></tr>
                    <tr><th>Dernière connexion</th><td>{data['user_info']['last_login']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>📁 Dossiers Assignés</h3>
                <table>
                    <tr>
                        <th>Titre</th>
                        <th>Client</th>
                        <th>Rôle</th>
                        <th>Statut</th>
                        <th>Score</th>
                        <th>Date Ouverture</th>
                    </tr>
        """
        
        for dossier in data['dossiers']:
            html_content += f"""
                    <tr>
                        <td>{dossier['titre']}</td>
                        <td>{dossier['client_nom']}</td>
                        <td>{dossier['role']}</td>
                        <td>{dossier['statut']}</td>
                        <td>{dossier['score']}</td>
                        <td>{dossier['date_ouverture']}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
        """
        
        # Ajouter les activités si disponibles
        if data['activites']:
            html_content += """
            <div class="section">
                <h3>🔄 Activités Récentes (30 derniers jours)</h3>
                <table>
                    <tr>
                        <th>Date</th>
                        <th>Action</th>
                        <th>Description</th>
                    </tr>
            """
            
            for activite in data['activites'][:10]:  # Limiter à 10 activités
                html_content += f"""
                        <tr>
                            <td>{activite['timestamp']}</td>
                            <td>{activite['action']}</td>
                            <td>{activite['description']}</td>
                        </tr>
                """
            
            html_content += """
                </table>
            </div>
            """
        
        html_content += """
            <div class="section">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        # Nom du fichier
        filename = f"demo_agent_{data['agent']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération rapport démo agent: {str(e)}")
        return None

@login_required(login_url='Connexion')
def imprimer_rapport_agent(request, agent_id):
    """
    Génère et retourne directement le PDF du rapport agent (même approche que imprimer_facture_paiement)
    """
    try:
        # Récupérer l'agent
        agent_obj = get_object_or_404(agent, id=agent_id)
        
        # Vérifier les permissions
        user_company = getattr(request.user, 'company', None)
        if user_company and agent_obj.company != user_company:
            return HttpResponse("Accès non autorisé", status=403)
        
        from utils.jsreport_service import jsreport_service
        
        # Récupérer le type de rapport depuis les paramètres GET
        type_rapport = request.GET.get('type', 'complet')
        
        # Préparer les données
        rapport_data = preparer_donnees_rapport_agent(agent_obj, type_rapport, request)
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_agent_{agent_obj.id}_{type_rapport}.pdf"
        return jsreport_service.generate_pdf_response(
            template_name="rapport_agent",  # Votre template existant
            data=rapport_data,
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Erreur génération rapport agent: {str(e)}")
        # En cas d'erreur JSReport, générer un rapport démo
        try:
            rapport_data = preparer_donnees_rapport_agent(agent_obj, type_rapport, request)
            demo_url = generer_rapport_demo_agent(rapport_data, type_rapport, 'html')
            if demo_url:
                return HttpResponse(f'<script>window.open("{demo_url}", "_blank");</script>')
        except:
            pass
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def telecharger_rapport_client(request, rapport_id):
    """
    Télécharge un rapport client généré (fonction conservée pour compatibilité)
    """
    # Cette fonction peut être utilisée pour télécharger des rapports sauvegardés
    pass

@login_required(login_url='Connexion')
def generer_rapport_juridiction(request):
    """
    Génère un rapport juridiction via JSReport
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        # Récupérer les paramètres
        juridiction_id = request.POST.get('juridiction_id')
        type_rapport = request.POST.get('type_rapport', 'complet')
        format_rapport = request.POST.get('format', 'pdf')
        
        if not juridiction_id:
            return JsonResponse({'error': 'Juridiction non spécifiée'}, status=400)
        
        # Récupérer la juridiction
        juridiction_obj = get_object_or_404(Juridiction, id=juridiction_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and juridiction_obj.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Préparer les données pour le rapport
        rapport_data = preparer_donnees_rapport_juridiction(juridiction_obj, type_rapport, request)
        
        # Générer le rapport via JSReport
        rapport_url = generer_rapport_jsreport_juridiction(rapport_data, type_rapport, format_rapport)
        
        if rapport_url:
            return JsonResponse({
                'success': True,
                'rapport_url': rapport_url,
                'juridiction_nom': juridiction_obj.nom,
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'jsreport'
            })
        else:
            # Mode démo si JSReport n'est pas disponible
            demo_url = generer_rapport_demo_juridiction(rapport_data, type_rapport, format_rapport)
            return JsonResponse({
                'success': True,
                'rapport_url': demo_url,
                'juridiction_nom': juridiction_obj.nom,
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'demo',
                'message': 'Rapport généré en mode démo. Configurez JSReport pour la génération complète.'
            })
            
    except Exception as e:
        logger.error(f"Erreur génération rapport juridiction: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

def preparer_donnees_rapport_juridiction(juridiction_obj, type_rapport, request):
    """
    Prépare les données pour le rapport juridiction (format compatible JSReport Handlebars)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Récupérer les dossiers liés à cette juridiction (si applicable)
    # Note: Ceci dépend de la logique métier - il faudrait une relation entre dossier et juridiction
    dossiers_lies = []  # À implémenter selon la logique métier
    
    # Récupérer les agents qui travaillent dans cette juridiction (si applicable)
    agents_lies = []  # À implémenter selon la logique métier
    
    # Structure des données compatible avec JSReport Handlebars
    data = {
        "rapport": {
            "today": today,
            "type": type_rapport,
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
        },
        "juridiction": {
            "id": juridiction_obj.id,
            "nom": safe_str(juridiction_obj.nom),
            "lieu": safe_str(juridiction_obj.lieu.nom) if juridiction_obj.lieu else 'Non défini',
            "date_creation": juridiction_obj.date_creation.strftime('%d/%m/%Y') if juridiction_obj.date_creation else '',
            "adresse_complete": f"{juridiction_obj.lieu.nom}" if juridiction_obj.lieu else 'Adresse non définie'
        },
        "cabinet": {
            "nom": safe_str(juridiction_obj.cabinet.nom) if juridiction_obj.cabinet else safe_str(request.user.cabinet.nom),
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "dossiers": dossiers_lies,
        "agents": agents_lies,
        "statistiques": {
            "total_dossiers": len(dossiers_lies),
            "total_agents": len(agents_lies),
            "date_creation": juridiction_obj.date_creation.strftime('%d/%m/%Y') if juridiction_obj.date_creation else ''
        }
    }
    
    return data

def generer_rapport_jsreport_juridiction(data, type_rapport, format_rapport):
    """
    Génère le rapport juridiction via JSReport Docker (utilise le service centralisé)
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Nom du template JSReport selon le type de rapport
        template_name = "RapportJuridiction"  # Utilisez votre template existant ou créez-en un
        
        # Générer le PDF via le service centralisé
        pdf_content = jsreport_service.generate_pdf(template_name, data)
        
        # Créer le dossier rapports s'il n'existe pas
        import os
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Nom du fichier
        filename = f"rapport_juridiction_{data['juridiction']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier PDF
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération JSReport juridiction: {str(e)}")
        return None

def generer_rapport_demo_juridiction(data, type_rapport, format_rapport):
    """
    Génère un rapport démo juridiction en HTML quand JSReport n'est pas disponible
    """
    try:
        import os
        
        # Créer le dossier rapports s'il n'existe pas
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Générer le contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Rapport Juridiction - {data['juridiction']['nom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .section {{ margin: 20px 0; }}
                .stats {{ display: flex; justify-content: space-around; background: #f5f5f5; padding: 15px; }}
                .stat-item {{ text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="demo-notice">
                <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo. 
                Configurez JSReport Docker pour la génération complète des rapports.
            </div>
            
            <div class="header">
                <h1>Rapport Juridiction - {type_rapport.title()}</h1>
                <h2>{data['juridiction']['nom']}</h2>
                <p>Généré le {data['rapport']['date_generation']} par {data['rapport']['genere_par']}</p>
            </div>
            
            <div class="section">
                <h3>📊 Statistiques</h3>
                <div class="stats">
                    <div class="stat-item">
                        <strong>{data['statistiques']['total_dossiers']}</strong><br>
                        Dossiers Liés
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['total_agents']}</strong><br>
                        Agents Assignés
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['date_creation']}</strong><br>
                        Date Création
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🏛️ Informations Juridiction</h3>
                <table>
                    <tr><th>Nom</th><td>{data['juridiction']['nom']}</td></tr>
                    <tr><th>Lieu</th><td>{data['juridiction']['lieu']}</td></tr>
                    <tr><th>Adresse</th><td>{data['juridiction']['adresse_complete']}</td></tr>
                    <tr><th>Date création</th><td>{data['juridiction']['date_creation']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>🏢 Cabinet</h3>
                <table>
                    <tr><th>Nom du cabinet</th><td>{data['cabinet']['nom']}</td></tr>
                    <tr><th>Téléphone</th><td>{data['cabinet']['telephone']}</td></tr>
                    <tr><th>Email</th><td>{data['cabinet']['email']}</td></tr>
                    <tr><th>Adresse</th><td>{data['cabinet']['adresse']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        # Nom du fichier
        filename = f"demo_juridiction_{data['juridiction']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération rapport démo juridiction: {str(e)}")
        return None

@login_required(login_url='Connexion')
def generer_rapport_commune(request):
    """
    Génère un rapport commune via JSReport
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        # Récupérer les paramètres
        commune_id = request.POST.get('commune_id')
        type_rapport = request.POST.get('type_rapport', 'complet')
        format_rapport = request.POST.get('format', 'pdf')
        
        if not commune_id:
            return JsonResponse({'error': 'Commune non spécifiée'}, status=400)
        
        # Récupérer la commune
        commune_obj = get_object_or_404(commune, id=commune_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and commune_obj.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Préparer les données pour le rapport
        rapport_data = preparer_donnees_rapport_commune(commune_obj, type_rapport, request)
        
        # Générer le rapport via JSReport
        rapport_url = generer_rapport_jsreport_commune(rapport_data, type_rapport, format_rapport)
        
        if rapport_url:
            return JsonResponse({
                'success': True,
                'rapport_url': rapport_url,
                'commune_nom': commune_obj.nom,
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'jsreport'
            })
        else:
            # Mode démo si JSReport n'est pas disponible
            demo_url = generer_rapport_demo_commune(rapport_data, type_rapport, format_rapport)
            return JsonResponse({
                'success': True,
                'rapport_url': demo_url,
                'commune_nom': commune_obj.nom,
                'type_rapport': type_rapport,
                'format': format_rapport,
                'mode': 'demo',
                'message': 'Rapport généré en mode démo. Configurez JSReport pour la génération complète.'
            })
            
    except Exception as e:
        logger.error(f"Erreur génération rapport commune: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

def preparer_donnees_rapport_commune(commune_obj, type_rapport, request):
    """
    Prépare les données pour le rapport commune (format compatible JSReport Handlebars)
    """
    # Fonctions utilitaires
    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Structure des données compatible avec JSReport Handlebars
    data = {
        "rapport": {
            "today": today,
            "type": type_rapport,
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
        },
        "commune": {
            "id": commune_obj.id,
            "nom": safe_str(commune_obj.nom),
            "date_ouverture": commune_obj.date_ouverture.strftime('%d/%m/%Y %H:%M') if commune_obj.date_ouverture else '',
            "statut": "Actif"  # Par défaut
        },
        "cabinet": {
            "nom": safe_str(commune_obj.cabinet.nom) if commune_obj.cabinet else safe_str(request.user.cabinet.nom),
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "statistiques": {
            "date_ouverture": commune_obj.date_ouverture.strftime('%d/%m/%Y') if commune_obj.date_ouverture else '',
            "statut": "Actif"
        }
    }
    
    return data

def generer_rapport_jsreport_commune(data, type_rapport, format_rapport):
    """
    Génère le rapport commune via JSReport Docker (utilise le service centralisé)
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Nom du template JSReport selon le type de rapport
        template_name = "RapportCommune"  # Utilisez votre template existant ou créez-en un
        
        # Générer le PDF via le service centralisé
        pdf_content = jsreport_service.generate_pdf(template_name, data)
        
        # Créer le dossier rapports s'il n'existe pas
        import os
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Nom du fichier
        filename = f"rapport_commune_{data['commune']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier PDF
        with open(filepath, 'wb') as f:
            f.write(pdf_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération JSReport commune: {str(e)}")
        return None

def generer_rapport_demo_commune(data, type_rapport, format_rapport):
    """
    Génère un rapport démo commune en HTML quand JSReport n'est pas disponible
    """
    try:
        import os
        
        # Créer le dossier rapports s'il n'existe pas
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Générer le contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Rapport Commune - {data['commune']['nom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #333; padding-bottom: 20px; }}
                .section {{ margin: 20px 0; }}
                .stats {{ display: flex; justify-content: space-around; background: #f5f5f5; padding: 15px; }}
                .stat-item {{ text-align: center; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="demo-notice">
                <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo. 
                Configurez JSReport Docker pour la génération complète des rapports.
            </div>
            
            <div class="header">
                <h1>Rapport Commune - {type_rapport.title()}</h1>
                <h2>{data['commune']['nom']}</h2>
                <p>Généré le {data['rapport']['date_generation']} par {data['rapport']['genere_par']}</p>
            </div>
            
            <div class="section">
                <h3>📊 Statistiques</h3>
                <div class="stats">
                    <div class="stat-item">
                        <strong>{data['statistiques']['statut']}</strong><br>
                        Statut
                    </div>
                    <div class="stat-item">
                        <strong>{data['statistiques']['date_ouverture']}</strong><br>
                        Date Ouverture
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>🏛️ Informations Commune</h3>
                <table>
                    <tr><th>Nom</th><td>{data['commune']['nom']}</td></tr>
                    <tr><th>Date ouverture</th><td>{data['commune']['date_ouverture']}</td></tr>
                    <tr><th>Statut</th><td>{data['commune']['statut']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>🏢 Cabinet</h3>
                <table>
                    <tr><th>Nom du cabinet</th><td>{data['cabinet']['nom']}</td></tr>
                    <tr><th>Téléphone</th><td>{data['cabinet']['telephone']}</td></tr>
                    <tr><th>Email</th><td>{data['cabinet']['email']}</td></tr>
                    <tr><th>Adresse</th><td>{data['cabinet']['adresse']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        # Nom du fichier
        filename = f"demo_commune_{data['commune']['id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération rapport démo commune: {str(e)}")
        return None

@login_required(login_url='Connexion')
def imprimer_rapport_commune(request, commune_id):
    """
    Génère et retourne directement le PDF du rapport commune (même approche que imprimer_facture_paiement)
    """
    try:
        # Récupérer la commune
        commune_obj = get_object_or_404(commune, id=commune_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and commune_obj.cabinet != user_cabinet:
            return HttpResponse("Accès non autorisé", status=403)
        
        from utils.jsreport_service import jsreport_service
        
        # Récupérer le type de rapport depuis les paramètres GET
        type_rapport = request.GET.get('type', 'complet')
        
        # Préparer les données
        rapport_data = preparer_donnees_rapport_commune(commune_obj, type_rapport, request)
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_commune_{commune_obj.id}_{type_rapport}.pdf"
        return jsreport_service.generate_pdf_response(
            template_name="rapport_commune",  # Votre template existant
            data=rapport_data,
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Erreur génération rapport commune: {str(e)}")
        # En cas d'erreur JSReport, générer un rapport démo
        try:
            rapport_data = preparer_donnees_rapport_commune(commune_obj, type_rapport, request)
            demo_url = generer_rapport_demo_commune(rapport_data, type_rapport, 'html')
            if demo_url:
                return HttpResponse(f'<script>window.open("{demo_url}", "_blank");</script>')
        except:
            pass
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
@login_required(login_url='Connexion')
def imprimer_rapport_juridiction(request, juridiction_id):
    """
    Génère et retourne directement le PDF du rapport juridiction (même approche que imprimer_facture_paiement)
    """
    try:
        # Récupérer la juridiction
        juridiction_obj = get_object_or_404(Juridiction, id=juridiction_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and juridiction_obj.cabinet != user_cabinet:
            return HttpResponse("Accès non autorisé", status=403)
        
        from utils.jsreport_service import jsreport_service
        
        # Récupérer le type de rapport depuis les paramètres GET
        type_rapport = request.GET.get('type', 'complet')
        
        # Préparer les données
        rapport_data = preparer_donnees_rapport_juridiction(juridiction_obj, type_rapport, request)
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_juridiction_{juridiction_obj.id}_{type_rapport}.pdf"
        return jsreport_service.generate_pdf_response(
            template_name="rapport_juridiction",  # Votre template existant
            data=rapport_data,
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Erreur génération rapport juridiction: {str(e)}")
        # En cas d'erreur JSReport, générer un rapport démo
        try:
            rapport_data = preparer_donnees_rapport_juridiction(juridiction_obj, type_rapport, request)
            demo_url = generer_rapport_demo_juridiction(rapport_data, type_rapport, 'html')
            if demo_url:
                return HttpResponse(f'<script>window.open("{demo_url}", "_blank");</script>')
        except:
            pass
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def details_commune_ajax(request, commune_id):
    """
    Retourne les détails d'une commune via AJAX
    """
    try:
        # Récupérer la commune
        commune_obj = get_object_or_404(commune, id=commune_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and commune_obj.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Préparer les données
        data = {
            'id': commune_obj.id,
            'nom': commune_obj.nom,
            'date_ouverture': commune_obj.date_ouverture.strftime('%d/%m/%Y %H:%M') if commune_obj.date_ouverture else None,
            'statut': 'Actif',  # Par défaut
            'cabinet': commune_obj.cabinet.nom if commune_obj.cabinet else 'Non défini',
            'derniere_modification': commune_obj.date_ouverture.strftime('%d/%m/%Y') if commune_obj.date_ouverture else None
        }
        
        return JsonResponse({'success': True, 'data': data})
        
    except Exception as e:
        logger.error(f"Erreur récupération détails commune: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

@login_required(login_url='Connexion')
def export_communes_selection(request):
    """
    Exporte les communes sélectionnées en PDF
    """
    try:
        # Récupérer les IDs des communes sélectionnées
        communes_ids = request.GET.get('communes', '').split(',')
        communes_ids = [int(id) for id in communes_ids if id.isdigit()]
        
        if not communes_ids:
            return HttpResponse("Aucune commune sélectionnée", status=400)
        
        # Récupérer les communes
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet:
            communes_obj = commune.objects.filter(id__in=communes_ids, cabinet=user_cabinet)
        else:
            communes_obj = commune.objects.filter(id__in=communes_ids)
        
        # Préparer les données pour le rapport consolidé
        rapport_data = {
            "rapport": {
                "today": datetime.now().strftime("%d/%m/%Y"),
                "type": "selection",
                "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
                "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username,
                "titre": f"Rapport de {len(communes_obj)} commune(s) sélectionnée(s)"
            },
            "cabinet": {
                "nom": user_cabinet.nom if user_cabinet else "Cabinet",
                "telephone": user_cabinet.telephone if user_cabinet else '',
                "email": user_cabinet.email if user_cabinet else '',
                "adresse": f"{user_cabinet.adresse.numero}, {user_cabinet.adresse.avenue}, {user_cabinet.adresse.quartier}, {user_cabinet.adresse.commune}, {user_cabinet.adresse.ville}" if user_cabinet and user_cabinet.adresse else '',
                "logo": user_cabinet.logo.url if user_cabinet and user_cabinet.logo else None
            },
            "communes": []
        }
        
        for com in communes_obj:
            rapport_data["communes"].append({
                "id": com.id,
                "nom": com.nom or "",
                "date_ouverture": com.date_ouverture.strftime('%d/%m/%Y %H:%M') if com.date_ouverture else '',
                "statut": "Actif"
            })
        
        # Générer le rapport via JSReport ou mode démo
        try:
            from utils.jsreport_service import jsreport_service
            filename = f"rapport_communes_selection_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return jsreport_service.generate_pdf_response(
                template_name="rapport_communes_selection",
                data=rapport_data,
                filename=filename
            )
        except:
            # Mode démo HTML
            html_content = generer_rapport_demo_communes_selection(rapport_data)
            response = HttpResponse(html_content, content_type='text/html')
            return response
        
    except Exception as e:
        logger.error(f"Erreur export communes sélection: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def export_communes_global(request):
    """
    Exporte toutes les communes en PDF
    """
    try:
        # Récupérer toutes les communes du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet:
            communes_obj = commune.objects.filter(cabinet=user_cabinet).order_by('nom')
        else:
            communes_obj = commune.objects.all().order_by('nom')
        
        # Préparer les données pour le rapport global
        rapport_data = {
            "rapport": {
                "today": datetime.now().strftime("%d/%m/%Y"),
                "type": "global",
                "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
                "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username,
                "titre": f"Rapport global de toutes les communes ({communes_obj.count()})"
            },
            "cabinet": {
                "nom": user_cabinet.nom if user_cabinet else "Cabinet",
                "telephone": user_cabinet.telephone if user_cabinet else '',
                "email": user_cabinet.email if user_cabinet else '',
                "adresse": f"{user_cabinet.adresse.numero}, {user_cabinet.adresse.avenue}, {user_cabinet.adresse.quartier}, {user_cabinet.adresse.commune}, {user_cabinet.adresse.ville}" if user_cabinet and user_cabinet.adresse else '',
                "logo": user_cabinet.logo.url if user_cabinet and user_cabinet.logo else None
            },
            "communes": [],
            "statistiques": {
                "total_communes": communes_obj.count(),
                "communes_actives": communes_obj.count(),  # Toutes sont considérées actives par défaut
                "communes_recentes": communes_obj.filter(date_ouverture__gte=datetime.now() - timedelta(days=30)).count() if communes_obj.exists() else 0
            }
        }
        
        for com in communes_obj:
            rapport_data["communes"].append({
                "id": com.id,
                "nom": com.nom or "",
                "date_ouverture": com.date_ouverture.strftime('%d/%m/%Y %H:%M') if com.date_ouverture else '',
                "statut": "Actif"
            })
        
        # Générer le rapport via JSReport ou mode démo
        try:
            from utils.jsreport_service import jsreport_service
            filename = f"rapport_communes_global_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            return jsreport_service.generate_pdf_response(
                template_name="rapport_communes_global",
                data=rapport_data,
                filename=filename
            )
        except:
            # Mode démo HTML
            html_content = generer_rapport_demo_communes_global(rapport_data)
            response = HttpResponse(html_content, content_type='text/html')
            return response
        
    except Exception as e:
        logger.error(f"Erreur export communes global: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def statistiques_communes(request):
    """
    Génère un rapport de statistiques des communes
    """
    try:
        # Récupérer les communes du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet:
            communes_obj = commune.objects.filter(cabinet=user_cabinet)
        else:
            communes_obj = commune.objects.all()
        
        # Calculer les statistiques
        total_communes = communes_obj.count()
        communes_actives = total_communes  # Par défaut toutes actives
        
        # Statistiques par période
        maintenant = datetime.now()
        communes_ce_mois = communes_obj.filter(date_ouverture__month=maintenant.month, date_ouverture__year=maintenant.year).count()
        communes_cette_annee = communes_obj.filter(date_ouverture__year=maintenant.year).count()
        
        # Préparer les données
        rapport_data = {
            "rapport": {
                "today": maintenant.strftime("%d/%m/%Y"),
                "type": "statistiques",
                "date_generation": maintenant.strftime('%d/%m/%Y à %H:%M'),
                "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username,
                "titre": "Statistiques des Communes"
            },
            "cabinet": {
                "nom": user_cabinet.nom if user_cabinet else "Cabinet",
                "telephone": user_cabinet.telephone if user_cabinet else '',
                "email": user_cabinet.email if user_cabinet else ''
            },
            "statistiques": {
                "total_communes": total_communes,
                "communes_actives": communes_actives,
                "communes_ce_mois": communes_ce_mois,
                "communes_cette_annee": communes_cette_annee,
                "pourcentage_actives": round((communes_actives / total_communes * 100) if total_communes > 0 else 0, 1)
            }
        }
        
        # Générer le rapport HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Statistiques Communes - {rapport_data['cabinet']['nom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
                .stat-box {{ background: #f8f9fa; border-left: 4px solid #007bff; padding: 15px; margin: 10px 0; }}
                .stat-number {{ font-size: 2em; font-weight: bold; color: #007bff; }}
                .chart-placeholder {{ background: #e9ecef; height: 200px; display: flex; align-items: center; justify-content: center; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Statistiques des Communes</h1>
                <p>{rapport_data['cabinet']['nom']}</p>
                <p>Généré le {rapport_data['rapport']['date_generation']} par {rapport_data['rapport']['genere_par']}</p>
            </div>
            
            <div class="stat-box">
                <div class="stat-number">{rapport_data['statistiques']['total_communes']}</div>
                <div>Total des communes</div>
            </div>
            
            <div class="stat-box">
                <div class="stat-number">{rapport_data['statistiques']['communes_actives']}</div>
                <div>Communes actives ({rapport_data['statistiques']['pourcentage_actives']}%)</div>
            </div>
            
            <div class="stat-box">
                <div class="stat-number">{rapport_data['statistiques']['communes_ce_mois']}</div>
                <div>Communes créées ce mois</div>
            </div>
            
            <div class="stat-box">
                <div class="stat-number">{rapport_data['statistiques']['communes_cette_annee']}</div>
                <div>Communes créées cette année</div>
            </div>
            
            <div class="chart-placeholder">
                <p>📈 Graphiques à implémenter avec Chart.js</p>
            </div>
            
            <div style="margin-top: 40px; text-align: center; color: #6c757d;">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        return HttpResponse(html_content, content_type='text/html')
        
    except Exception as e:
        logger.error(f"Erreur statistiques communes: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def generer_rapport_demo_communes_selection(data):
    """
    Génère un rapport démo HTML pour une sélection de communes
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{data['rapport']['titre']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; }}
            .commune-item {{ background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 15px; margin: 10px 0; }}
            .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="demo-notice">
            <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo.
        </div>
        
        <div class="header">
            <h1>{data['rapport']['titre']}</h1>
            <p>Généré le {data['rapport']['date_generation']} par {data['rapport']['genere_par']}</p>
        </div>
        
        <div>
            <h3>📋 Liste des communes sélectionnées</h3>
    """
    
    for commune_data in data['communes']:
        html_content += f"""
            <div class="commune-item">
                <h5>🏛️ {commune_data['nom']}</h5>
                <p><strong>ID:</strong> {commune_data['id']}</p>
                <p><strong>Date ouverture:</strong> {commune_data['date_ouverture'] or 'Non définie'}</p>
                <p><strong>Statut:</strong> <span style="color: green;">{commune_data['statut']}</span></p>
            </div>
        """
    
    html_content += """
        </div>
        
        <div style="margin-top: 40px; text-align: center; color: #6c757d;">
            <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
        </div>
    </body>
    </html>
    """
    
    return html_content

def generer_rapport_demo_communes_global(data):
    """
    Génère un rapport démo HTML global des communes
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>{data['rapport']['titre']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; }}
            .stats {{ display: flex; justify-content: space-around; background: #f8f9fa; padding: 20px; margin: 20px 0; }}
            .stat-item {{ text-align: center; }}
            .commune-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px; }}
            .commune-card {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="demo-notice">
            <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo.
        </div>
        
        <div class="header">
            <h1>{data['rapport']['titre']}</h1>
            <p>{data['cabinet']['nom']}</p>
            <p>Généré le {data['rapport']['date_generation']} par {data['rapport']['genere_par']}</p>
        </div>
        
        <div class="stats">
            <div class="stat-item">
                <h3>{data['statistiques']['total_communes']}</h3>
                <p>Total Communes</p>
            </div>
            <div class="stat-item">
                <h3>{data['statistiques']['communes_actives']}</h3>
                <p>Communes Actives</p>
            </div>
            <div class="stat-item">
                <h3>{data['statistiques']['communes_recentes']}</h3>
                <p>Créées récemment</p>
            </div>
        </div>
        
        <div>
            <h3>📋 Toutes les communes</h3>
            <div class="commune-grid">
    """
    
    for commune_data in data['communes']:
        html_content += f"""
                <div class="commune-card">
                    <h5>🏛️ {commune_data['nom']}</h5>
                    <p><strong>ID:</strong> {commune_data['id']}</p>
                    <p><strong>Date ouverture:</strong> {commune_data['date_ouverture'] or 'Non définie'}</p>
                    <p><strong>Statut:</strong> <span style="color: green;">{commune_data['statut']}</span></p>
                </div>
        """
    
    html_content += """
            </div>
        </div>
        
        <div style="margin-top: 40px; text-align: center; color: #6c757d;">
            <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
        </div>
    </body>
    </html>
    """
    
    return html_content

@login_required(login_url='Connexion')
def rapport_dossier_interface(request):
    """
    Interface pour afficher la liste des dossiers et générer leurs rapports d'activités internes
    """
    try:
        # Récupérer les dossiers du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            dossiers = dossier.objects.filter(cabinet=user_cabinet).select_related(
                'client', 'type_affaire', 'juridiction'
            ).order_by('-date_ouverture')
        else:
            dossiers = dossier.objects.all().select_related(
                'client', 'type_affaire', 'juridiction'
            ).order_by('-date_ouverture')
        
        # Calculer les statistiques pour chaque dossier
        dossiers_data = []
        for dos in dossiers:
            # Compter les activités internes liées à ce dossier
            from Dossier.models import ActiviteHeure
            activites_count = ActiviteHeure.objects.filter(dossier=dos).count()
            
            # Dernière activité interne
            derniere_activite = ActiviteHeure.objects.filter(
                dossier=dos
            ).order_by('-date_activite').first()
            
            # Activités récentes (7 derniers jours)
            date_limite = datetime.now().date() - timedelta(days=7)
            activites_recentes = ActiviteHeure.objects.filter(
                dossier=dos,
                date_activite__gte=date_limite
            ).count()
            
            # Récupérer l'avocat principal
            from Dossier.models import AvocatDossier
            avocat_principal = AvocatDossier.objects.filter(
                dossier=dos, role='Principal'
            ).first()
            
            # Calculer les heures totales et le montant facturé
            activites_dossier = ActiviteHeure.objects.filter(dossier=dos)
            heures_totales = sum(float(act.duree_heures) for act in activites_dossier)
            activites_facturees = activites_dossier.filter(facturee=True).count()
            
            dossiers_data.append({
                'dossier': dos,
                'client_nom': f"{dos.client.nom} {dos.client.prenom}",
                'type_affaire': dos.type_affaire.nom_type if dos.type_affaire else 'Non défini',
                'avocat_principal': f"{avocat_principal.avocat.nom} {avocat_principal.avocat.prenom}" if avocat_principal else 'Non assigné',
                'activites_count': activites_count,
                'activites_recentes': activites_recentes,
                'heures_totales': heures_totales,
                'activites_facturees': activites_facturees,
                'derniere_activite': derniere_activite.date_activite if derniere_activite else None,
                'derniere_activite_description': derniere_activite.description[:50] + '...' if derniere_activite and len(derniere_activite.description) > 50 else (derniere_activite.description if derniere_activite else 'Aucune activité')
            })
        
        context = {
            'dossiers_data': dossiers_data,
            'total_dossiers': len(dossiers_data),
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_dossier.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_dossier_interface: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def rapport_activites_dossier(request, dossier_id):
    """
    Génère un rapport détaillé des activités internes d'un dossier spécifique
    """
    try:
        # Récupérer le dossier
        dossier_obj = get_object_or_404(dossier, id=dossier_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and dossier_obj.cabinet != user_cabinet:
            return HttpResponse("Accès non autorisé", status=403)
        
        # Récupérer les paramètres de filtrage
        periode = request.GET.get('periode', '30')  # 30 jours par défaut
        avocat_filter = request.GET.get('avocat', 'all')
        facturee_filter = request.GET.get('facturee', 'all')
        format_rapport = request.GET.get('format', 'html')
        
        # Calculer la date limite
        if periode == 'all':
            date_limite = None
        else:
            jours = int(periode)
            date_limite = datetime.now().date() - timedelta(days=jours)
        
        # Récupérer les activités internes
        from Dossier.models import ActiviteHeure
        activites_query = ActiviteHeure.objects.filter(
            dossier=dossier_obj
        ).select_related('avocat').order_by('-date_activite')
        
        if date_limite:
            activites_query = activites_query.filter(date_activite__gte=date_limite)
        
        if avocat_filter != 'all':
            activites_query = activites_query.filter(avocat_id=avocat_filter)
            
        if facturee_filter != 'all':
            facturee_bool = facturee_filter == 'true'
            activites_query = activites_query.filter(facturee=facturee_bool)
        
        activites = activites_query
        
        # Préparer les données pour le rapport
        rapport_data = preparer_donnees_rapport_activites_dossier(
            dossier_obj, activites, periode, avocat_filter, request
        )
        
        if format_rapport == 'pdf':
            # Générer le PDF
            return generer_pdf_activites_dossier(rapport_data, dossier_obj)
        else:
            # Récupérer la liste des avocats pour le filtre
            from Agent.models import agent
            avocats = agent.objects.filter(company=request.user.company) if hasattr(request.user, 'company') else agent.objects.all()
            
            # Afficher en HTML
            return render(request, 'admin_template/rapport_activites_dossier.html', {
                'rapport_data': rapport_data,
                'dossier': dossier_obj,
                'activites': activites,
                'periode': periode,
                'avocat_filter': avocat_filter,
                'facturee_filter': facturee_filter,
                'avocats': avocats
            })
        
    except Exception as e:
        logger.error(f"Erreur génération rapport activités dossier: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def activites_dossier_ajax(request, dossier_id):
    """
    Retourne les activités internes d'un dossier via AJAX pour affichage dynamique
    """
    try:
        # Récupérer le dossier
        dossier_obj = get_object_or_404(dossier, id=dossier_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and dossier_obj.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Paramètres de pagination
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        offset = (page - 1) * per_page
        
        # Récupérer les activités internes
        from Dossier.models import ActiviteHeure
        activites_query = ActiviteHeure.objects.filter(
            dossier=dossier_obj
        ).select_related('avocat').order_by('-date_activite')
        
        total_activites = activites_query.count()
        activites = activites_query[offset:offset + per_page]
        
        activites_data = []
        for activite in activites:
            # Calculer le coût si possible
            cout_activite = 0
            try:
                cout_activite = activite.calculer_cout_activite()
            except:
                pass
            
            activites_data.append({
                'id': activite.id,
                'date_activite': activite.date_activite.strftime('%d/%m/%Y'),
                'avocat': f"{activite.avocat.nom} {activite.avocat.prenom}" if activite.avocat else 'Non assigné',
                'duree_heures': float(activite.duree_heures),
                'description': activite.description,
                'facturee': activite.facturee,
                'cout_estime': float(cout_activite) if cout_activite else 0,
                'statut_facturation': 'Facturée' if activite.facturee else 'Non facturée',
                'color': 'success' if activite.facturee else 'warning',
                'icon': 'mdi-check-circle' if activite.facturee else 'mdi-clock'
            })
        
        return JsonResponse({
            'success': True,
            'activites': activites_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total_activites,
                'pages': (total_activites + per_page - 1) // per_page,
                'has_next': offset + per_page < total_activites,
                'has_prev': page > 1
            }
        })
        
    except Exception as e:
        logger.error(f"Erreur récupération activités dossier AJAX: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

@login_required(login_url='Connexion')
def statistiques_activites_dossiers(request):
    """
    Génère des statistiques globales sur les activités internes des dossiers
    """
    try:
        # Récupérer les dossiers du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            dossiers_ids = list(dossier.objects.filter(cabinet=user_cabinet).values_list('id', flat=True))
        else:
            dossiers_ids = list(dossier.objects.all().values_list('id', flat=True))
        
        # Calculer les statistiques
        from Dossier.models import ActiviteHeure
        from django.db.models import Count, Sum, Q
        
        # Activités par avocat
        activites_par_avocat = ActiviteHeure.objects.filter(
            dossier_id__in=dossiers_ids
        ).values('avocat__nom', 'avocat__prenom').annotate(
            count=Count('id'),
            heures_totales=Sum('duree_heures')
        ).order_by('-count')
        
        # Activités par période (30 derniers jours)
        date_limite = datetime.now().date() - timedelta(days=30)
        activites_recentes = ActiviteHeure.objects.filter(
            dossier_id__in=dossiers_ids,
            date_activite__gte=date_limite
        ).extra(
            select={'day': 'DATE(date_activite)'}
        ).values('day').annotate(
            count=Count('id'),
            heures=Sum('duree_heures')
        ).order_by('day')
        
        # Top 10 des dossiers les plus actifs
        dossiers_actifs = ActiviteHeure.objects.filter(
            dossier_id__in=dossiers_ids
        ).values('dossier_id').annotate(
            count=Count('id'),
            heures_totales=Sum('duree_heures')
        ).order_by('-count')[:10]
        
        # Enrichir avec les informations des dossiers
        dossiers_actifs_data = []
        for item in dossiers_actifs:
            try:
                dos = dossier.objects.get(id=item['dossier_id'])
                dossiers_actifs_data.append({
                    'dossier': dos,
                    'count': item['count'],
                    'heures_totales': float(item['heures_totales']) if item['heures_totales'] else 0,
                    'client_nom': f"{dos.client.nom} {dos.client.prenom}",
                    'numero_reference': dos.numero_reference_dossier
                })
            except dossier.DoesNotExist:
                continue
        
        # Statistiques de facturation
        activites_facturees = ActiviteHeure.objects.filter(
            dossier_id__in=dossiers_ids,
            facturee=True
        ).count()
        
        activites_non_facturees = ActiviteHeure.objects.filter(
            dossier_id__in=dossiers_ids,
            facturee=False
        ).count()
        
        # Heures totales
        heures_totales = ActiviteHeure.objects.filter(
            dossier_id__in=dossiers_ids
        ).aggregate(total=Sum('duree_heures'))['total'] or 0
        
        statistiques = {
            'total_activites': ActiviteHeure.objects.filter(dossier_id__in=dossiers_ids).count(),
            'activites_ce_mois': ActiviteHeure.objects.filter(
                dossier_id__in=dossiers_ids,
                date_activite__month=datetime.now().month,
                date_activite__year=datetime.now().year
            ).count(),
            'activites_cette_semaine': ActiviteHeure.objects.filter(
                dossier_id__in=dossiers_ids,
                date_activite__gte=datetime.now().date() - timedelta(days=7)
            ).count(),
            'activites_aujourd_hui': ActiviteHeure.objects.filter(
                dossier_id__in=dossiers_ids,
                date_activite=datetime.now().date()
            ).count(),
            'activites_facturees': activites_facturees,
            'activites_non_facturees': activites_non_facturees,
            'heures_totales': float(heures_totales),
            'activites_par_avocat': list(activites_par_avocat),
            'activites_recentes': list(activites_recentes),
            'dossiers_actifs': dossiers_actifs_data
        }
        
        context = {
            'statistiques': statistiques,
            'total_dossiers': len(dossiers_ids),
            'today': date.today()
        }
        
        return render(request, 'admin_template/statistiques_activites_dossiers.html', context)
        
    except Exception as e:
        logger.error(f"Erreur statistiques activités dossiers: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_activites_dossier(dossier_obj, activites, periode, avocat_filter, request):
    """
    Prépare les données pour le rapport d'activités internes d'un dossier
    """
    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Statistiques des activités
    activites_par_avocat = {}
    activites_par_jour = {}
    heures_par_jour = {}
    total_heures = 0
    activites_facturees = 0
    activites_non_facturees = 0
    
    for activite in activites:
        # Par avocat
        avocat_nom = f"{activite.avocat.nom} {activite.avocat.prenom}" if activite.avocat else 'Non assigné'
        if avocat_nom not in activites_par_avocat:
            activites_par_avocat[avocat_nom] = {'count': 0, 'heures': 0}
        activites_par_avocat[avocat_nom]['count'] += 1
        activites_par_avocat[avocat_nom]['heures'] += float(activite.duree_heures)
        
        # Par jour
        jour = activite.date_activite.strftime('%d/%m/%Y')
        activites_par_jour[jour] = activites_par_jour.get(jour, 0) + 1
        heures_par_jour[jour] = heures_par_jour.get(jour, 0) + float(activite.duree_heures)
        
        # Totaux
        total_heures += float(activite.duree_heures)
        if activite.facturee:
            activites_facturees += 1
        else:
            activites_non_facturees += 1
    
    # Récupérer l'avocat principal
    from Dossier.models import AvocatDossier
    avocat_principal = AvocatDossier.objects.filter(
        dossier=dossier_obj, role='Principal'
    ).first()
    
    # Préparer les données des activités
    activites_data = []
    for activite in activites:
        # Calculer le coût si possible
        cout_activite = 0
        try:
            cout_activite = activite.calculer_cout_activite()
        except:
            pass
        
        activites_data.append({
            'date_activite': activite.date_activite.strftime('%d/%m/%Y'),
            'avocat': f"{activite.avocat.nom} {activite.avocat.prenom}" if activite.avocat else 'Non assigné',
            'duree_heures': float(activite.duree_heures),
            'description': activite.description,
            'facturee': activite.facturee,
            'cout_estime': float(cout_activite) if cout_activite else 0,
            'statut_facturation': 'Facturée' if activite.facturee else 'Non facturée',
            'color': 'success' if activite.facturee else 'warning',
            'icon': 'mdi-check-circle' if activite.facturee else 'mdi-clock'
        })
    
    data = {
        "rapport": {
            "today": today,
            "periode": periode,
            "avocat_filter": avocat_filter,
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
        },
        "dossier": {
            "id": dossier_obj.id,
            "numero_reference": safe_str(dossier_obj.numero_reference_dossier),
            "titre": safe_str(dossier_obj.titre),
            "client_nom": f"{dossier_obj.client.nom} {dossier_obj.client.prenom}",
            "type_affaire": safe_str(dossier_obj.type_affaire.nom_type) if dossier_obj.type_affaire else 'Non défini',
            "statut": safe_str(dossier_obj.statut_dossier),
            "date_ouverture": dossier_obj.date_ouverture.strftime('%d/%m/%Y') if dossier_obj.date_ouverture else '',
            "avocat_principal": f"{avocat_principal.avocat.nom} {avocat_principal.avocat.prenom}" if avocat_principal else 'Non assigné',
            "juridiction": safe_str(dossier_obj.juridiction.nom) if dossier_obj.juridiction else 'Non définie'
        },
        "cabinet": {
            "nom": safe_str(dossier_obj.cabinet.nom) if dossier_obj.cabinet else safe_str(request.user.cabinet.nom),
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "activites": activites_data,
        "statistiques": {
            "total_activites": len(activites_data),
            "total_heures": total_heures,
            "activites_facturees": activites_facturees,
            "activites_non_facturees": activites_non_facturees,
            "activites_par_avocat": activites_par_avocat,
            "activites_par_jour": activites_par_jour,
            "heures_par_jour": heures_par_jour,
            "periode_affichee": f"{periode} derniers jours" if periode != 'all' else 'Toutes les activités'
        }
    }
    
    return data

def generer_pdf_activites_dossier(rapport_data, dossier_obj):
    """
    Génère un PDF du rapport d'activités d'un dossier
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        filename = f"activites_dossier_{dossier_obj.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return jsreport_service.generate_pdf_response(
            template_name="rapport_activites_dossier",
            data=rapport_data,
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Erreur génération PDF activités dossier: {str(e)}")
        # Mode démo HTML
        return generer_html_demo_activites_dossier(rapport_data, dossier_obj)

def generer_html_demo_activites_dossier(rapport_data, dossier_obj):
    """
    Génère un rapport HTML démo des activités d'un dossier
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rapport d'Activités - Dossier {rapport_data['dossier']['numero_reference']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
            .section {{ margin: 20px 0; }}
            .stats {{ display: flex; justify-content: space-around; background: #f8f9fa; padding: 20px; margin: 20px 0; }}
            .stat-item {{ text-align: center; }}
            .activity-item {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0; }}
            .activity-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }}
            .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <div class="demo-notice">
            <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo.
        </div>
        
        <div class="header">
            <h1>📋 Rapport d'Activités du Dossier</h1>
            <h2>{rapport_data['dossier']['numero_reference']} - {rapport_data['dossier']['titre']}</h2>
            <p><strong>Client:</strong> {rapport_data['dossier']['client_nom']}</p>
            <p>Généré le {rapport_data['rapport']['date_generation']} par {rapport_data['rapport']['genere_par']}</p>
        </div>
        
        <div class="section">
            <h3>📊 Statistiques</h3>
            <div class="stats">
                <div class="stat-item">
                    <h3>{rapport_data['statistiques']['total_activites']}</h3>
                    <p>Total Activités</p>
                </div>
                <div class="stat-item">
                    <h3>{len(rapport_data['statistiques']['activites_par_type'])}</h3>
                    <p>Types d'Activités</p>
                </div>
                <div class="stat-item">
                    <h3>{len(rapport_data['statistiques']['activites_par_user'])}</h3>
                    <p>Utilisateurs Actifs</p>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h3>📋 Informations du Dossier</h3>
            <table>
                <tr><th>Numéro de référence</th><td>{rapport_data['dossier']['numero_reference']}</td></tr>
                <tr><th>Titre</th><td>{rapport_data['dossier']['titre']}</td></tr>
                <tr><th>Client</th><td>{rapport_data['dossier']['client_nom']}</td></tr>
                <tr><th>Type d'affaire</th><td>{rapport_data['dossier']['type_affaire']}</td></tr>
                <tr><th>Statut</th><td>{rapport_data['dossier']['statut']}</td></tr>
                <tr><th>Avocat principal</th><td>{rapport_data['dossier']['avocat_principal']}</td></tr>
                <tr><th>Date d'ouverture</th><td>{rapport_data['dossier']['date_ouverture']}</td></tr>
            </table>
        </div>
        
        <div class="section">
            <h3>🔄 Liste des Activités ({rapport_data['statistiques']['periode_affichee']})</h3>
    """
    
    for activite in rapport_data['activites']:
        html_content += f"""
            <div class="activity-item">
                <div class="activity-header">
                    <strong>{activite['title']}</strong>
                    <span>{activite['timestamp']}</span>
                </div>
                <p><strong>Action:</strong> {activite['action']} | <strong>Par:</strong> {activite['user']}</p>
                <p>{activite['description']}</p>
            </div>
        """
    
    html_content += """
        </div>
        
        <div style="margin-top: 40px; text-align: center; color: #6c757d;">
            <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
        </div>
    </body>
    </html>
    """
    
    return HttpResponse(html_content, content_type='text/html')

@login_required(login_url='Connexion')
def rapport_activites_internes(request):
    """
    Rapport pour les activités internes configurées dans Structure.Activite
    """
    try:
        # Récupérer les activités du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            from Structure.models import Activite
            activites = Activite.objects.filter(cabinet=user_cabinet).order_by('-date_activite')
        else:
            from Structure.models import Activite
            activites = Activite.objects.all().order_by('-date_activite')
        
        # Calculer les statistiques pour chaque activité
        activites_data = []
        for activite in activites:
            # Compter combien de fois cette activité a été utilisée dans les dossiers
            from Dossier.models import ActiviteHeure
            utilisations = ActiviteHeure.objects.filter(
                dossier__cabinet=user_cabinet if user_cabinet else None
            ).count()
            
            # Calculer les heures totales pour cette activité
            heures_totales = 0
            revenus_potentiels = 0
            try:
                # Rechercher les utilisations de cette activité par nom/description
                utilisations_activite = ActiviteHeure.objects.filter(
                    description__icontains=activite.nom_activite,
                    dossier__cabinet=user_cabinet if user_cabinet else None
                )
                utilisations = utilisations_activite.count()
                heures_totales = sum(float(u.duree_heures) for u in utilisations_activite)
                
                # Calculer les revenus potentiels
                for utilisation in utilisations_activite:
                    try:
                        cout = utilisation.calculer_cout_activite()
                        if cout:
                            revenus_potentiels += float(cout)
                    except:
                        pass
            except:
                pass
            
            activites_data.append({
                'activite': activite,
                'utilisations': utilisations,
                'heures_totales': heures_totales,
                'revenus_potentiels': revenus_potentiels,
                'derniere_utilisation': utilisations_activite.order_by('-date_activite').first() if 'utilisations_activite' in locals() else None
            })
        
        # Calculer les statistiques globales
        total_activites = len(activites_data)
        total_utilisations = sum(item['utilisations'] for item in activites_data)
        total_heures = sum(item['heures_totales'] for item in activites_data)
        total_revenus = sum(item['revenus_potentiels'] for item in activites_data)
        
        # Activités les plus utilisées
        activites_populaires = sorted(activites_data, key=lambda x: x['utilisations'], reverse=True)[:5]
        
        # Activités les plus rentables
        activites_rentables = sorted(activites_data, key=lambda x: x['revenus_potentiels'], reverse=True)[:5]
        
        context = {
            'activites_data': activites_data,
            'total_activites': total_activites,
            'total_utilisations': total_utilisations,
            'total_heures': total_heures,
            'total_revenus': total_revenus,
            'activites_populaires': activites_populaires,
            'activites_rentables': activites_rentables,
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_activites_internes.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_activites_internes: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

@login_required(login_url='Connexion')
def details_activite_interne_ajax(request, activite_id):
    """
    Retourne les détails d'une activité interne via AJAX
    """
    try:
        from Structure.models import Activite
        activite = get_object_or_404(Activite, id=activite_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and activite.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Récupérer les utilisations de cette activité
        from Dossier.models import ActiviteHeure
        utilisations = ActiviteHeure.objects.filter(
            description__icontains=activite.nom_activite,
            dossier__cabinet=user_cabinet if user_cabinet else None
        ).select_related('dossier', 'avocat').order_by('-date_activite')[:20]
        
        utilisations_data = []
        for utilisation in utilisations:
            cout_estime = 0
            try:
                cout_estime = utilisation.calculer_cout_activite()
            except:
                pass
            
            utilisations_data.append({
                'id': utilisation.id,
                'date_activite': utilisation.date_activite.strftime('%d/%m/%Y'),
                'dossier_titre': utilisation.dossier.titre,
                'dossier_numero': utilisation.dossier.numero_reference_dossier or f"#{utilisation.dossier.id}",
                'client_nom': f"{utilisation.dossier.client.nom} {utilisation.dossier.client.prenom}",
                'avocat': f"{utilisation.avocat.nom} {utilisation.avocat.prenom}" if utilisation.avocat else 'Non assigné',
                'duree_heures': float(utilisation.duree_heures),
                'description': utilisation.description,
                'facturee': utilisation.facturee,
                'cout_estime': float(cout_estime) if cout_estime else 0
            })
        
        # Statistiques de l'activité
        total_utilisations = len(utilisations_data)
        total_heures = sum(u['duree_heures'] for u in utilisations_data)
        total_revenus = sum(u['cout_estime'] for u in utilisations_data)
        utilisations_facturees = sum(1 for u in utilisations_data if u['facturee'])
        
        return JsonResponse({
            'success': True,
            'activite': {
                'id': activite.id,
                'nom': activite.nom_activite,
                'date_creation': activite.date_activite.strftime('%d/%m/%Y %H:%M'),
                'cabinet': activite.cabinet.nom
            },
            'statistiques': {
                'total_utilisations': total_utilisations,
                'total_heures': total_heures,
                'total_revenus': total_revenus,
                'utilisations_facturees': utilisations_facturees,
                'taux_facturation': (utilisations_facturees / total_utilisations * 100) if total_utilisations > 0 else 0
            },
            'utilisations': utilisations_data
        })
        
    except Exception as e:
        logger.error(f"Erreur détails activité interne AJAX: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

@login_required(login_url='Connexion')
def generer_rapport_activite_interne(request):
    """
    Génère un rapport PDF pour une activité interne spécifique
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Méthode non autorisée'}, status=405)
    
    try:
        activite_id = request.POST.get('activite_id')
        format_rapport = request.POST.get('format', 'pdf')
        
        if not activite_id:
            return JsonResponse({'error': 'Activité non spécifiée'}, status=400)
        
        from Structure.models import Activite
        activite = get_object_or_404(Activite, id=activite_id)
        
        # Vérifier les permissions
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet and activite.cabinet != user_cabinet:
            return JsonResponse({'error': 'Accès non autorisé'}, status=403)
        
        # Préparer les données pour le rapport
        rapport_data = preparer_donnees_rapport_activite_interne(activite, request)
        
        if format_rapport == 'pdf':
            # Générer le PDF
            return generer_pdf_activite_interne(rapport_data, activite)
        else:
            # Mode démo HTML
            demo_url = generer_html_demo_activite_interne(rapport_data, activite)
            return JsonResponse({
                'success': True,
                'rapport_url': demo_url,
                'activite_nom': activite.nom_activite,
                'format': format_rapport,
                'mode': 'demo'
            })
            
    except Exception as e:
        logger.error(f"Erreur génération rapport activité interne: {str(e)}")
        return JsonResponse({'error': f'Erreur: {str(e)}'}, status=500)

def preparer_donnees_rapport_activite_interne(activite, request):
    """
    Prépare les données pour le rapport d'une activité interne
    """
    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Récupérer les utilisations de cette activité
    from Dossier.models import ActiviteHeure
    user_cabinet = getattr(request.user, 'cabinet', None)
    
    utilisations = ActiviteHeure.objects.filter(
        description__icontains=activite.nom_activite,
        dossier__cabinet=user_cabinet if user_cabinet else None
    ).select_related('dossier', 'avocat').order_by('-date_activite')
    
    # Préparer les données des utilisations
    utilisations_data = []
    total_heures = 0
    total_revenus = 0
    utilisations_facturees = 0
    
    for utilisation in utilisations:
        cout_estime = 0
        try:
            cout_estime = utilisation.calculer_cout_activite()
        except:
            pass
        
        utilisations_data.append({
            'date_activite': utilisation.date_activite.strftime('%d/%m/%Y'),
            'dossier_titre': utilisation.dossier.titre,
            'dossier_numero': utilisation.dossier.numero_reference_dossier or f"#{utilisation.dossier.id}",
            'client_nom': f"{utilisation.dossier.client.nom} {utilisation.dossier.client.prenom}",
            'avocat': f"{utilisation.avocat.nom} {utilisation.avocat.prenom}" if utilisation.avocat else 'Non assigné',
            'duree_heures': float(utilisation.duree_heures),
            'description': utilisation.description,
            'facturee': utilisation.facturee,
            'cout_estime': float(cout_estime) if cout_estime else 0
        })
        
        total_heures += float(utilisation.duree_heures)
        total_revenus += float(cout_estime) if cout_estime else 0
        if utilisation.facturee:
            utilisations_facturees += 1
    
    data = {
        "rapport": {
            "today": today,
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "genere_par": f"{request.user.first_name} {request.user.last_name}" if request.user.first_name else request.user.username
        },
        "activite": {
            "id": activite.id,
            "nom": safe_str(activite.nom_activite),
            "date_creation": activite.date_activite.strftime('%d/%m/%Y %H:%M'),
            "cabinet": safe_str(activite.cabinet.nom)
        },
        "cabinet": {
            "nom": safe_str(activite.cabinet.nom),
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "utilisations": utilisations_data,
        "statistiques": {
            "total_utilisations": len(utilisations_data),
            "total_heures": total_heures,
            "total_revenus": total_revenus,
            "utilisations_facturees": utilisations_facturees,
            "taux_facturation": (utilisations_facturees / len(utilisations_data) * 100) if len(utilisations_data) > 0 else 0
        }
    }
    
    return data

def generer_pdf_activite_interne(rapport_data, activite):
    """
    Génère un PDF du rapport d'une activité interne
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        filename = f"activite_interne_{activite.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        return jsreport_service.generate_pdf_response(
            template_name="rapport_activite",  # Utiliser le template existant
            data=rapport_data,
            filename=filename,
            disposition="inline"  # Affichage dans le navigateur
        )
        
    except Exception as e:
        logger.error(f"Erreur génération PDF activité interne: {str(e)}")
        # Mode démo HTML
        return generer_html_demo_activite_interne(rapport_data, activite)

def generer_html_demo_activite_interne(rapport_data, activite):
    """
    Génère un rapport HTML démo d'une activité interne
    """
    try:
        import os
        
        # Créer le dossier rapports s'il n'existe pas
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Rapport Activité Interne - {rapport_data['activite']['nom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
                .section {{ margin: 20px 0; }}
                .stats {{ display: flex; justify-content: space-around; background: #f8f9fa; padding: 20px; margin: 20px 0; }}
                .stat-item {{ text-align: center; }}
                .utilisation-item {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0; }}
                .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <div class="demo-notice">
                <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo.
            </div>
            
            <div class="header">
                <h1>📋 Rapport Activité Interne</h1>
                <h2>{rapport_data['activite']['nom']}</h2>
                <p>Généré le {rapport_data['rapport']['date_generation']} par {rapport_data['rapport']['genere_par']}</p>
            </div>
            
            <div class="section">
                <h3>📊 Statistiques</h3>
                <div class="stats">
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['total_utilisations']}</h3>
                        <p>Total Utilisations</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['total_heures']:.1f}h</h3>
                        <p>Heures Totales</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['total_revenus']:.2f} USD</h3>
                        <p>Revenus Générés</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['taux_facturation']:.1f}%</h3>
                        <p>Taux Facturation</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>📋 Informations de l'Activité</h3>
                <table>
                    <tr><th>Nom</th><td>{rapport_data['activite']['nom']}</td></tr>
                    <tr><th>Date de création</th><td>{rapport_data['activite']['date_creation']}</td></tr>
                    <tr><th>Cabinet</th><td>{rapport_data['activite']['cabinet']}</td></tr>
                    <tr><th>Total utilisations</th><td>{rapport_data['statistiques']['total_utilisations']}</td></tr>
                </table>
            </div>
            
            <div class="section">
                <h3>🔄 Utilisations de l'Activité</h3>
        """
        
        for utilisation in rapport_data['utilisations']:
            statut = "Facturée" if utilisation['facturee'] else "Non facturée"
            color = "success" if utilisation['facturee'] else "warning"
            
            html_content += f"""
                <div class="utilisation-item">
                    <div style="display: flex; justify-content: between; align-items: center;">
                        <div>
                            <strong>{utilisation['dossier_titre']}</strong> ({utilisation['dossier_numero']})
                            <br><small>Client: {utilisation['client_nom']}</small>
                            <br><small>Avocat: {utilisation['avocat']}</small>
                        </div>
                        <div style="text-align: right;">
                            <strong>{utilisation['duree_heures']}h</strong>
                            <br><span style="color: {'green' if utilisation['facturee'] else 'orange'}">{statut}</span>
                            <br><small>{utilisation['cout_estime']:.2f} USD</small>
                        </div>
                    </div>
                    <p style="margin-top: 10px;"><em>{utilisation['description']}</em></p>
                    <small style="color: #666;">Date: {utilisation['date_activite']}</small>
                </div>
            """
        
        html_content += """
            </div>
            
            <div style="margin-top: 40px; text-align: center; color: #6c757d;">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        # Nom du fichier
        filename = f"demo_activite_interne_{activite.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération rapport démo activité interne: {str(e)}")
        return None


@login_required(login_url='Connexion')
def referentielle_caisse(request):
    """
    Référentielle de la caisse - Rapport des services du cabinet
    """
    try:
        # Récupérer les services du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            messages.error(request, "Aucun cabinet associé à votre compte.")
            return redirect('Dashboard_Cabinet_Administrateur')
        
        # Récupérer tous les services du cabinet
        services_cabinet = ServiceCabinet.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter')
        
        # Statistiques générales
        total_services = services_cabinet.count()
        services_recents = services_cabinet.filter(
            date_ajouter__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Services les plus récents (top 5)
        services_top = services_cabinet[:5]
        
        context = {
            'services_cabinet': services_cabinet,
            'total_services': total_services,
            'services_recents': services_recents,
            'services_top': services_top,
            'cabinet': user_cabinet,
        }
        
        return render(request, 'admin_template/referentiel_caisse.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans referentielle_caisse: {str(e)}")
        messages.error(request, f"Erreur lors du chargement du référentiel: {str(e)}")
        return redirect('Dashboard_Cabinet_Administrateur')


@login_required(login_url='Connexion')
def details_service_cabinet_ajax(request, service_id):
    """
    Récupérer les détails d'un service cabinet via AJAX
    """
    try:
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            return JsonResponse({'error': 'Cabinet non trouvé'}, status=404)
        
        service = get_object_or_404(ServiceCabinet, id=service_id, cabinet=user_cabinet)
        
        # Statistiques d'utilisation du service (si applicable)
        # Ici on peut ajouter des statistiques sur l'utilisation du service
        # dans les mouvements de caisse ou autres modules
        
        data = {
            'id': service.id,
            'nom_service': service.nom_service,
            'date_ajouter': service.date_ajouter.strftime('%d/%m/%Y à %H:%M') if service.date_ajouter else 'Non définie',
            'cabinet': service.cabinet.nom_cabinet if service.cabinet else 'Non défini',
            # Ajouter d'autres statistiques si nécessaire
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f"Erreur details_service_cabinet_ajax: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='Connexion')
def generer_rapport_referentiel_caisse(request):
    """
    Générer un rapport PDF du référentiel de la caisse
    """
    try:
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            return JsonResponse({'error': 'Cabinet non trouvé'}, status=404)
        
        # Récupérer les services
        services_cabinet = ServiceCabinet.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter')
        
        # Créer le PDF
        filename = f"referentiel_caisse_{user_cabinet.nom_cabinet}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(settings.MEDIA_ROOT, 'rapports', filename)
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Générer le PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Titre
        story.append(Paragraph(f"Référentiel de la Caisse - {user_cabinet.nom_cabinet}", title_style))
        story.append(Spacer(1, 20))
        
        # Date de génération
        story.append(Paragraph(f"Généré le {timezone.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Statistiques
        story.append(Paragraph(f"Nombre total de services: {services_cabinet.count()}", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Tableau des services
        if services_cabinet.exists():
            data = [['#', 'Nom du Service', 'Date d\'Ajout']]
            
            for i, service in enumerate(services_cabinet, 1):
                data.append([
                    str(i),
                    service.nom_service,
                    service.date_ajouter.strftime('%d/%m/%Y') if service.date_ajouter else 'Non définie'
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("Aucun service trouvé.", styles['Normal']))
        
        # Construire le PDF
        doc.build(story)
        
        return JsonResponse({
            'success': True,
            'message': 'Rapport généré avec succès',
            'download_url': f"/media/rapports/{filename}"
        })
        
    except Exception as e:
        logger.error(f"Erreur génération rapport référentiel caisse: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='Connexion')
def referentielle_caisse(request):
    """
    Référentielle de la caisse - Rapport des services du cabinet
    """
    try:
        # Récupérer les services du cabinet
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            messages.error(request, "Aucun cabinet associé à votre compte.")
            return redirect('Dashboard_Cabinet_Administrateur')
        
        # Récupérer tous les services du cabinet
        services_cabinet = ServiceCabinet.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter')
        
        # Statistiques générales
        total_services = services_cabinet.count()
        services_recents = services_cabinet.filter(
            date_ajouter__gte=timezone.now() - timedelta(days=30)
        ).count()
        
        # Services les plus récents (top 5)
        services_top = services_cabinet[:5]
        
        context = {
            'services_cabinet': services_cabinet,
            'total_services': total_services,
            'services_recents': services_recents,
            'services_top': services_top,
            'cabinet': user_cabinet,
        }
        
        return render(request, 'admin_template/referentiel_caisse.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans referentielle_caisse: {str(e)}")
        messages.error(request, f"Erreur lors du chargement du référentiel: {str(e)}")
        return redirect('Dashboard_Cabinet_Administrateur')


@login_required(login_url='Connexion')
def details_service_cabinet_ajax(request, service_id):
    """
    Récupérer les détails d'un service cabinet via AJAX
    """
    try:
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            return JsonResponse({'error': 'Cabinet non trouvé'}, status=404)
        
        service = get_object_or_404(ServiceCabinet, id=service_id, cabinet=user_cabinet)
        
        # Statistiques d'utilisation du service (si applicable)
        # Ici on peut ajouter des statistiques sur l'utilisation du service
        # dans les mouvements de caisse ou autres modules
        
        data = {
            'id': service.id,
            'nom_service': service.nom_service,
            'date_ajouter': service.date_ajouter.strftime('%d/%m/%Y à %H:%M') if service.date_ajouter else 'Non définie',
            'cabinet': service.cabinet.nom_cabinet if service.cabinet else 'Non défini',
            # Ajouter d'autres statistiques si nécessaire
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        logger.error(f"Erreur details_service_cabinet_ajax: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='Connexion')
def generer_rapport_referentiel_caisse(request):
    """
    Générer un rapport PDF du référentiel de la caisse
    """
    try:
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            return JsonResponse({'error': 'Cabinet non trouvé'}, status=404)
        
        # Récupérer les services
        services_cabinet = ServiceCabinet.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter')
        
        # Créer le PDF
        filename = f"referentiel_caisse_{user_cabinet.nom_cabinet}_{timezone.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(settings.MEDIA_ROOT, 'rapports', filename)
        
        # Créer le répertoire s'il n'existe pas
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Générer le PDF
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center
        )
        
        # Titre
        story.append(Paragraph(f"Référentiel de la Caisse - {user_cabinet.nom_cabinet}", title_style))
        story.append(Spacer(1, 20))
        
        # Date de génération
        story.append(Paragraph(f"Généré le {timezone.now().strftime('%d/%m/%Y à %H:%M')}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Statistiques
        story.append(Paragraph(f"Nombre total de services: {services_cabinet.count()}", styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Tableau des services
        if services_cabinet.exists():
            data = [['#', 'Nom du Service', 'Date d\'Ajout']]
            
            for i, service in enumerate(services_cabinet, 1):
                data.append([
                    str(i),
                    service.nom_service,
                    service.date_ajouter.strftime('%d/%m/%Y') if service.date_ajouter else 'Non définie'
                ])
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 14),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
        else:
            story.append(Paragraph("Aucun service trouvé.", styles['Normal']))
        
        # Construire le PDF
        doc.build(story)
        
        return JsonResponse({
            'success': True,
            'message': 'Rapport généré avec succès',
            'download_url': f"/media/rapports/{filename}"
        })
        
    except Exception as e:
        logger.error(f"Erreur génération rapport référentiel caisse: {str(e)}")
        return JsonResponse({'error': str(e)}, status=500)

@login_required(login_url='Connexion')
def rapport_caisse_interface(request):
    """
    Interface pour le rapport de caisse avec sélection de plage de dates
    """
    try:
        from paiement.models import Paiement
        from parametre.models import taux
        from django.db.models import Sum
        from decimal import Decimal
        
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            # Si l'utilisateur n'a pas de cabinet, prendre le premier disponible
            from Structure.models import Cabinet
            user_cabinet = Cabinet.objects.first()
            
        if not user_cabinet:
            return HttpResponse("Aucun cabinet trouvé", status=404)
        
        # Récupérer le taux de change actuel
        taux_obj = taux.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter').first()
        taux_change = Decimal(taux_obj.cout) if taux_obj else Decimal('2500.0')
        
        # Statistiques générales pour l'affichage initial
        if user_cabinet:
            total_entrees = Paiement.objects.filter(
                cabinet=user_cabinet,
                type_operation="ENTREE"
            ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0
            
            total_sorties = Paiement.objects.filter(
                cabinet=user_cabinet,
                type_operation="SORTIE"
            ).aggregate(total=Sum("montant_payer_dollars"))["total"] or 0
            
            solde_actuel = total_entrees - total_sorties
            
        else:
            total_entrees = total_sorties = solde_actuel = 0
        
        context = {
            'total_entrees': total_entrees,
            'total_entrees_fc': total_entrees * taux_change,
            'total_sorties': total_sorties,
            'total_sorties_fc': total_sorties * taux_change,
            'solde_actuel': solde_actuel,
            'solde_actuel_fc': solde_actuel * taux_change,
            'taux_change': taux_change,
            'today': timezone.now().date(),
        }
        
        return render(request, 'admin_template/rapport_caisse.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_caisse_interface: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)


@login_required(login_url='Connexion')
def generer_rapport_caisse(request):
    """
    Générer un rapport de caisse pour une plage de dates donnée
    """
    try:
        from paiement.models import Paiement
        from parametre.models import taux
        from django.db.models import Sum, Q
        from decimal import Decimal
        from datetime import datetime
        
        if request.method != 'POST':
            return JsonResponse({'success': False, 'error': 'Méthode non autorisée'})
        
        # Récupérer les paramètres
        data = json.loads(request.body)
        date_debut = data.get('date_debut')
        date_fin = data.get('date_fin')
        
        if not date_debut or not date_fin:
            return JsonResponse({'success': False, 'error': 'Dates de début et fin requises'})
        
        # Convertir les dates
        try:
            date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
            date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'success': False, 'error': 'Format de date invalide'})
        
        user_cabinet = getattr(request.user, 'cabinet', None)
        if not user_cabinet:
            # Si l'utilisateur n'a pas de cabinet, prendre le premier disponible
            from Structure.models import Cabinet
            user_cabinet = Cabinet.objects.first()
            
        if not user_cabinet:
            return JsonResponse({'success': False, 'error': 'Cabinet non trouvé'})
        
        # Récupérer le taux de change
        taux_obj = taux.objects.filter(cabinet=user_cabinet).order_by('-date_ajouter').first()
        taux_change = Decimal(taux_obj.cout) if taux_obj else Decimal('2500.0')
        
        # Filtrer les mouvements par plage de dates
        mouvements = Paiement.objects.filter(
            cabinet=user_cabinet,
            date_paiement__date__gte=date_debut,
            date_paiement__date__lte=date_fin
        ).order_by('-date_paiement')
        
        # Calculer les totaux pour la période
        entrees_periode = mouvements.filter(type_operation="ENTREE").aggregate(
            total=Sum("montant_payer_dollars")
        )["total"] or 0
        
        sorties_periode = mouvements.filter(type_operation="SORTIE").aggregate(
            total=Sum("montant_payer_dollars")
        )["total"] or 0
        
        solde_periode = entrees_periode - sorties_periode
        
        # Préparer les données pour le template
        mouvements_data = []
        for mouvement in mouvements:
            mouvements_data.append({
                'id': mouvement.id,
                'date': mouvement.date_paiement.strftime('%d/%m/%Y %H:%M'),
                'type_operation': mouvement.get_type_operation_display(),
                'motif': mouvement.motif,
                'montant_usd': float(mouvement.montant_payer_dollars),
                'montant_fc': float(mouvement.montant_payer_dollars * taux_change),
                'personne': mouvement.personne_qui_paie or (mouvement.client.nom if mouvement.client else 'N/A'),
                'dossier': mouvement.dossier.numero_reference_dossier if mouvement.dossier else 'N/A',
                'agent': mouvement.agent.nom if mouvement.agent else 'N/A',
            })
        
        # Calculer le solde avant la période
        solde_avant = Paiement.objects.filter(
            cabinet=user_cabinet,
            date_paiement__date__lt=date_debut
        ).aggregate(
            entrees=Sum("montant_payer_dollars", filter=Q(type_operation="ENTREE")),
            sorties=Sum("montant_payer_dollars", filter=Q(type_operation="SORTIE"))
        )
        
        entrees_avant = solde_avant['entrees'] or 0
        sorties_avant = solde_avant['sorties'] or 0
        solde_initial = entrees_avant - sorties_avant
        
        # Solde final
        solde_final = solde_initial + solde_periode
        
        rapport_data = {
            'success': True,
            'periode': {
                'date_debut': date_debut.strftime('%d/%m/%Y'),
                'date_fin': date_fin.strftime('%d/%m/%Y'),
            },
            'resume': {
                'solde_initial': float(solde_initial),
                'solde_initial_fc': float(solde_initial * taux_change),
                'entrees_periode': float(entrees_periode),
                'entrees_periode_fc': float(entrees_periode * taux_change),
                'sorties_periode': float(sorties_periode),
                'sorties_periode_fc': float(sorties_periode * taux_change),
                'solde_periode': float(solde_periode),
                'solde_periode_fc': float(solde_periode * taux_change),
                'solde_final': float(solde_final),
                'solde_final_fc': float(solde_final * taux_change),
            },
            'taux_change': float(taux_change),
            'mouvements': mouvements_data,
            'total_mouvements': len(mouvements_data),
            'cabinet': user_cabinet.nom,
            'date_generation': timezone.now().strftime('%d/%m/%Y %H:%M'),
        }
        
        # Enregistrer l'activité
        track_rapport_generation(
            request.user, 
            'rapport_caisse', 
            f"Période: {date_debut.strftime('%d/%m/%Y')} - {date_fin.strftime('%d/%m/%Y')}"
        )
        
        return JsonResponse(rapport_data)
        
    except Exception as e:
        logger.error(f"Erreur dans generer_rapport_caisse: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

@login_required(login_url='Connexion')
def imprimer_rapport_agents_filtre(request):
    """
    Génère et retourne directement le PDF du rapport agents avec filtres appliqués
    Suit la même logique que imprimer_facture_paiement (GET avec paramètres)
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Récupérer les paramètres GET (comme pour les autres rapports)
        agents_ids_json = request.GET.get('agents_ids', '[]')
        filtres_json = request.GET.get('filtres', '{}')
        type_rapport = request.GET.get('type_rapport', 'complet')
        
        logger.info(f"Début génération rapport agents - agents_ids: {agents_ids_json}, filtres: {filtres_json}")
        
        # Parser les données JSON
        try:
            agents_ids = json.loads(agents_ids_json)
            filtres = json.loads(filtres_json)
        except json.JSONDecodeError as e:
            logger.error(f"Erreur parsing JSON: {str(e)}")
            return HttpResponse("Données JSON invalides", status=400)
        
        if not agents_ids:
            logger.warning("Aucun agent sélectionné")
            return HttpResponse("Aucun agent sélectionné", status=400)
        
        logger.info(f"Agents sélectionnés: {len(agents_ids)} agents")
        
        # Récupérer les agents
        user_company = getattr(request.user, 'company', None)
        if user_company:
            agents_obj = agent.objects.filter(id__in=agents_ids, company=user_company)
        else:
            agents_obj = agent.objects.filter(id__in=agents_ids)
        
        logger.info(f"Agents trouvés en base: {agents_obj.count()} agents")
        
        # Préparer les données pour JSReport (même structure que facture_paiement)
        rapport_data = preparer_donnees_rapport_agents_filtre_simple(agents_obj, filtres, request)
        
        logger.info(f"Données préparées - {len(rapport_data.get('agents', []))} agents dans les données")
        logger.info(f"Template à utiliser: rapport_agent")
        
        # Test de connexion JSReport
        if not jsreport_service.test_connection():
            logger.error("Impossible de se connecter au service JSReport")
            return HttpResponse("Service JSReport indisponible", status=503)
        
        # Génération du PDF via le service centralisé JSReport (même logique que facture_paiement)
        filename = f"rapport_agents_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        logger.info(f"Appel JSReport avec template 'rapport_agent' et filename '{filename}'")
        
        return jsreport_service.generate_pdf_response(
            template_name="rapport_agent",
            data=rapport_data,
            filename=filename,
            disposition="inline"
        )
        
    except Exception as e:
        logger.error(f"Erreur génération rapport agents filtrés: {str(e)}", exc_info=True)
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_agents_filtre_simple(agents_obj, filtres, request):
    """
    Prépare les données pour JSReport (structure simplifiée comme facture_paiement)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Préparer les données des agents
    agents_data = []
    total_dossiers = 0
    dossiers_principaux = 0
    total_activites = 0
    agents_actifs = 0
    agents_inactifs = 0
    avocats = 0
    secretaires = 0
    autres_postes = 0
    
    for ag in agents_obj:
        # Compter les dossiers assignés à cet agent
        from Dossier.models import AvocatDossier
        dossiers_assignes = AvocatDossier.objects.filter(avocat=ag).count()
        dossiers_principaux_agent = AvocatDossier.objects.filter(avocat=ag, role='Principal').count()
        
        # Calculer les activités récentes
        activites_recentes = 0
        try:
            from Agent.models_activity import ActivityLog
            from datetime import timedelta
            from Authentification.models import CompteUtilisateur
            
            date_limite = datetime.now() - timedelta(days=30)
            user_agent = CompteUtilisateur.objects.get(agent=ag)
            activites_recentes = ActivityLog.objects.filter(
                user=user_agent,
                timestamp__gte=date_limite
            ).count()
        except:
            pass
        
        # Déterminer le statut
        statut_display = 'Inactif'
        try:
            from Authentification.models import CompteUtilisateur
            user_agent = CompteUtilisateur.objects.get(agent=ag)
            statut_display = 'Actif' if user_agent.is_active else 'Inactif'
        except CompteUtilisateur.DoesNotExist:
            statut_display = 'Pas de compte'
        
        # Générer les initiales pour la photo placeholder
        initiales = ""
        if ag.nom and ag.prenom:
            initiales = f"{ag.nom[0]}{ag.prenom[0]}".upper()
        elif ag.nom:
            initiales = ag.nom[0].upper()
        
        agent_info = {
            'id': ag.id,
            'nom': safe_str(ag.nom),
            'prenom': safe_str(ag.prenom),
            'email': safe_str(ag.email),
            'telephone': safe_str(ag.telephone),
            'poste': safe_str(ag.poste),
            'statut': statut_display,
            'dossiers_total': dossiers_assignes,
            'dossiers_principaux': dossiers_principaux_agent,
            'activites_recentes': activites_recentes,
            'photo': ag.photo.url if ag.photo else None,
            'initiales': initiales
        }
        
        # Calculs pour statistiques globales
        total_dossiers += dossiers_assignes
        dossiers_principaux += dossiers_principaux_agent
        total_activites += activites_recentes
        
        if statut_display == 'Actif':
            agents_actifs += 1
        else:
            agents_inactifs += 1
            
        if ag.poste == 'Avocat':
            avocats += 1
        elif ag.poste == 'Secrétaire':
            secretaires += 1
        else:
            autres_postes += 1
        
        agents_data.append(agent_info)
    
    # Calculer le taux d'activité
    taux_activite = 0
    if len(agents_data) > 0:
        taux_activite = round((agents_actifs / len(agents_data)) * 100, 1)
    
    # Préparer les filtres appliqués pour l'affichage
    filtres_appliques = "Aucun"
    if filtres.get('poste') or filtres.get('statut') or filtres.get('recherche'):
        filtres_list = []
        if filtres.get('poste'):
            filtres_list.append(f"Poste: {filtres['poste']}")
        if filtres.get('statut'):
            filtres_list.append(f"Statut: {filtres['statut']}")
        if filtres.get('recherche'):
            filtres_list.append(f"Recherche: \"{filtres['recherche']}\"")
        filtres_appliques = ", ".join(filtres_list)
    
    # Structure des données compatible avec JSReport (même style que facture_paiement)
    data = {
        "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "cabinet": {
            "nom": safe_str(request.user.cabinet.nom) if request.user.cabinet else "Cabinet",
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "site_web": safe_str(request.user.cabinet.site_web) if request.user.cabinet and hasattr(request.user.cabinet, 'site_web') else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "agents": agents_data,
        "filtres": filtres,
        "filtres_appliques": filtres_appliques,
        "statistiques": {
            "total_agents": len(agents_data),
            "agents_actifs": agents_actifs,
            "agents_inactifs": agents_inactifs,
            "avocats": avocats,
            "secretaires": secretaires,
            "autres_postes": autres_postes,
            "total_dossiers": total_dossiers,
            "dossiers_principaux": dossiers_principaux,
            "total_activites": total_activites,
            "taux_activite": taux_activite
        }
    }
    
    return data

@login_required(login_url='Connexion')
def test_jsreport_agent(request):
    """
    Vue de test pour vérifier JSReport et le template rapport_agent
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Test de connexion
        connection_ok = jsreport_service.test_connection()
        
        # Récupérer les templates
        templates = jsreport_service.get_templates()
        
        # Chercher le template rapport_agent
        rapport_agent_template = None
        if templates:
            for template in templates:
                if template.get('name') == 'rapport_agent':
                    rapport_agent_template = template
                    break
        
        # Données de test simples
        test_data = {
            "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "cabinet": {
                "nom": "Cabinet Test",
                "telephone": "123456789",
                "email": "test@cabinet.com",
                "site_web": "www.cabinet.com",
                "adresse": "Adresse test"
            },
            "agents": [
                {
                    "id": 1,
                    "nom": "Test",
                    "prenom": "Agent",
                    "email": "agent@test.com",
                    "telephone": "123456789",
                    "poste": "Avocat",
                    "statut": "Actif",
                    "dossiers_total": 5,
                    "dossiers_principaux": 3,
                    "activites_recentes": 10,
                    "initiales": "TA"
                }
            ],
            "filtres": {},
            "filtres_appliques": "Aucun",
            "statistiques": {
                "total_agents": 1,
                "agents_actifs": 1,
                "agents_inactifs": 0,
                "avocats": 1,
                "secretaires": 0,
                "autres_postes": 0,
                "total_dossiers": 5,
                "dossiers_principaux": 3,
                "total_activites": 10,
                "taux_activite": 100.0
            }
        }
        
        # Test de génération PDF
        pdf_test_result = None
        if connection_ok and rapport_agent_template:
            try:
                pdf_content = jsreport_service.generate_pdf("rapport_agent", test_data)
                pdf_test_result = "Succès" if pdf_content else "Échec"
            except Exception as e:
                pdf_test_result = f"Erreur: {str(e)}"
        
        # Préparer le rapport de diagnostic
        diagnostic = {
            "connexion_jsreport": "OK" if connection_ok else "ÉCHEC",
            "templates_disponibles": len(templates) if templates else 0,
            "template_rapport_agent": "Trouvé" if rapport_agent_template else "Non trouvé",
            "test_generation_pdf": pdf_test_result or "Non testé",
            "url_jsreport": jsreport_service.base_url,
        }
        
        if templates:
            diagnostic["liste_templates"] = [t.get('name', 'Sans nom') for t in templates]
        
        if rapport_agent_template:
            diagnostic["details_template"] = {
                "name": rapport_agent_template.get('name'),
                "shortid": rapport_agent_template.get('shortid'),
                "engine": rapport_agent_template.get('engine'),
                "recipe": rapport_agent_template.get('recipe')
            }
        
        # Retourner le diagnostic en JSON
        return HttpResponse(
            f"<pre>{json.dumps(diagnostic, indent=2, ensure_ascii=False)}</pre>",
            content_type='text/html'
        )
        
    except Exception as e:
        return HttpResponse(f"Erreur diagnostic: {str(e)}", status=500)
    """
    Génère un rapport démo HTML pour les agents filtrés
    """
    try:
        import os
        
        # Créer le dossier rapports s'il n'existe pas
        rapports_dir = os.path.join(settings.MEDIA_ROOT, 'rapports')
        os.makedirs(rapports_dir, exist_ok=True)
        
        # Générer le contenu HTML
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Rapport Agents Filtrés - {rapport_data['cabinet']['nom']}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ text-align: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }}
                .section {{ margin: 20px 0; }}
                .stats {{ display: flex; justify-content: space-around; background: #f8f9fa; padding: 20px; margin: 20px 0; }}
                .stat-item {{ text-align: center; }}
                .agent-item {{ background: white; border: 1px solid #dee2e6; border-radius: 8px; padding: 15px; margin: 10px 0; }}
                .demo-notice {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 10px; margin: 10px 0; border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .badge {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; }}
                .badge-success {{ background: #d4edda; color: #155724; }}
                .badge-danger {{ background: #f8d7da; color: #721c24; }}
                .badge-info {{ background: #d1ecf1; color: #0c5460; }}
            </style>
        </head>
        <body>
            <div class="demo-notice">
                <strong>⚠️ Mode Démo</strong> - Ce rapport est généré en mode démo. 
                Configurez JSReport Docker pour la génération complète des rapports.
            </div>
            
            <div class="header">
                <h1>📋 Rapport Agents - {type_rapport.title()}</h1>
                <h2>{rapport_data['cabinet']['nom']}</h2>
                <p>Généré le {rapport_data['date_generation']}</p>
                <p><strong>Filtres appliqués:</strong> {rapport_data['filtres_appliques']}</p>
            </div>
            
            <div class="section">
                <h3>📊 Statistiques</h3>
                <div class="stats">
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['total_agents']}</h3>
                        <p>Total Agents</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['agents_actifs']}</h3>
                        <p>Agents Actifs</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['avocats']}</h3>
                        <p>Avocats</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['secretaires']}</h3>
                        <p>Secrétaires</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['total_dossiers']}</h3>
                        <p>Total Dossiers</p>
                    </div>
                    <div class="stat-item">
                        <h3>{rapport_data['statistiques']['taux_activite']}%</h3>
                        <p>Taux d'Activité</p>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h3>👥 Liste des Agents ({len(rapport_data['agents'])} agents)</h3>
                <table>
                    <tr>
                        <th>N°</th>
                        <th>Nom & Prénom</th>
                        <th>Poste</th>
                        <th>Contact</th>
                        <th>Statut</th>
                        <th>Dossiers</th>
                        <th>Activités</th>
                    </tr>
        """
        
        for i, agent_info in enumerate(rapport_data['agents'], 1):
            statut_class = "badge-success" if agent_info['statut'] == 'Actif' else "badge-danger"
            
            html_content += f"""
                    <tr>
                        <td>{i}</td>
                        <td>
                            <strong>{agent_info['nom']} {agent_info['prenom']}</strong><br>
                            <small>ID: {agent_info['id']}</small>
                        </td>
                        <td><span class="badge badge-info">{agent_info['poste']}</span></td>
                        <td>
                            {agent_info['email']}<br>
                            {agent_info['telephone']}
                        </td>
                        <td><span class="badge {statut_class}">{agent_info['statut']}</span></td>
                        <td>
                            <strong>{agent_info['dossiers_principaux']}</strong> Principal(aux)<br>
                            <strong>{agent_info['dossiers_total']}</strong> Total
                        </td>
                        <td>{agent_info['activites_recentes']}</td>
                    </tr>
            """
        
        html_content += """
                </table>
            </div>
            
            <div style="margin-top: 40px; text-align: center; color: #6c757d;">
                <p><em>Rapport généré par le système de gestion Cabinet Avocat</em></p>
            </div>
        </body>
        </html>
        """
        
        # Nom du fichier
        filename = f"demo_agents_filtre_{type_rapport}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
        filepath = os.path.join(rapports_dir, filename)
        
        # Sauvegarder le fichier
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Retourner l'URL relative
        return f"/media/rapports/{filename}"
        
    except Exception as e:
        logger.error(f"Erreur génération rapport démo agents filtrés: {str(e)}")
        return None

@login_required(login_url='Connexion')
def imprimer_rapport_clients_filtre(request):
    """
    Génère et retourne directement le PDF du rapport clients avec filtres appliqués
    Suit la même logique que imprimer_rapport_agents_filtre
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Récupérer les paramètres GET
        clients_ids_json = request.GET.get('clients_ids', '[]')
        filtres_json = request.GET.get('filtres', '{}')
        type_rapport = request.GET.get('type_rapport', 'complet')
        
        logger.info(f"Début génération rapport clients - clients_ids: {clients_ids_json}, filtres: {filtres_json}")
        
        # Parser les données JSON
        try:
            clients_ids = json.loads(clients_ids_json)
            filtres = json.loads(filtres_json)
        except json.JSONDecodeError as e:
            logger.error(f"Erreur parsing JSON: {str(e)}")
            return HttpResponse("Données JSON invalides", status=400)
        
        if not clients_ids:
            logger.warning("Aucun client sélectionné")
            return HttpResponse("Aucun client sélectionné", status=400)
        
        logger.info(f"Clients sélectionnés: {len(clients_ids)} clients")
        
        # Récupérer les clients
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet:
            clients_obj = client.objects.filter(id__in=clients_ids, cabinet=user_cabinet)
        else:
            clients_obj = client.objects.filter(id__in=clients_ids)
        
        logger.info(f"Clients trouvés en base: {clients_obj.count()} clients")
        
        # Préparer les données pour JSReport
        rapport_data = preparer_donnees_rapport_clients_filtre(clients_obj, filtres, request)
        
        logger.info(f"Données préparées - {len(rapport_data.get('clients', []))} clients dans les données")
        logger.info(f"Template à utiliser: rapport_client")
        
        # Test de connexion JSReport
        if not jsreport_service.test_connection():
            logger.error("Impossible de se connecter au service JSReport")
            return HttpResponse("Service JSReport indisponible", status=503)
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_clients_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        logger.info(f"Appel JSReport avec template 'rapport_client' et filename '{filename}'")
        
        return jsreport_service.generate_pdf_response(
            template_name="rapport_client",
            data=rapport_data,
            filename=filename,
            disposition="inline"
        )
        
    except Exception as e:
        logger.error(f"Erreur génération rapport clients filtrés: {str(e)}", exc_info=True)
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_clients_filtre(clients_obj, filtres, request):
    """
    Prépare les données pour JSReport (structure adaptée aux clients)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Préparer les données des clients
    clients_data = []
    total_dossiers = 0
    total_dossiers_ouverts = 0
    total_dossiers_gagnes = 0
    total_montant_usd = 0
    total_montant_fc = 0
    clients_actifs = 0
    clients_physiques = 0
    clients_morales = 0
    
    for cl in clients_obj:
        # Compter les dossiers du client
        from Dossier.models import dossier
        dossiers_client = dossier.objects.filter(client=cl)
        total_dossiers_client = dossiers_client.count()
        dossiers_ouverts_client = dossiers_client.filter(statut_dossier='Ouvert').count()
        dossiers_gagnes_client = dossiers_client.filter(score='gagne').count()
        
        # Calculer les montants
        montant_usd_client = sum(safe_float(d.montant_dollars_enreg) for d in dossiers_client)
        montant_fc_client = sum(safe_float(d.montant_fc_enreg) for d in dossiers_client)
        
        # Dernière activité
        derniere_activite = ""
        if dossiers_client.exists():
            dernier_dossier = dossiers_client.order_by('-date_ouverture').first()
            if dernier_dossier and dernier_dossier.date_ouverture:
                derniere_activite = dernier_dossier.date_ouverture.strftime('%d/%m/%Y')
        
        # Générer les initiales pour la photo placeholder
        initiales = ""
        if cl.nom and cl.prenom:
            initiales = f"{cl.nom[0]}{cl.prenom[0]}".upper()
        elif cl.nom:
            initiales = cl.nom[0].upper()
        
        client_info = {
            'id': cl.id,
            'nom': safe_str(cl.nom),
            'prenom': safe_str(cl.prenom),
            'email': safe_str(cl.email),
            'telephone': safe_str(cl.telephone),
            'type_client': safe_str(cl.type_client) if hasattr(cl, 'type_client') else 'Physique',
            'total_dossiers': total_dossiers_client,
            'dossiers_ouverts': dossiers_ouverts_client,
            'dossiers_gagnes': dossiers_gagnes_client,
            'montant_total_usd': montant_usd_client,
            'montant_total_fc': montant_fc_client,
            'derniere_activite': derniere_activite,
            'photo': cl.photo.url if cl.photo else None,
            'initiales': initiales
        }
        
        # Calculs pour statistiques globales
        total_dossiers += total_dossiers_client
        total_dossiers_ouverts += dossiers_ouverts_client
        total_dossiers_gagnes += dossiers_gagnes_client
        total_montant_usd += montant_usd_client
        total_montant_fc += montant_fc_client
        
        # Compter les types de clients
        clients_actifs += 1  # Tous les clients sélectionnés sont considérés comme actifs
        
        type_client = getattr(cl, 'type_client', 'Physique')
        if type_client == 'Physique':
            clients_physiques += 1
        else:
            clients_morales += 1
        
        clients_data.append(client_info)
    
    # Calculer le taux de réussite
    taux_reussite = 0
    if total_dossiers > 0:
        taux_reussite = round((total_dossiers_gagnes / total_dossiers) * 100, 1)
    
    # Préparer les filtres appliqués pour l'affichage
    filtres_appliques = "Aucun"
    if filtres.get('type') or filtres.get('statut') or filtres.get('recherche'):
        filtres_list = []
        if filtres.get('type'):
            filtres_list.append(f"Type: {filtres['type']}")
        if filtres.get('statut'):
            filtres_list.append(f"Statut: {filtres['statut']}")
        if filtres.get('recherche'):
            filtres_list.append(f"Recherche: \"{filtres['recherche']}\"")
        filtres_appliques = ", ".join(filtres_list)
    
    # Structure des données compatible avec JSReport
    data = {
        "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "cabinet": {
            "nom": safe_str(request.user.cabinet.nom) if request.user.cabinet else "Cabinet",
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "site_web": safe_str(request.user.cabinet.site_web) if request.user.cabinet and hasattr(request.user.cabinet, 'site_web') else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "clients": clients_data,
        "filtres": filtres,
        "filtres_appliques": filtres_appliques,
        "statistiques": {
            "total_clients": len(clients_data),
            "clients_actifs": clients_actifs,
            "clients_physiques": clients_physiques,
            "clients_morales": clients_morales,
            "total_dossiers": total_dossiers,
            "total_dossiers_ouverts": total_dossiers_ouverts,
            "total_dossiers_gagnes": total_dossiers_gagnes,
            "montant_total_usd": round(total_montant_usd, 2),
            "montant_total_fc": round(total_montant_fc, 0),
            "taux_reussite": taux_reussite
        }
    }
    
    return data
@login_required(login_url='Connexion')
def imprimer_rapport_juridictions_filtre(request):
    """
    Génère et retourne directement le PDF du rapport juridictions avec filtres appliqués
    Suit la même logique que imprimer_rapport_clients_filtre
    """
    try:
        from utils.jsreport_service import jsreport_service
        
        # Récupérer les paramètres GET
        juridictions_ids_json = request.GET.get('juridictions_ids', '[]')
        filtres_json = request.GET.get('filtres', '{}')
        type_rapport = request.GET.get('type_rapport', 'complet')
        
        logger.info(f"Début génération rapport juridictions - juridictions_ids: {juridictions_ids_json}, filtres: {filtres_json}")
        
        # Parser les données JSON
        try:
            juridictions_ids = json.loads(juridictions_ids_json)
            filtres = json.loads(filtres_json)
        except json.JSONDecodeError as e:
            logger.error(f"Erreur parsing JSON: {str(e)}")
            return HttpResponse("Données JSON invalides", status=400)
        
        if not juridictions_ids:
            logger.warning("Aucune juridiction sélectionnée")
            return HttpResponse("Aucune juridiction sélectionnée", status=400)
        
        logger.info(f"Juridictions sélectionnées: {len(juridictions_ids)} juridictions")
        
        # Récupérer les juridictions
        from Structure.models import Juridiction
        user_cabinet = getattr(request.user, 'cabinet', None)
        if user_cabinet:
            juridictions_obj = Juridiction.objects.filter(id__in=juridictions_ids, cabinet=user_cabinet)
        else:
            juridictions_obj = Juridiction.objects.filter(id__in=juridictions_ids)
        
        logger.info(f"Juridictions trouvées en base: {juridictions_obj.count()} juridictions")
        
        # Préparer les données pour JSReport
        rapport_data = preparer_donnees_rapport_juridictions_filtre(juridictions_obj, filtres, request)
        
        logger.info(f"Données préparées - {len(rapport_data.get('juridictions', []))} juridictions dans les données")
        logger.info(f"Template à utiliser: rapport_juridiction")
        
        # Test de connexion JSReport
        if not jsreport_service.test_connection():
            logger.error("Impossible de se connecter au service JSReport")
            return HttpResponse("Service JSReport indisponible", status=503)
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_juridictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        logger.info(f"Appel JSReport avec template 'rapport_juridiction' et filename '{filename}'")
        
        return jsreport_service.generate_pdf_response(
            template_name="rapport_juridiction",
            data=rapport_data,
            filename=filename,
            disposition="inline"
        )
        
    except Exception as e:
        logger.error(f"Erreur génération rapport juridictions filtrées: {str(e)}", exc_info=True)
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_juridictions_filtre(juridictions_obj, filtres, request):
    """
    Prépare les données pour JSReport (structure adaptée aux juridictions)
    """
    # Fonctions utilitaires
    def safe_str(value):
        return "" if value is None else str(value)
    
    # Date du jour
    today = datetime.now().strftime("%d/%m/%Y")
    
    # Préparer les données des juridictions
    juridictions_data = []
    juridictions_actives = 0
    lieux_set = set()
    avec_date_creation = 0
    avec_description = 0
    repartition_lieux = {}
    
    for jur in juridictions_obj:
        # Informations de base
        lieu_nom = jur.lieu.nom if jur.lieu else "Non défini"
        date_creation = ""
        if hasattr(jur, 'date_creation') and jur.date_creation:
            date_creation = jur.date_creation.strftime('%d/%m/%Y')
            avec_date_creation += 1
        
        description = safe_str(getattr(jur, 'description', ''))
        if description:
            avec_description += 1
        
        juridiction_info = {
            'id': jur.id,
            'nom': safe_str(jur.nom),
            'lieu_nom': lieu_nom,
            'date_creation': date_creation,
            'description': description,
            'statut': 'Actif'  # Toutes les juridictions sélectionnées sont considérées comme actives
        }
        
        # Calculs pour statistiques globales
        juridictions_actives += 1
        lieux_set.add(lieu_nom)
        
        # Répartition par lieu
        if lieu_nom in repartition_lieux:
            repartition_lieux[lieu_nom] += 1
        else:
            repartition_lieux[lieu_nom] = 1
        
        juridictions_data.append(juridiction_info)
    
    # Calculer le taux d'activité (100% car toutes les juridictions sélectionnées sont actives)
    taux_activite = 100.0
    
    # Préparer la répartition par lieu pour le template
    repartition_lieux_list = []
    for lieu, count in repartition_lieux.items():
        repartition_lieux_list.append({
            'lieu': lieu,
            'count': count
        })
    
    # Préparer les filtres appliqués pour l'affichage
    filtres_appliques = "Aucun"
    if filtres.get('lieu') or filtres.get('recherche'):
        filtres_list = []
        if filtres.get('lieu'):
            filtres_list.append(f"Lieu: {filtres['lieu']}")
        if filtres.get('recherche'):
            filtres_list.append(f"Recherche: \"{filtres['recherche']}\"")
        filtres_appliques = ", ".join(filtres_list)
    
    # Structure des données compatible avec JSReport
    data = {
        "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "cabinet": {
            "nom": safe_str(request.user.cabinet.nom) if request.user.cabinet else "Cabinet",
            "telephone": safe_str(request.user.cabinet.telephone) if request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user.cabinet else '',
            "site_web": safe_str(request.user.cabinet.site_web) if request.user.cabinet and hasattr(request.user.cabinet, 'site_web') else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user.cabinet and request.user.cabinet.logo else None
        },
        "juridictions": juridictions_data,
        "filtres": filtres,
        "filtres_appliques": filtres_appliques,
        "statistiques": {
            "total_juridictions": len(juridictions_data),
            "juridictions_actives": juridictions_actives,
            "lieux_differents": len(lieux_set),
            "avec_date_creation": avec_date_creation,
            "avec_description": avec_description,
            "taux_activite": taux_activite,
            "repartition_lieux": repartition_lieux_list
        }
    }
    
    return data

@login_required(login_url='Connexion')
def imprimer_rapport_communes_filtre(request):
    """
    Génère et retourne directement le PDF du rapport communes avec filtres appliqués
    (utilise template_name au lieu de shortid pour plus de fiabilité)
    """
    try:
        # Récupérer les IDs des communes depuis les paramètres POST
        communes_ids = request.POST.getlist('communes_ids[]')
        
        if not communes_ids:
            return HttpResponse("Aucune commune sélectionnée", status=400)
        
        logger.info(f"Impression rapport communes filtrées - IDs: {communes_ids}")
        
        # Récupérer les communes
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            communes_obj = commune.objects.filter(id__in=communes_ids, cabinet=user_cabinet)
        else:
            communes_obj = commune.objects.filter(id__in=communes_ids)
        
        if not communes_obj.exists():
            return HttpResponse("Aucune commune trouvée", status=404)
        
        # Récupérer les filtres appliqués
        filtres = {
            'statut': request.POST.get('filtre_statut', ''),
            'periode': request.POST.get('filtre_periode', ''),
            'recherche': request.POST.get('recherche', ''),
        }
        
        # Préparer les données pour JSReport
        rapport_data = preparer_donnees_rapport_communes_filtre(communes_obj, filtres, request)
        
        logger.info(f"Données préparées - {len(rapport_data.get('communes', []))} communes dans les données")
        
        from utils.jsreport_service import jsreport_service
        
        # Génération du PDF via le service centralisé JSReport avec template_name
        filename = f"rapport_communes_filtre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Essayer d'abord avec le template commune spécifique
        try:
            return jsreport_service.generate_pdf_response(
                template_name="rapport_commune",  # Template spécifique aux communes
                data=rapport_data,
                filename=filename,
                disposition="inline"  # Affichage dans le navigateur au lieu de téléchargement
            )
        except Exception as template_error:
            logger.warning(f"Template 'rapport_commune' non trouvé, utilisation du template client: {template_error}")
            # Fallback: utiliser le template client existant
            return jsreport_service.generate_pdf_response(
                template_name="Facture_paiement_client",  # Template de fallback qui fonctionne
                data=rapport_data,
                filename=filename,
                disposition="inline"
            )
        
    except requests.RequestException as e:
        logger.error(f"Erreur JSReport: {str(e)}")
        return HttpResponse(f"Erreur lors de la génération du PDF : {e}", status=500)
    except Exception as e:
        logger.error(f"Erreur impression rapport communes filtrées: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_communes_filtre(communes_obj, filtres, request):
    """
    Prépare les données pour JSReport (structure adaptée aux communes)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Préparer les données des communes
    communes_data = []
    communes_actives = 0
    avec_date_ouverture = 0
    
    for com in communes_obj:
        # Déterminer le statut (pour l'instant toutes sont actives)
        statut = "Actif"
        if statut == "Actif":
            communes_actives += 1
        
        # Vérifier si la commune a une date d'ouverture
        if com.date_ouverture:
            avec_date_ouverture += 1
        
        commune_info = {
            'id': com.id,
            'nom': safe_str(com.nom),
            'date_ouverture': com.date_ouverture.strftime('%d/%m/%Y') if com.date_ouverture else 'Non définie',
            'statut': statut,
            'cabinet_nom': safe_str(com.cabinet.nom) if com.cabinet else 'Non défini',
            'derniere_activite': 'Récente'  # À adapter selon vos besoins
        }
        
        communes_data.append(commune_info)
    
    # Calculer les statistiques
    total_communes = len(communes_data)
    taux_activite = (communes_actives / total_communes * 100) if total_communes > 0 else 0
    
    # Préparer les filtres appliqués pour l'affichage
    filtres_appliques = "Aucun"
    if filtres.get('statut') or filtres.get('periode') or filtres.get('recherche'):
        filtres_list = []
        if filtres.get('statut'):
            filtres_list.append(f"Statut: {filtres['statut']}")
        if filtres.get('periode'):
            filtres_list.append(f"Période: {filtres['periode']} jours")
        if filtres.get('recherche'):
            filtres_list.append(f"Recherche: \"{filtres['recherche']}\"")
        filtres_appliques = ", ".join(filtres_list)
    
    # Structure des données compatible avec JSReport
    data = {
        "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "cabinet": {
            "nom": safe_str(request.user.cabinet.nom) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else "Cabinet",
            "telephone": safe_str(request.user.cabinet.telephone) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else '',
            "site_web": safe_str(request.user.cabinet.site_web) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and hasattr(request.user.cabinet, 'site_web') else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and request.user.cabinet.logo else None
        },
        "communes": communes_data,
        "filtres": filtres,
        "filtres_appliques": filtres_appliques,
        "statistiques": {
            "total_communes": total_communes,
            "communes_actives": communes_actives,
            "avec_date_ouverture": avec_date_ouverture,
            "taux_activite": taux_activite
        }
    }
    
    return data

# Fin du fichier views.py - Correction du problème de formatage

@login_required(login_url='Connexion')
def imprimer_rapport_dossiers_filtre(request):
    """
    Génère et retourne directement le PDF du rapport dossiers avec filtres appliqués
    (même logique que les autres rapports)
    """
    try:
        # Récupérer les IDs des dossiers depuis les paramètres POST
        dossiers_ids = request.POST.getlist('dossiers_ids[]')
        
        if not dossiers_ids:
            return HttpResponse("Aucun dossier sélectionné", status=400)
        
        logger.info(f"Impression rapport dossiers filtrés - IDs: {dossiers_ids}")
        
        # Récupérer les dossiers
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            dossiers_obj = dossier.objects.filter(id__in=dossiers_ids, cabinet=user_cabinet)
        else:
            dossiers_obj = dossier.objects.filter(id__in=dossiers_ids)
        
        if not dossiers_obj.exists():
            return HttpResponse("Aucun dossier trouvé", status=404)
        
        # Récupérer les filtres appliqués
        filtres = {
            'statut': request.POST.get('filtre_statut', ''),
            'activite': request.POST.get('filtre_activite', ''),
            'recherche': request.POST.get('recherche', ''),
        }
        
        # Préparer les données pour JSReport
        rapport_data = preparer_donnees_rapport_dossiers_filtre(dossiers_obj, filtres, request)
        
        logger.info(f"Données préparées - {len(rapport_data.get('dossiers', []))} dossiers dans les données")
        
        from utils.jsreport_service import jsreport_service
        
        # Génération du PDF via le service centralisé JSReport avec template_name
        filename = f"rapport_dossiers_filtre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Utiliser le template dossier spécifique
        return jsreport_service.generate_pdf_response(
            template_name="rapport_dossier",  # Template spécifique aux dossiers
            data=rapport_data,
            filename=filename,
            disposition="inline"  # Affichage dans le navigateur au lieu de téléchargement
        )
        
    except requests.RequestException as e:
        logger.error(f"Erreur JSReport: {str(e)}")
        return HttpResponse(f"Erreur lors de la génération du PDF : {e}", status=500)
    except Exception as e:
        logger.error(f"Erreur impression rapport dossiers filtrés: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_dossiers_filtre(dossiers_obj, filtres, request):
    """
    Prépare les données pour JSReport (structure adaptée aux dossiers)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Préparer les données des dossiers
    dossiers_data = []
    dossiers_ouverts = 0
    dossiers_clotures = 0
    montant_total_fc = 0
    montant_total_usd = 0
    
    for dos in dossiers_obj:
        # Récupérer l'avocat principal
        from Dossier.models import AvocatDossier
        avocat_principal = AvocatDossier.objects.filter(dossier=dos, role='Principal').first()
        avocat_nom = f"{avocat_principal.avocat.nom} {avocat_principal.avocat.prenom}" if avocat_principal else "Non assigné"
        
        # Calculer les statistiques
        if dos.statut_dossier == 'Ouvert':
            dossiers_ouverts += 1
        elif dos.statut_dossier == 'Clôturé':
            dossiers_clotures += 1
        
        montant_total_fc += safe_float(dos.montant_fc_enreg)
        montant_total_usd += safe_float(dos.montant_dollars_enreg)
        
        dossier_info = {
            'id': dos.id,
            'numero_reference': safe_str(dos.numero_reference_dossier),
            'titre': safe_str(dos.titre),
            'client_nom': f"{dos.client.nom} {dos.client.prenom}" if dos.client else "Client non défini",
            'type_affaire': safe_str(dos.type_affaire.nom_type) if dos.type_affaire else 'Non défini',
            'avocat_principal': avocat_nom,
            'statut': safe_str(dos.statut_dossier),
            'date_ouverture': dos.date_ouverture.strftime('%d/%m/%Y') if dos.date_ouverture else 'Non définie',
            'date_cloture': dos.date_cloture.strftime('%d/%m/%Y') if dos.date_cloture else 'En cours',
            'montant_fc': safe_float(dos.montant_fc_enreg),
            'montant_usd': safe_float(dos.montant_dollars_enreg),
            'score': safe_str(dos.score) if dos.score else 'En cours'
        }
        
        dossiers_data.append(dossier_info)
    
    # Calculer les statistiques
    total_dossiers = len(dossiers_data)
    taux_reussite = (dossiers_clotures / total_dossiers * 100) if total_dossiers > 0 else 0
    
    # Préparer les filtres appliqués pour l'affichage
    filtres_appliques = "Aucun"
    if filtres.get('statut') or filtres.get('activite') or filtres.get('recherche'):
        filtres_list = []
        if filtres.get('statut'):
            filtres_list.append(f"Statut: {filtres['statut']}")
        if filtres.get('activite'):
            filtres_list.append(f"Activité: {filtres['activite']} jours")
        if filtres.get('recherche'):
            filtres_list.append(f"Recherche: \"{filtres['recherche']}\"")
        filtres_appliques = ", ".join(filtres_list)
    
    # Structure des données compatible avec JSReport
    data = {
        "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "cabinet": {
            "nom": safe_str(request.user.cabinet.nom) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else "Cabinet",
            "telephone": safe_str(request.user.cabinet.telephone) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else '',
            "site_web": safe_str(request.user.cabinet.site_web) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and hasattr(request.user.cabinet, 'site_web') else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and request.user.cabinet.logo else None
        },
        "dossiers": dossiers_data,
        "filtres": filtres,
        "filtres_appliques": filtres_appliques,
        "statistiques": {
            "total_dossiers": total_dossiers,
            "dossiers_ouverts": dossiers_ouverts,
            "dossiers_clotures": dossiers_clotures,
            "montant_total_fc": montant_total_fc,
            "montant_total_usd": montant_total_usd,
            "taux_reussite": taux_reussite
        }
    }
    
    return data

@login_required(login_url='Connexion')
def imprimer_rapport_activites_internes_filtre(request):
    """
    Génère et retourne directement le PDF du rapport activités internes avec filtres appliqués
    (même logique que les autres rapports)
    """
    try:
        # Récupérer les IDs des activités depuis les paramètres POST
        activites_ids = request.POST.getlist('activites_ids[]')
        
        if not activites_ids:
            return HttpResponse("Aucune activité sélectionnée", status=400)
        
        logger.info(f"Impression rapport activités internes filtrées - IDs: {activites_ids}")
        
        # Récupérer les activités
        from Structure.models import Activite
        user_cabinet = getattr(request.user, 'cabinet', None)
        
        if user_cabinet:
            activites_obj = Activite.objects.filter(id__in=activites_ids, cabinet=user_cabinet)
        else:
            activites_obj = Activite.objects.filter(id__in=activites_ids)
        
        if not activites_obj.exists():
            return HttpResponse("Aucune activité trouvée", status=404)
        
        # Récupérer les filtres appliqués
        filtres = {
            'recherche': request.POST.get('recherche', ''),
            'tri': request.POST.get('tri', ''),
            'ordre': request.POST.get('ordre', ''),
        }
        
        # Préparer les données pour JSReport
        rapport_data = preparer_donnees_rapport_activites_internes_filtre(activites_obj, filtres, request)
        
        logger.info(f"Données préparées - {len(rapport_data.get('activites', []))} activités dans les données")
        
        from utils.jsreport_service import jsreport_service
        
        # Génération du PDF via le service centralisé JSReport
        filename = f"rapport_activites_internes_filtre_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Utiliser le template activités internes
        return jsreport_service.generate_pdf_response(
            template_name="rapport_activite",  # Template spécifique aux activités
            data=rapport_data,
            filename=filename,
            disposition="inline"  # Affichage dans le navigateur au lieu de téléchargement
        )
        
    except requests.RequestException as e:
        logger.error(f"Erreur JSReport: {str(e)}")
        return HttpResponse(f"Erreur lors de la génération du PDF : {e}", status=500)
    except Exception as e:
        logger.error(f"Erreur impression rapport activités internes filtrées: {str(e)}")
        return HttpResponse(f"Erreur: {str(e)}", status=500)

def preparer_donnees_rapport_activites_internes_filtre(activites_obj, filtres, request):
    """
    Prépare les données pour JSReport (structure adaptée aux activités internes)
    """
    # Fonctions utilitaires
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def safe_str(value):
        return "" if value is None else str(value)
    
    # Préparer les données des activités
    activites_data = []
    total_utilisations = 0
    total_heures = 0
    total_revenus = 0
    
    from Dossier.models import ActiviteHeure
    
    for activite in activites_obj:
        # Récupérer les utilisations de cette activité
        utilisations = ActiviteHeure.objects.filter(
            description__icontains=activite.nom_activite
        ).select_related('dossier', 'avocat')
        
        # Calculer les statistiques pour cette activité
        utilisations_count = utilisations.count()
        heures_totales = sum(float(u.duree_heures) for u in utilisations)
        revenus_potentiels = 0
        
        # Calculer les revenus potentiels
        for utilisation in utilisations:
            try:
                cout = utilisation.calculer_cout_activite()
                revenus_potentiels += float(cout) if cout else 0
            except:
                pass
        
        # Dernière utilisation
        derniere_utilisation = utilisations.order_by('-date_activite').first()
        derniere_utilisation_data = None
        if derniere_utilisation:
            derniere_utilisation_data = {
                'date': derniere_utilisation.date_activite.strftime('%d/%m/%Y'),
                'dossier': derniere_utilisation.dossier.titre[:30] + '...' if len(derniere_utilisation.dossier.titre) > 30 else derniere_utilisation.dossier.titre
            }
        
        activite_info = {
            'id': activite.id,
            'nom_activite': safe_str(activite.nom_activite),
            'date_creation': activite.date_activite.strftime('%d/%m/%Y') if activite.date_activite else 'Non définie',
            'utilisations': utilisations_count,
            'heures_totales': round(heures_totales, 1),
            'revenus_potentiels': round(revenus_potentiels, 2),
            'derniere_utilisation': derniere_utilisation_data
        }
        
        activites_data.append(activite_info)
        
        # Totaux
        total_utilisations += utilisations_count
        total_heures += heures_totales
        total_revenus += revenus_potentiels
    
    # Calculer les statistiques globales
    total_activites = len(activites_data)
    taux_utilisation = (sum(1 for a in activites_data if a['utilisations'] > 0) / total_activites * 100) if total_activites > 0 else 0
    
    # Préparer les filtres appliqués pour l'affichage
    filtres_appliques = "Aucun"
    if filtres.get('recherche') or filtres.get('tri'):
        filtres_list = []
        if filtres.get('recherche'):
            filtres_list.append(f"Recherche: \"{filtres['recherche']}\"")
        if filtres.get('tri'):
            filtres_list.append(f"Tri: {filtres['tri']}")
        if filtres.get('ordre'):
            filtres_list.append(f"Ordre: {filtres['ordre']}")
        filtres_appliques = ", ".join(filtres_list)
    
    # Activités les plus populaires (top 5)
    activites_populaires = sorted(activites_data, key=lambda x: x['utilisations'], reverse=True)[:5]
    
    # Structure des données compatible avec JSReport
    data = {
        "date_generation": datetime.now().strftime('%d/%m/%Y à %H:%M'),
        "cabinet": {
            "nom": safe_str(request.user.cabinet.nom) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else "Cabinet",
            "telephone": safe_str(request.user.cabinet.telephone) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else '',
            "email": safe_str(request.user.cabinet.email) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet else '',
            "site_web": safe_str(request.user.cabinet.site_web) if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and hasattr(request.user.cabinet, 'site_web') else '',
            "adresse": f"{request.user.cabinet.adresse.numero}, {request.user.cabinet.adresse.avenue}, {request.user.cabinet.adresse.quartier}, {request.user.cabinet.adresse.commune}, {request.user.cabinet.adresse.ville}" if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and request.user.cabinet.adresse else '',
            "logo": request.user.cabinet.logo.url if request.user and hasattr(request.user, 'cabinet') and request.user.cabinet and request.user.cabinet.logo else None
        },
        "activites": activites_data,
        "filtres": filtres,
        "filtres_appliques": filtres_appliques,
        "statistiques": {
            "total_activites": total_activites,
            "total_utilisations": total_utilisations,
            "total_heures": round(total_heures, 1),
            "total_revenus": round(total_revenus, 2),
            "taux_utilisation": round(taux_utilisation, 1)
        },
        "activites_populaires": activites_populaires
    }
    
    return data