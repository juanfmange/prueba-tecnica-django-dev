from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt
import datetime


# Create your views here
# Resgistro de usuario
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        
        return Response(serializer.data)


### Login usuario con jwt
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()

        if user is None:
            raise AuthenticationFailed('User not found')

        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60), 
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret',algorithm='HS256').decode('utf-8')

        response = Response()

        #generar cookie para login
        response.set_cookie(key='jwt', value=token, httponly=True)

        response.data = {
            "jwt": token
        }

        return response

# usuario logeado
class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unaunthentificated')

        user = User.objects.filter(id=payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)


# logout de usuario
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }

        return response


# cookie de usuario logeado
class Cookie(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        return Response(token)
