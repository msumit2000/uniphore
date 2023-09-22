from django.urls import path, include
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('login', jwt_views.TokenObtainPairView.as_view(), name='login'),
    # API for UI
    path('udops/create_corpus/', views.create_corpus.as_view()),
    path('udops/add/', views.add.as_view()),
    path('udops/remote/', views.remote.as_view()),
    path('udops/commit/', views.commit.as_view()),
    path('udops/push/', views.push.as_view()),
    path('udops/clone/', views.clone.as_view()),
    path('udops/pull/', views.pull.as_view()),
    #   corpus API
    path('udops/corpus/count/', views.get_udops_count.as_view()),
    path('udops/corpus/summary/', views.summary.as_view()),
    path('udops/corpus/list/', views.get_corpus_list.as_view()),
    path('udops/corpus/search/', views.search_corpus.as_view()),
    path('udops/corpus/upsert/', views.upsert.as_view()),
    path('udops/corpus/donut/', views.donut.as_view()),
    path('udops/corpus/summary_custom/', views.summary_custom.as_view()),
    path('udops/corpus/update_custom_field/', views.update_custom_field.as_view()),
    path('udops/corpus/language/', views.language.as_view()),
    path('udops/corpus/source_type/', views.source_type.as_view()),
    path('udops/corpus/corpus_type/', views.corpus_type.as_view()),
    ### dataset API ####
    # path('udops/dataset/count/', views.get_datset_count.as_view()),
    # path('udops/dataset/summary/', views.dataset_summary.as_view()),
    # path('udops/dataset/list/', views.dataset_list.as_view()),
    # path('udops/dataset/search/', views.dataset_search.as_view()),
    # path('udops/dataset/update/', views.update_dataset.as_view()),
    # path('udops/dataset/corpus_list/', views.dataset_corpus_list.as_view()),
    ### user management API ###
    path('udops/user/list/', views.list_user.as_view()),
    path('udops/user/upsert_user/', views.upsert_user.as_view()),
    path('udops/team/list/', views.team_list.as_view()),
    path('udops/team/upsert/', views.team_upsert.as_view()),
    path('udops/team/admin_upsert/', views.upsert_admin.as_view()),
    path('udops/team/admin_upsert/', views.remove_admin.as_view()),
    path('udops/team/add_users_team/', views.add_users_team.as_view()),
    path('udops/team/remove_users/', views.remove_users_team.as_view()),
    path('udops/user/access_permission/', views.grant_corpus.as_view()),
    path('udops/user/remove_permission/', views.remove_user_corpus.as_view()),
    path('udops/user/corpus_access_list_write/', views.grant_corpus_list_write.as_view()),
    path('udops/user/corpus_access_list_read/', views.grant_corpus_list_read.as_view()),
    path('udops/user/list_teams_read/', views.get_list_teams_read.as_view()),
    path('udops/user/list_teams_write/', views.get_list_teams_write.as_view()),
    path('udops/user/team_permission_read/', views.grant_team_pemission_read.as_view()),
    path('udops/user/team_permission_write/', views.grant_team_pemission_write.as_view()),
    path('udops/user/remove_team_access_permission/', views.remove_access_team.as_view()),
    path('udops/team/existing_users/', views.existing_users.as_view()),
    path('udops/team/not_existing_users/', views.not_existing_users.as_view()),
    path('udops/team/add_team/', views.add_team.as_view()),
    path('udops/team/delete_team/', views.delete_team.as_view()),
    path('udops/user/add_user/', views.add_user.as_view()),
    path('udops/team/list_search_team/', views.get_team_list_search.as_view()),
    path('udops/user/list_search_user/', views.list_user_search.as_view()),
    path('udops/user/user_status/', views.user_status),
]
