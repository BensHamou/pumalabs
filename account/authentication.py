import requests
from django.contrib.auth.backends import BaseBackend
from .models import User
from requests.auth import HTTPBasicAuth
from django.contrib.auth.hashers import check_password
from django.contrib import messages 
from django.db.models import Q


class ApiBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            if username in ['admin', 'admin@admin.com']:
                user = User.objects.get(Q(username=username) | Q(email=username))
                if check_password(password, user.password):
                    return user
                else:
                    messages.error(request, "Mot de passe incorrect")
                    return None
            
            if '@' not in username:
                user = User.objects.get(username = username)
                email = user.email
            else:
                email = username
                
            auth = HTTPBasicAuth(email, password)

            response = requests.post('https://api.ldap.groupe-hasnaoui.com/pumalabs/auth', auth=auth)

            if not response.status_code == 200:
                messages.error(request, "Problème avec la connexion au serveur")
            else:
                if not response.json().get('authenticated'):
                    messages.error(request, "Mot de passe incorrect")
                else:
                    user = User.objects.get(username = response.json().get('userinfo')['ad2000'])
                    return user
        except User.DoesNotExist:
            messages.error(request, "Utilisateur pas trouvé")
        return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
