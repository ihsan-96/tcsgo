from django.urls import path

from . import views

urlpatterns = [
    # ex: /rides/
    path('', views.index, name='index'),

    # ex: /rides/5
    path('<int:user_id>/', views.groups, name='groups'),

    # ex: /rides/5/member
    path('<int:group_id>/member', views.group_member, name='group_member'),

    # ex: /rides/5/member/request_ride/
    path('<int:group_id>/member/request_ride', views.request_ride, name='request_ride'),

    # ex: /rides/5/owner
    path('<int:group_id>/owner', views.group_owner, name='group_owner'),

    # ex: /rides/5/owner/configure_ride/
    path('<int:group_id>/owner/configure_ride', views.configure_ride, name='configure_ride'),

    # ex: /rides/search_ride
    path('search_ride/', views.search_ride, name='search_ride'),

    # ex: /rides/search_ride/3
    path('search_ride/<int:point_id>', views.searching_ride, name='searching_ride'),

    # ex: /rides/search_ride/3/search_results
    path('search_ride/<int:point_id>/search_results', views.search_results, name='search_results'),

    # ex: /rides/add_ride
    path('add_ride/', views.add_ride, name='add_ride'),

    # ex: /rides/add_ride/2
    path('add_ride/<int:user_id>', views.adding_ride, name='adding_ride'),

    # ex: /rides/5/owner/manage_request/
    path('<int:group_id>/owner/manage_request', views.manage_request, name='manage_request'),

]
