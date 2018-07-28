from django.http import HttpResponse

from django.db.models import Q

from django.shortcuts import render, redirect

from .models import GroupsHistory, Cars, Points, Membership, Groups, Requests, Users

from .forms import RequestRideForm, ConfigureRideForm, SearchRideForm, AddRideForm


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

    if group.start_point.id == 1 :
        trip1_status = 'Not Available'
    if available_seats_trip1 == 0 :
        trip1_status = 'Pool is full'

    if group.end_point.id == 1 :
        trip2_status = 'Not Available'
    if available_seats_trip2 == 0 :
        trip2_status = 'Pool is full'


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
    trip1_points = group.trip1_intermediate_points.all().values_list('id', flat=True)
    trip2_points = group.trip2_intermediate_points.all().values_list('id', flat=True)
    trip1_points = list(map(str, trip1_points))
    trip2_points = list(map(str, trip2_points))
    error_message = ''
    form = RequestRideForm()
    context = {
    'form' : form,
    'group' : group,
    'error_message' : error_message,
    'trip1_points' : trip1_points,
    'trip2_points' : trip2_points
    }
    if request.method == 'POST':
        if 'cancel' in request.POST :
            return redirect('rides:group_member',group_id,user_id)
        elif 'request' in request.POST :
            post_data = request.POST.copy()
            if (post_data['trip_type'][0] == '1' and group.start_point.id == 1) or (post_data['trip_type'][0] == '2' and group.end_point.id == 1) :
                context['error_message'] = 'Ride Not Available.'
                form = RequestRideForm()
                return render(request, 'rides/request_ride.html', context)
            elif (post_data['point'] not in trip1_points and post_data['trip_type'][0] == '1' and post_data['point'] != group.start_point.id) or (post_data['point'] not in trip2_points and post_data['trip_type'][0] == '2' and post_data['point'] != group.end_point.id):
                context['error_message'] = 'This ride is not through your area'
                form = RequestRideForm()
                return render(request, 'rides/request_ride.html', context)
            else :
                post_data['group'] = group_id
                post_data['user'] = user_id
                form_return = RequestRideForm(post_data)
                if form_return.is_valid():
                    form_return.save()
                    return redirect('rides:group_member',group_id,user_id)
                else :
                    context['error_message'] = 'ERROR: You might have requested earlier'
                    form = RequestRideForm()
                    return render(request, 'rides/request_ride.html', context)
    return render(request, 'rides/request_ride.html', context)





def group_owner(request, group_id):

    if request.method == 'POST':
        if 'reject_request' in request.POST:
            r = Requests.objects.get(id = request.POST['request_id'])
            r.delete()
        if 'accept_request' in request.POST:
            r = Requests.objects.get(id = request.POST['request_id'])
            g = Groups.objects.get(id = group_id)
            u = Users.objects.get(id = r.user_id)
            p = r.point
            trip_type = r.trip_type
            m = Membership.objects.create(trip_type = trip_type, group = g, user = u, point = p)
            r.delete()
        if 'remove_member' in request.POST:
            m = Membership.objects.get(id = request.POST['member_id'])
            m.delete()

    group = Groups.objects.get(id = group_id)
    requests = Requests.objects.filter(group_id = group_id)
    trip1_members = Membership.objects.filter(group_id=group_id).filter(trip_type=1)
    trip2_members = Membership.objects.filter(group_id=group_id).filter(trip_type=2)
    available_seats_trip1 = group.seats_offered - trip1_members.count()
    available_seats_trip2 = group.seats_offered - trip2_members.count()
    seats_offered = group.seats_offered
    trip1_status = 'Available'
    trip2_status = 'Available'

    if group.start_point.id == 1 :
        trip1_status = 'Not Available'

    if group.end_point.id == 1 :
        trip2_status = 'Not Available'

    context = {
    'requests' : requests,
    'group' : group,
    'trip1_status' : trip1_status,
    'trip2_status' : trip2_status,
    'available_seats_trip1' : available_seats_trip1,
    'available_seats_trip2' : available_seats_trip2,
    'seats_offered' : seats_offered,
    'trip1_members' : trip1_members,
    'trip2_members' : trip2_members,
    }

    if request.method == 'POST':
        return render(request, 'rides/group_owner.html', context)
    return render(request, 'rides/group_owner.html', context)


