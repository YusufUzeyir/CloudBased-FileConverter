from django.urls import path
from . import views

urlpatterns = [
    path('', views.imgtopdf, name="imgtopdf"),
    path('jpgtopng', views.jpgtopng),
    path('png', views.png),
    path('docxtopdf', views.docxtopdf),
    path('pdftodocx', views.pdftodocx),
    path('txttopdf', views.txttopdf),
    path('txttodocx', views.txttodocx),
]
