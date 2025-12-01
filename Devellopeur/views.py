from django.shortcuts import render

# Create your views here.
def dashboard_admin(request):
    return render(request, "dev_template/index.html")