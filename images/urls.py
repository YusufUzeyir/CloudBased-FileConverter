from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('imgtopdf', views.imgtopdf),
    path('jpgtopng', views.jpgtopng),
    path('png', views.png),
    path('docxtopdf', views.docxtopdf),
    path('txttopdf', views.txttopdf),
    path('pdftodocx', views.pdftodocx),
    path('txttodocx', views.txttodocx),
    
]
