from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='Connexion')
def dashboard_admin(request):
    return render(request, "dev_template/index.html")