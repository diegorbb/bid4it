from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Auth paths
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_user, name='logout'),

    # Product paths
    path('product/<str:pk>', views.product_page, name='product-page'),
]
