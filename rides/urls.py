from django.urls import path
from . import views

app_name = 'rides'

urlpatterns = [
    # ex: signup/
    path('signup/', views.signup, name='signup'),

    # ex: login/
    path('login/', views.custom_login, name='login'),

    # ex: /signup/add_details
    path('signup/add_details', views.add_details, name='add_details'),

    # ex: /rides/5
    path('', views.groups, name='groups'),

    # ex: /rides/5/member
    path('<int:group_id>/member/', views.group_member, name='group_member'),

    # ex: /rides/5/member/request_ride/
    path('<int:group_id>/member/request_ride', views.request_ride, name='request_ride'),

    # ex: /rides/5/owner
    path('<int:group_id>/owner', views.group_owner, name='group_owner'),

    # ex: /rides/5/owner/configure_ride/
    path('<int:group_id>/owner/configure_ride', views.configure_ride, name='configure_ride'),

    # ex: /rides/search_ride
    path('search_ride/', views.search_ride, name='search_ride'),

    # ex: /rides/search_ride/3
    path('search_ride/<int:point_id>', views.search_results, name='search_results'),

    # ex: /rides/add_ride/2
    path('add_ride/', views.add_ride, name='add_ride'),

]
