from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from Dossier.models import client, dossier
from Agent.models import agent
import json
from datetime import date, datetime
import logging

logger = logging.getLogger(__name__)

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
        
        context = {
            'clients': clients,
            'total_clients': clients.count(),
            'today': date.today()
        }
        
        return render(request, 'admin_template/rapport_client.html', context)
        
    except Exception as e:
        logger.error(f"Erreur dans rapport_client_interface: {str(e)}")
        # Retourner une page d'erreur simple
        from django.http import HttpResponse
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
            'montant_usd': safe_float(d.montant_usd_enreg),
            'avocat_principal': avocat_nom
        }
        
        # Calculs pour statistiques
        total_fc += safe_float(d.montant_fc_enreg)
        total_usd += safe_float(d.montant_usd_enreg)
        
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
def telecharger_rapport_client(request, rapport_id):
    """
    Télécharge un rapport client généré (fonction conservée pour compatibilité)
    """
    # Cette fonction peut être utilisée pour télécharger des rapports sauvegardés
    pass