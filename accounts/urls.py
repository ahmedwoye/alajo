from django.urls import path
from . import views 
from .views import render_pdf_view, CustomerListView

urlpatterns = [
    path('register/', views.registerpage,name='register'),
    path('login/', views.loginpage,name='login'),
    path('logout/', views.logoutUser,name='logout'),

    path('', views.home, name="home"),
    path('user/', views.userPage,name='user-page'),
    path('products/', views.products,name='products'),
    path('customer/<str:pk_test>/', views.customer,name='customer'),
    path('sales/', views.sales,name='sales'),
    path('status/', views.status, name='status'),
    path('payment/', views.payment, name='payment'),
    path('account/', views.accountSettings, name='account'),
    path('create_order/', views.createOrder, name ='create_order'),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),
    path('pdf/', views.render_pdf_view,name='test-pdf-report'),
    path('test/', CustomerListView.as_view(), name='customer-list-view'),
 ]