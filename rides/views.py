from django.http import HttpResponse

from django.db.models import Q

from django.shortcuts import render

from .models import GroupsHistory

from .models import Groups

from .models import Cars


def index(request):
    return HttpResponse("You're looking at index view of rider")
    #This the Index of Rider. Currently nothing is here

def groups(request, user_id):
    groups_list = GroupsHistory.objects.filter( Q(members__id=user_id) | Q(owner_id=user_id) ).order_by('-date').distinct()
    context = {
    'groups_list' : groups_list,
    'user_id' : user_id
    }
    return render(request, 'rides/groups.html', context)
    #This is the my groups page.


def group_member(request, group_id):
    context = {
    group = Groups.objects.get(id = group_id)
    }
    #This is the group expansion for group member.


def request_ride(request, group_id):
    return HttpResponse("You're requesting group %s as member." % group_id)
    #This is the request ACTION in group expansion of group member


def group_owner(request, group_id):
    return HttpResponse("You're looking at owner's page of group %s for configuration." % group_id)
    #This is the group expansion for group owner.


def configure_ride(request, group_id):
    return HttpResponse("You're configuring group %s." % group_id)
    #This is the ACTION configuring the ride in group expansion of group owner


def search_ride(request):
    response = "You're looking at the finding new rides page"
    return HttpResponse(response)
    #This is the page where user search for new rides


def searching_ride(request, point_id):
    return HttpResponse("You're searching ride from point %s." % point_id)
    #This is the ACTION of searching new rides

def search_results(request, point_id):
    rides_list = Groups.objects.filter(Q(start_point_id=point_id) | Q(end_point_id=point_id) | Q(trip1_intermediate_points__id=point_id) | Q(trip2_intermediate_points__id=point_id) ).distinct()
    output = ', '.join([g.owner.last_name + ' - ' + g.car.car_name for g in rides_list])
    return HttpResponse(output)
    #This is the results page of searching new rides


def add_ride(request):
    return HttpResponse("You're looking at adding a new ride's page.")
    #This is the page for adding new cars, also an inactive group will be automatically added.


def adding_ride(request, user_id):
    return HttpResponse("You're adding a new ride by %s." % user_id)
    #This is the ACTION of adding new rides


def manage_request(request, group_id):
    return HttpResponse("You're looking at managing requests page of group %s." % group_id)
    #This is page where owner accepts or rejects requests, ACTION is also in this page
