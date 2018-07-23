from django.http import HttpResponse

from django.db.models import Q

from django.shortcuts import render, redirect

from .models import GroupsHistory, Cars, Points, Membership, Groups, Requests

from .forms import GroupMemberForm


def index(request):
    return HttpResponse("You're looking at index view of rider")
    #This the Index of Rider. Currently nothing is here

def groups(request, user_id):
    groups_history_list = GroupsHistory.objects.filter( members__id=user_id ).order_by('-date').distinct()
    groups_owner_list = Groups.objects.filter( owner_id=user_id ).distinct()
    context = {
    'groups_history_list' : groups_history_list,
    'groups_owner_list' : groups_owner_list,
    'user_id' : user_id
    }
    return render(request, 'rides/groups.html', context)
    #This is the my groups page.



def group_member(request, group_id, user_id):

    if request.method == 'POST':
        if 'delete_request' in request.POST:
            r = Requests.objects.get(id = request.POST['request_id'])
            r.delete()
        if 'leave_trip' in request.POST:
            if request.POST['member_id']:
                m = Membership.objects.get(id = request.POST['member_id'])
                m.delete()

    group = Groups.objects.get(id = group_id)
    requests = Requests.objects.filter(user_id = user_id)
    trip1_members = Membership.objects.filter(group_id=group_id).filter(trip_type=1)
    trip2_members = Membership.objects.filter(group_id=group_id).filter(trip_type=2)
    available_seats_trip1 = group.seats_offered - trip1_members.count()
    available_seats_trip2 = group.seats_offered - trip2_members.count()
    trip1_members_list=[i.user.id for i in trip1_members]
    trip2_members_list=[i.user.id for i in trip2_members]
    trip1_status = 'Available'
    trip2_status = 'Available'


    if group.start_point == 1 :
        trip1_status = 'Not Available'
    if available_seats_trip1 == 0 :
        trip1_status = 'Not Available'

    if group.end_point == 1 :
        trip2_status = 'Not Available'
    if available_seats_trip2 == 0 :
        trip2_status = 'Not Available'


    context = {
    'requests' : requests,
    'group' : group,
    'user_id' : user_id,
    'trip1_status' : trip1_status,
    'trip2_status' : trip2_status,
    'available_seats_trip1' : available_seats_trip1,
    'available_seats_trip2' : available_seats_trip2,
    'trip1_members' : trip1_members,
    'trip2_members' : trip2_members,
    'trip1_members_list' : trip1_members_list,
    'trip2_members_list' : trip2_members_list
    }
    if request.method == 'POST':
        return render(request, 'rides/group_member.html', context)
    return render(request, 'rides/group_member.html', context)



def request_ride(request, group_id, user_id):
    group = Groups.objects.get(id = group_id)
    if request.method == 'POST':
        if 'cancel' in request.POST :
            return redirect('rides:group_member',group_id,user_id)
        else :
            post_data = request.POST.copy()
            post_data['group'] = group_id
            post_data['user'] = user_id
            if 'enroute' in request.POST :
                post_data['trip_type'] = 1
            form = GroupMemberForm(post_data)
            if form.is_valid():
                form.save()
                return redirect('rides:group_member',group_id,user_id)
            #else: print error messages for time too
    form = GroupMemberForm()
    context = {
    'form' : form,
    'group' : group,
    }

    return render(request, 'rides/request_ride.html', context)
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
