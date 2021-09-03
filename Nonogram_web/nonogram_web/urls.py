from django.urls import path
from . import views
#URLConf
urlpatterns = [
    path('', views.dim_web),
    path('cord', views.cord_web),
    path('generate', views.generate_web)
]