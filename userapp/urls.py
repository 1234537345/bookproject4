from django.urls import path
from .import views
urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('searchuser/', views.filtersearch, name='filter'),
    path('userbookdetails/<int:p_id>/', views.userbookdetails, name='bookdetails'),
    path('addtocart/<int:book_id>/', views.addtocart, name='addtocart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('increase/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove_cart/<int:item_id>/', views.remove_from_cart, name='remove_cart'),
    path('create-checkout-session/', views.create_checkout_session, name='create-checkout-session'),
    path('success/', views.success, name='success'),
    path('cancel/', views.cancel, name='cancel')

]