def configure_ride(request, group_id):
    group = Groups.objects.get(id = group_id)
    if request.method == 'POST':
        if 'cancel' in request.POST :
            return redirect('rides:group_owner',group_id)
        post_data = request.POST.copy()
        post_data['owner'] = group.owner_id
        post_data['car'] = group.car_id
        form_return = ConfigureRideForm(post_data, instance = group)
        print(form_return.is_valid())
        print(form_return.errors)
        if form_return.is_valid():
            form_return.save()
            print('valid')
            return redirect('rides:group_owner',group_id)
    form = ConfigureRideForm(instance = group)

    context = {
     'form': form,
     'group': group
     }
    return render(request, 'rides/configure_ride.html', context)
    #Add constraints to configure by considering riders also


def search_ride(request, user_id):
    if request.method == 'POST' :
        point_id = int(request.POST['point'])
        return redirect('rides:search_results', user_id,  point_id)
    form = SearchRideForm()
    context = {
    'form' : form
    }
    return render(request, 'rides/search_ride.html', context)


def search_results(request, user_id, point_id):
    trip1_ip = list(Points.objects.get(id = point_id).trip1_intermediate_points.all())
    trip1_sp = list(Groups.objects.filter(start_point_id = point_id))
    trip1 = trip1_sp + trip1_ip
    trip1.sort(key=lambda x: x.trip1_time)
    trip2_ip = list(Points.objects.get(id = point_id).trip2_intermediate_points.all())
    trip2_sp = list(Groups.objects.filter(end_point_id = point_id))
    trip2 = trip2_sp + trip2_ip
    trip2.sort(key=lambda x: x.trip2_time)
    context = {
    'trip1_list' : trip1,
    'trip2_list' : trip2,
    'user_id' : user_id
    }
    return render(request, 'rides/search_results.html', context)


# def request_ride(request, group_id, user_id):
#     group = Groups.objects.get(id = group_id)
#     trip1_points = group.trip1_intermediate_points.all().values_list('id', flat=True)
#     trip2_points = group.trip2_intermediate_points.all().values_list('id', flat=True)
#     trip1_points = list(map(str, trip1_points))
#     trip2_points = list(map(str, trip2_points))
#     error_message = ''
#     form = RequestRideForm()
#     context = {
#     'form' : form,
#     'group' : group,
#     'error_message' : error_message,
#     'trip1_points' : trip1_points,
#     'trip2_points' : trip2_points
#     }
#     if request.method == 'POST':
#         if 'cancel' in request.POST :
#             return redirect('rides:group_member',group_id,user_id)
#         elif 'request' in request.POST :
#             post_data = request.POST.copy()
#             if (post_data['trip_type'][0] == '1' and group.start_point.id == 1) or (post_data['trip_type'][0] == '2' and group.end_point.id == 1) :
#                 context['error_message'] = 'Ride Not Available.'
#                 form = RequestRideForm()
#                 return render(request, 'rides/request_ride.html', context)
#             elif (post_data['point'] not in trip1_points and post_data['trip_type'][0] == '1' and post_data['point'] != group.start_point.id) or (post_data['point'] not in trip2_points and post_data['trip_type'][0] == '2' and post_data['point'] != group.end_point.id):
#                 context['error_message'] = 'This ride is not through your area'
#                 form = RequestRideForm()
#                 return render(request, 'rides/request_ride.html', context)
#             else :
#                 post_data['group'] = group_id
#                 post_data['user'] = user_id
#                 form_return = RequestRideForm(post_data)
#                 if form_return.is_valid():
#                     form_return.save()
#                     return redirect('rides:group_member',group_id,user_id)
#                 else :
#                     context['error_message'] = 'ERROR: You might have requested earlier'
#                     form = RequestRideForm()
#                     return render(request, 'rides/request_ride.html', context)
#     return render(request, 'rides/request_ride.html', context)

def add_ride(request, user_id):
    form = AddRideForm()
    error_message = ''
    context = {
    'form' : form
    }
    if request.method == 'POST' :
        post_data = request.POST.copy()
        post_data['owner'] = user_id
        car_number = post_data['car_number']
        form_return = AddRideForm(post_data)
        if form_return.is_valid():
            form_return.save()
            car = Cars.objects.get(car_number = car_number)
            user = Users.objects.get(id = user_id)
            new_group = Groups.objects.create(owner = user, car = car)
            return redirect('rides:groups', user_id)
        else :
            context['error_message'] = 'ERROR: Car already exists.'
            form = AddRideForm()
            return render(request, 'rides/add_ride.html', context)
    return render(request, 'rides/add_ride.html', context)
