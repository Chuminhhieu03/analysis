from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
def index(request):
    return render(request, 'profile.html')

def changepassword(request):
    return render(request, 'changepassword.html')

def upgrade(request):
    return render(request, 'upgrade.html')
