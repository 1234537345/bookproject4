from django.urls import path

from testbookapp import views

urlpatterns = [
    path('', views.wlcmpage, name='wlcm'),
    path('createbook/', views.createbook, name='create'),
    path('index/', views.index, name='index'),
    path('listdetails/', views.listdetails, name='list'),
    path('updatebook/<int:p_id>/', views.updatebook, name='update'),
    path('deletedetails/<int:p_id>/', views.deletedetails, name='delete'),
    path('detailsview/<int:p_id>/', views.viewdetails, name='details'),
    path('searchbook/', views.searchbook, name='search')

    ]





