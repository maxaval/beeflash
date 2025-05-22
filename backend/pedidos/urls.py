from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RyderViewSet, ComercioViewSet, ClienteViewSet, PedidoViewSet, RegistroUsuarioView, CustomLoginView, UserListView, UserUpdateView, UserDeleteView, EstadisticasPedidoView, ReporteComercioView

router = DefaultRouter()
router.register(r'ryders', RyderViewSet)
router.register(r'comercios', ComercioViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += [
    path('registro/', RegistroUsuarioView.as_view(), name='registro'),
]

urlpatterns += [
    path('token/', CustomLoginView.as_view(), name='token_obtain_pair'),
]

urlpatterns += [
    path('usuarios/', UserListView.as_view(), name='user-list'),
]

urlpatterns += [
    path('usuarios/<int:pk>/', UserUpdateView.as_view(), name='user-update'),
    path('usuarios/<int:pk>/eliminar/', UserDeleteView.as_view(), name='user-delete'),
]

urlpatterns += [
    path('estadisticas/', EstadisticasPedidoView.as_view(), name='estadisticas'),
    path('reportes-comercios/', ReporteComercioView.as_view(), name='reportes_comercios'),
]