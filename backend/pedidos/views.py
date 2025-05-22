from django.shortcuts import render
from rest_framework import viewsets, status, generics
from .models import Ryder, Comercio, Cliente, Pedido
from .serializers import RyderSerializer, ComercioSerializer, ClienteSerializer, PedidoSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny, IsAdminUser

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.serializers import ModelSerializer

from django.contrib.auth.decorators import login_required

from django.db.models import Avg, Count


# Create your views here.

@login_required
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")

class RyderViewSet(viewsets.ModelViewSet):
    queryset = Ryder.objects.all()
    serializer_class = RyderSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  # Solo usuarios autenticados pueden ver los Ryders

class ComercioViewSet(viewsets.ModelViewSet):
    queryset = Comercio.objects.all()
    serializer_class = ComercioSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]  # Solo usuarios autenticados pueden ver los Comercio

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden ver los Cliente

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]  # Solo usuarios autenticados pueden ver los Pedidos

class RegistroUsuarioView(APIView):
    permission_classes = [AllowAny]  # Permitir el acceso sin autenticación

    def post(self, request):
        data = request.data
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        rol = data.get("rol")  # Administrador, Ryder, Comercio

        # Validar que el usuario no exista
        if User.objects.filter(username=username).exists():
            return Response({"error": "El usuario ya existe"}, status=status.HTTP_400_BAD_REQUEST)

        # Crear usuario y asignarle rol
        usuario = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
        )
        
        if rol and Group.objects.filter(name=rol).exists():
            grupo = Group.objects.get(name=rol)
            usuario.groups.add(grupo)

        usuario.save()
        return Response({"mensaje": "Usuario creado exitosamente"}, status=status.HTTP_201_CREATED)
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["rol"] = self.user.groups.first().name if self.user.groups.exists() else "Sin rol"
        return data

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_active']

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Solo administradores pueden acceder

class UserUpdateView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Solo administradores pueden editar usuarios

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Solo administradores pueden eliminar usuarios

class EstadisticasPedidoView(APIView):
    def get(self, request):
        tiempo_promedio = Pedido.objects.filter(estado="entregado").aggregate(Avg('fecha_entrega'))
        return Response({"tiempo_promedio_minutos": tiempo_promedio["fecha_entrega__avg"]})
    
class ReporteComercioView(APIView):
    def get(self, request):
        data = Comercio.objects.annotate(
            total_pedidos=Count("pedido"),
            pedidos_entregados=Count("pedido", filter=models.Q(pedido__estado="entregado")),
        ).values("nombre", "total_pedidos", "pedidos_entregados")

        return Response(list(data))