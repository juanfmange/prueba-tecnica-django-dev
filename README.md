# Prueba tecnica desarrollador Django #

*Este repositorio es parte de la prueba técnica para desarrollador backend Django*

##### Herramientas implementadas

* Django Rest Framework
* Postgres
* Pandas
* Git
* Github
* Thunder Client

## Caso de uso

Desarrollar un API Rest con la ayuda de Django Rest Framework. Respuestas y envío de información mediante JSON.

### Implementación

Se desarrollo un modelo base para el proyecto, donde se gestionan los otros modelos (usuarios,bienes).

En setting.py, se agregaron las nuevas aplicaciones al modelo base:

```python
INSTALLED_APPS = [

'rest_framework',

'corsheaders',

'users',

'products'

]
```

Se agregó el middleware para corsheaders:

```python
MIDDLEWARE = [

'corsheaders.middleware.CorsMiddleware',

]
```

Para la conexión de la api a la base de datos de postgres utilizamos la libreria psycopg2:

```python
DATABASES = {

'default': {

'ENGINE': 'django.db.backends.postgresql_psycopg2',

'NAME': 'newdb',

'USER': 'juanmange',

'PASSWORD': '260697',

'HOST': '127.0.0.1',

'PORT': '5432',



}

}
```

Las urls para el modelo base son las siguientes:

```python
urlpatterns = [

path('admin/', admin.site.urls),

path('api/',include('users.urls')),

path('api/',include('products.urls')),

]
```

Se creó el modelo de usuario en users.models.py:

```python
class User(AbstractUser):


name = models.CharField(max_length=255)

username = models.CharField(max_length=255)

password = models.CharField(max_length=255)


USERNAME_FIELD = 'id'

REQUIRED_FIELDS = []


def __str__(self):

return self.name

```

Se implementó la clase AbstractUser de Django para la autentificación del usuario mediante la api.

Se creó el modelo de bienes en products.models.py heredando el modelo de usuario para poder trabajar con mi modelo de usuario:

```python
from django.db import models

from users.models import User

# Create your models here.



class Products(models.Model):

product = models.CharField(max_length=255)

description = models.CharField(max_length=255)

user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)

created = models.DateTimeField(auto_now_add=True)

modified = models.DateTimeField(auto_now=True)

```

Con el modelo usuario heredado para los bienes, podemos generar una ForeignKey para hacer una relación uno a muchos, es decir, el usuario puede tener varios bienes, pero los bienes solo pueden tener un usuario., En dado caso de que el usuario sea eliminado, tambien sus bienes se irán para asi poder tener una identidad referencial en la base de datos y evitando almacenar datos corruptos.

Posteriormente, se realizarón las migración de los modelos:

```bash
python3 manage.py makemigrations

python3 manage.py migrate

```

Una vez realizadas las migraciones podemos verificar en estas que los datos sean correctos, en caso contrario, podemos modificarlos.

Empezamos por el  las vistas de usuario:

```python
from rest_framework.response import Response

from rest_framework.views import APIView

from rest_framework.exceptions import AuthenticationFailed

from .serializers import UserSerializer

from .models import User

import jwt

import datetime



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
```

Algo importante que se implemento al proyecto fueron los serializers. Estos nos permiten transformar datos complejos en tipos de datos nativos de python, que posteriormente se pueden representar en JSON.

Los serializers para usuario:

```python
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

class Meta:

model = User

fields = ['id', 'name', 'username', 'password']

extra_kwargs = {

'password': {'write_only': True}

}



def create(self, validated_data):

password = validated_data.pop('password', None)

instance = self.Meta.model(**validated_data)

if password is not None:

instance.set_password(password)

instance.save()

return instance


```

para terminar de trabajar con usuarios, declaramos las urls:

```python
from django.urls import path

from .views import LoginView, RegisterView, UserView, LogoutView, Cookie

from rest_framework_simplejwt import views as jwt_views



urlpatterns = [

path('register', RegisterView.as_view()),

path('login', LoginView.as_view()),

path('user', UserView.as_view()),

path('logout', LogoutView.as_view()),

path('cookie', Cookie.as_view()),

path('token', jwt_views.TokenObtainPairView.as_view(),

name='token_obtain_pair'),

]
```

Corremos el servidor para trabajar con la api:

```bash
python3 manage.py runserver
```

Para el caso de registro de usuario:

![user_register](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_register.png)

Para el caso de login de usuario, podemos observar que obtenemos como respuesta el JWT

![user_login](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_login.png)

Tambien podemos saber que usuario esta logeado:

![user_user](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_user.png)

De igual forma podemos observar su cookie:

![user_cookie](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_cookie.png)

Logout de usuario:

![user_logout](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_logout.png)

para el caso del token de usuario:

![user_token](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_token.png)

Tambien podemos observar que al momento de querer hacer un login con un usuario a contraseña incorrecta tenemos respuesta para cada caso:

![user_b_user](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_b_user.png)

![user_b_password](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_b_password.png)

o si no tenemos un usuario logeado:

![user_b_login](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/user_b_login.png)

Para el modelo Bienes, declaramos el serializer:

```python
from rest_framework import serializers

from .models import Products




class ProductSerializer(serializers.ModelSerializer):

class Meta:

model = Products

fields = '__all__'



```

las vistas de los bienes:

```python
ffrom django.http import Http404

from rest_framework.response import Response

from rest_framework.views import APIView

from .models import Products

from .serializers import ProductSerializer

from rest_framework import status




class ViewProducts (APIView):

def get(self,request, format = None):

products = Products.objects.all()

serializer = ProductSerializer(products,many = True)

return Response(serializer.data)

def post(self,request,format = None):

serializer = ProductSerializer(data=request.data)

if serializer.is_valid():

serializer.save()

return Response(serializer.data)

return Response(serializer.errors)




## Modelo CRUD para los Bienes

class ProductDetail(APIView):

def get_object(self, pk):

try:

return Products.objects.get(pk=pk)

except Products.DoesNotExist:

raise Http404



def get(self, request, pk, format=None):

snippet = self.get_object(pk)

serializer = ProductSerializer(snippet)

return Response(serializer.data)



def put(self, request, pk, format=None):

snippet = self.get_object(pk)

serializer = ProductSerializer(snippet, data=request.data)

if serializer.is_valid():

serializer.save()

return Response(serializer.data)

return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def delete(self, request, pk, format=None):

snippet = self.get_object(pk)

snippet.delete()

return Response(status=status.HTTP_204_NO_CONTENT)
```

y sus urls:

```python
from django import views

from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns



from .views import ViewProducts, ProductDetail



urlpatterns = [

path('products', ViewProducts.as_view()),

path('products/<int:pk>/', ProductDetail.as_view()),

]



urlpatterns = format_suffix_patterns(urlpatterns)
```

En el caso de los bienes, trabajamos directamente con el id del cada bien para poder usar el modelo CRUD

Para ver los bienes registrados:

![products_products](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/products_products.png)

Podemos agregar un bien nuevo desde la api:

![products_add](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/products_add.png)

si queremos agregar un bien que tenga un usuario que no exista:

![products_b_add](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/products_b_add.png)

Modificar un bien agregando a la url el id del bien a modificar:

![products_put](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/products_put.png)

Obtener un bien por su id en la url:

![product_by_id](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/product_by_id.png)

Eliminar un bien de igual forma agregando a la url el id del bien a eliminar:

![product_delete](/home/juanmange/Documentos/python/PruebaTecnicaDjango/base/img/product_delete.png)
