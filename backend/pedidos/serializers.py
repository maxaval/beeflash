from rest_framework import serializers
from .models import Ryder, Comercio, Cliente, Pedido

class RyderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ryder
        fields = '__all__'

class ComercioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comercio
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedido
        fields = '__all__'
        