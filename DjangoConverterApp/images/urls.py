from django.urls import path
from . import views

urlpatterns = [
    path('', views.imgtopdf, name="imgtopdf"),
    path('jpgtopng', views.jpgtopng),
    path('png', views.png),
<<<<<<< HEAD
    path('txttopdf', views.txttopdf),
    path('docxtopdf', views.docxtopdf, name='docxtopdf'),
    

=======
    path('docxtopdf', views.docxtopdf),
    path('pdftodocx', views.pdftodocx),
    path('txttopdf', views.txttopdf),
    path('txttodocx', views.txttodocx),
>>>>>>> 2cf472b40ebbff862dde93cfb088d3b04e8e97d6
]
