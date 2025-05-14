from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('updatePassword/', views.updatePassword, name='updatePassword'),
    path('updateUser/', views.updateUser, name='updateUser'),
    path('updateInfo/', views.updateInfo, name='updateInfo'),
    path('product/<int:pk>', views.product, name='product'),
    path('category/<str:foo>', views.category, name='category'),
    path('categorySummary/', views.categorySummary, name='categorySummary'),
    path('search/', views.search, name='search'),
]
