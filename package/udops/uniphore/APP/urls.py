from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('udops/corpus/count/', views.get_udops_count),
    path('udops/corpus/summary/',views.summary),
    path('udops/corpus/list/',views.get_corpus_list),
    path('udops/corpus/search/',views.search_corpus),
    path('udops/corpus/upsert/', views.upsert),
    path('udops/corpus/donut/', views.donut),
    path('udops/corpus/summary_custom/',views.summary_custom),
    path('udops/corpus/update_custom_field/',views.update_custom_field),
        ### dataset API ####
    path('udops/dataset/summary/',views.dataset_summary),
    path('udops/dataset/list/',views.dataset_list),
    path('udops/dataset/search/',views.dataset_search),
    path('udops/dataset/update/',views.update_dataset),
    path('udops/dataset/corpus_list/',views.dataset_corpus_list),
    ### user management API ###
    path('udops/user/list/',views.list_user),
    path('udops/user/upsert_user/',views.upsert_user),
    path('udops/team/list/',views.team_list),
    path('udops/team/upsert/',views.team_upsert),
    path('udops/team/add_users_team/',views.add_users_team),
    path('udops/team/remove_users/',views.remove_users_team),
    path('udops/user/access_permission/',views.grant_corpus),
    path('udops/user/remove_permission/',views.remove_user_corpus),
    path('udops/user/corpus_access_list_write/',views.grant_corpus_list_write),
    path('udops/user/corpus_access_list_read/',views.grant_corpus_list_read),
    path('udops/user/list_teams_read/',views.get_list_teams_read),
    path('udops/user/list_teams_write/',views.get_list_teams_write),
    path('udops/user/team_permission_read/',views.grant_team_pemission_read),
    path('udops/user/team_permission_write/',views.grant_team_pemission_write),
    path('udops/team/existing_users/',views.existing_users),
    path('udops/team/not_existing_users/',views.not_existing_users),
    path('udops/team/add_team/',views.add_team),
    path('udops/user/add_user/',views.add_user),
    path('udops/team/list_search_team/',views.get_team_list_search),
    path('udops/user/list_search_user/',views.list_user_search),
    path('udops/dataset/count/',views.get_datset_count),

]
