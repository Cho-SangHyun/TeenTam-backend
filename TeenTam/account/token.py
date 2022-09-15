from rest_framework.response import Response
import jwt, datetime

def CreateToken(user):

    payload = {
      'id' : user.id,
      'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60), # Expire time 60m
      'iat' : datetime.datetime.now() # Issued at(created time)
    }

    token = jwt.encode(payload,"secretJWTkey",algorithm="HS256") # Creating Token by payload
    return token

def GetToken(request):
    token = request.GET.get("jwt")
    payload = jwt.decode(token, 'secretJWTkey', algorithms=['HS256'])
    return payload

def CheckToken(request):
    token = request.COOKIES.get('jwt')
    if not token:
        return False
    try:
        payload = jwt.decode(token, 'secretJWTkey', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return False
        
    return True   