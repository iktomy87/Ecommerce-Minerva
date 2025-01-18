from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.store, name='homepage'), 
    path('signup', views.Signup.as_view(), name='signup'), 
    path('login', views.Login.as_view(), name='login'), 
    path('logout', views.logout, name='logout'), 
    path('cart', views.CartView.as_view(), name='cart'),  
    path('check-out', views.CheckOut.as_view(), name='checkout'), 
    path('orders', views.OrderView.as_view(), name='orders'),  
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
