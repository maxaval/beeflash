from django.contrib import admin
from .models import Ryder, Comercio, Cliente, Pedido
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group

# Register your models here.
# Registra los modelos en el panel de administración
admin.site.register(Ryder)
admin.site.register(Comercio)
admin.site.register(Cliente)
admin.site.register(Pedido)

# Personalizar la visualización de User en el panel
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')

# Sobrescribir la configuración existente de User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Registrar los grupos para asignar roles
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name',)
    filter_horizontal = ('permissions',)

admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
