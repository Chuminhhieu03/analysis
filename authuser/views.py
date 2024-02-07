from django.shortcuts import render,get_object_or_404,redirect

# Create your views here.
def index(request):
    return render(request, 'profile.html')

def edit_profile(request):
    return render(request, "editprofile.html")

def feedback_user(request):
    return render(request, "feedback.html")
