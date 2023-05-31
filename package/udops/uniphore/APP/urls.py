from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('count/', views.get_udops_count),
    path('summary/',views.summary),
    path('list/',views.get_corpus_list),
    path('search_by_name/',views.search_corpus_by_name),
    path('search_by_string/',views.list_by_string_name),
    path('upsert/', views.upsert),
    path('donut/', views.donut)

]
