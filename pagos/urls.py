from django.urls import path
from . import views

urlpatterns = [ 
    path('', views.VistaInicio.as_view(), name='inicio'),
    path('config/', views.configuracion_stripe),
    path('pago-orden/', views.proceder_pago_orden),
    path('aprobado/', views.VistaAprobado.as_view(), name='aprobado'),
    path('cancelado/', views.VistaCancelado.as_view(), name='cancelado'),
    path('webhook/', views.stripe_webhook),
]
