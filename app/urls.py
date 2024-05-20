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
    path('list_product', views.list_product, name='list-item'),

    # User paths
    path('user/<int:pk>/my-bids/', views.user_bids, name='user-bids'),
    path('user/<int:pk>/my-listings', views.user_listings, name='user-listings'),
    path('my-listings/listing/<int:pk>/archive/', views.archive_listing, name='archive-listing'),
    path('my-listings/listing/<int:pk>/edit/', views.edit_listing, name='edit-listing'),
]
