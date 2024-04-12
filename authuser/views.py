from .services.UserService_Login import handleLoginServices
from .services.UserService_Logout import LogOut_Service
from .services.UserService_Signup import SignUp_Service
from .services.UserService_ResetPass import ResetPass_Service, ActivateAccount_Service, SetNewPassword_Service
from .services.UserService_Profile import HomeProfile_Service, EditProfile_Service
from .services.UserService_FeedBack import FeedBack_Service
from .services.UserService_ChangePass import  ChangePassword_Service
from .services.UserService_Upgrade import UpgradeHome_Service, UpgradeCheckOut_Service, UpgradeSucces_Service
# Create your views here.

def handleLogin(request):
    return handleLoginServices(request)

def logout(request):
    return LogOut_Service(request)

def signup(request):
    return SignUp_Service(request)

def resetPassword(request):
    return ResetPass_Service(request)

def ActivateAccountView(request, uidb64, token):
    return ActivateAccount_Service(request, uidb64, token)

def SetNewPasswordView(request, uidb64, token):
    return SetNewPassword_Service(request, uidb64, token)

def index(request):
    return HomeProfile_Service(request)

def edit_profile(request):
    return EditProfile_Service(request)

def feedback_user(request):
    return FeedBack_Service(request)

def changepassword(request):
    return ChangePassword_Service(request)

def upgrade(request):
    return UpgradeHome_Service(request)

def upgrade_checkout(request):
    return UpgradeCheckOut_Service(request)
        
def upgrade_success(request):
    return UpgradeSucces_Service(request)