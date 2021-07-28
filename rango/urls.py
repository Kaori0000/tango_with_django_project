from django.urls import path
from rango import views

app_name = 'rango'
 #mapping the HTML and views
urlpatterns = [
    path('', views.index, name='index'), #if empty, call views.index
    path('about/', views.about, name='about'), #if 'about/', call views.about
    path('category/<slug:category_name_slug>/', 
          views.show_category, name='show_category'),
]

