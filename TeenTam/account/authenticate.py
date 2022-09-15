from rest_framework_simplejwt.tokens import RefreshToken

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    return str(refresh), str(refresh.access_token) 
    
    # {
    #     'refresh': str(refresh),
    #     'access': str(refresh.access_token),
    # }

def jwt_login(response, user):
    refresh, access = get_tokens_for_user(user)
    response.data = access
    response.set_cookie(key="refreshtoken", value=refresh, httponly=True)
    
    return response