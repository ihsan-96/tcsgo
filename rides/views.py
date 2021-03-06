from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import GroupsHistory, Cars, Points, Membership, Groups, Requests, Users
from .forms import RequestRideForm, ConfigureRideForm, SearchRideForm, AddRideForm, UserForm, UsersForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login
from .forms import CustomLoginForm
from collections import defaultdict

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('rides:groups')
    else:
        return login(request, authentication_form=CustomLoginForm)


def signup(request):
    if request.user.is_authenticated:
        return redirect('rides:groups')
    else:
        form = UserForm()
        context = {
        'form' : form
        }
        if request.method == 'POST' :
            form_return = UserForm(request.POST)
            if form_return.is_valid() :
                user = form_return.save(commit = False)
                username = form_return.cleaned_data['username']
                password = form_return.cleaned_data['password']
                user.set_password(password)
                user.save()
                user = authenticate(username = username, password = password)

                if user is not None :
                    if user.is_active:
                        login(request, user)
                        return redirect('rides:add_details')

        return render(request, 'rides/signup.html', context)

@login_required
def add_details(request):
    form = UsersForm()
    error_message = ""
    context = {
    'form' : form,
    'error_message' : error_message
    }
    if request.method == 'POST':
        form_return = UsersForm(request.POST)
        if form_return.is_valid():
            user = User.objects.get(id = request.user.id)
            users = Users.objects.create(user_reference = user.id,
            first_name = user.first_name,
            last_name = user.last_name,
            email = user.email,
            sex = request.POST['sex'],
            phone_number = request.POST['phone_number'],
            dl_number = request.POST['dl_number'],
            blood_group = request.POST['blood_group'],
            employee_number = request.POST['employee_number'],
            card_number = request.POST['card_number'],
            )
            return redirect('rides:groups')
        else:
            error_message="Some of the information given here is already used."

    return render(request, 'rides/add_details.html', context)


@login_required
def groups(request):
    user_id = request.user.id
    user = Users.objects.get(user_reference = user_id)
    groups_history_list = GroupsHistory.objects.filter( members__id=user.id ).order_by('-date')

    distinct_groups = defaultdict(int)
    ghlist = []

    for group_history in groups_history_list:
        if distinct_groups[group_history.group_id] == 0:
            ghlist.append(group_history)

        distinct_groups[group_history.group_id] += 1

    groups_owner_list = Groups.objects.filter( owner_id=user.id ).distinct()
    # groups_active_list = filter from groups where he is a member
    context = {
    'groups_history_list' : ghlist,
    'groups_owner_list' : groups_owner_list,
    'user_id' : user.id
    }
    return render(request, 'rides/groups.html', context)


@login_required
def group_member(request, group_id):
    group = Groups.objects.get(id = group_id)
    error_message = ''
    user_id = request.user.id
    user = Users.objects.get(user_reference = user_id)
    if request.method == 'POST':
        if 'delete_request' in request.POST:
            r = Requests.objects.get(id = request.POST['request_id'])
            r.delete()
        if 'leave_trip' in request.POST:
            if request.POST['member_id']:
                m = Membership.objects.get(id = request.POST['member_id'])
                requests = Requests.objects.filter(trip_type=m.trip_type, user_id=m.user_id)
                for req in requests :
                    req.request_status='pending'
                    req.save()
                m.delete()
        if 'join_ride' in request.POST:
            if group.status == 'trip1':
                trip_type = 1
                user.ride_status = 'trip1'
                user.save()
            elif group.status == 'trip2':
                trip_type = 1
                user.ride_status = 'trip2'
                user.save()
            else :
                error_message = "Ride hasn't started."
            requests = Requests.objects.filter(user_id = user.id, trip_type=trip_type)
            for req in requests:
                req.delete()
        if 'end_ride' in request.POST:
            if group.status == 'trip1':
                user.ride_status = 'idle'
                user.save()
                m = Membership.objects.get(user=user, group=group, trip_type=1)
                m.delete()
            elif group.status == 'trip2':
                user.ride_status = 'idle'
                user.save()
                m = Membership.objects.get(user=user, group=group, trip_type=2)
                m.delete()
            else :
                error_message = "Ride hasn't started."
    requests = Requests.objects.filter(user_id = user.id, group=group, request_status='pending')
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
    'user' : user,
    'user_id' : user.id,
    'trip1_status' : trip1_status,
    'trip2_status' : trip2_status,
    'available_seats_trip1' : available_seats_trip1,
    'available_seats_trip2' : available_seats_trip2,
    'trip1_members' : trip1_members,
    'trip2_members' : trip2_members,
    'trip1_members_list' : trip1_members_list,
    'trip2_members_list' : trip2_members_list,
    'error_message' : error_message
    }
    if request.method == 'POST':
        return render(request, 'rides/group_member.html', context)
    return render(request, 'rides/group_member.html', context)


@login_required
def request_ride(request, group_id):
    user_id = request.user.id
    user = Users.objects.get(user_reference = user_id)
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
    'trip2_points' : trip2_points,
    }
    if request.method == 'POST':
        if 'cancel' in request.POST :
            return redirect('rides:group_member',group_id)
        elif 'request' in request.POST :
            post_data = request.POST.copy()
            if (post_data['trip_type'][0] == '1' and group.start_point.id == 1) or (post_data['trip_type'][0] == '2' and group.end_point.id == 1) or (group.status != 'idle'):
                context['error_message'] = 'Ride Not Available.'
                form = RequestRideForm()
                return render(request, 'rides/request_ride.html', context)
            elif (post_data['point'] not in trip1_points and post_data['trip_type'][0] == '1' and int(post_data['point']) != group.start_point.id) or (post_data['point'] not in trip2_points and post_data['trip_type'][0] == '2' and int(post_data['point']) != group.end_point.id):
                context['error_message'] = 'This ride is not through your area'
                form = RequestRideForm()
                return render(request, 'rides/request_ride.html', context)
            else :
                post_data['group'] = group_id
                post_data['user'] = user.id
                form_return = RequestRideForm(post_data)
                if form_return.is_valid():
                    form_return.save()
                    return redirect('rides:group_member',group_id)
                else :
                    context['error_message'] = 'ERROR: You might have requested earlier'
                    form = RequestRideForm()
                    return render(request, 'rides/request_ride.html', context)
    return render(request, 'rides/request_ride.html', context)




@login_required
def group_owner(request, group_id):
    user_id = request.user.id
    user = Users.objects.get(user_reference = user_id)
    trip1_members = Membership.objects.filter(group_id=group_id).filter(trip_type=1)
    trip2_members = Membership.objects.filter(group_id=group_id).filter(trip_type=2)
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
            requests = Requests.objects.filter(trip_type=trip_type, user=u)
            for req in requests :
                req.request_status='accepted'
                req.save()
        if 'remove_member' in request.POST:
            m = Membership.objects.get(id = request.POST['member_id'])
            requests = Requests.objects.filter(trip_type=m.trip_type, user_id=m.user_id)
            for req in requests :
                req.request_status='pending'
                req.save()
            m.delete()
        if 'start_ride' in request.POST:
            g = Groups.objects.get(id = group_id)
            #Change Availability
            if request.POST['trip_type'] == 'enroute' :
                print(g.status)
                g.status = 'trip1'
                requests = Requests.objects.filter(trip_type=1, group_id=group_id)
            else :
                g.status = 'trip2'
                requests = Requests.objects.filter(trip_type=2, group_id=group_id)
            g.save()

            for req in requests :
                req.delete()
        if 'end_ride' in request.POST:
            g = Groups.objects.get(id = group_id)
            i = Points.objects.get(id = 1)
            if g.status == 'trip1' :
                gh = GroupsHistory.objects.create(group_id = group_id,
                source = g.start_point,
                destination_id = 7,
                pay_status = g.pay_status)
                #Give Destination value as TCS
                g.start_point = i
                for member in trip1_members:
                    u = member.user
                    u.ride_status = 'idle'
                    u.save()
            if g.status == 'trip2' :
                gh = GroupsHistory.objects.create(group_id = group_id,
                source_id = 7,
                destination = g.end_point,
                pay_status = g.pay_status)
                #Give Destination value as TCS
                g.end_point = i
                for member in trip2_members:
                    u = member.user
                    u.ride_status = 'idle'
                    u.save()
            for m in g.members.all():
                gh.members.add(m)#Bug-Both trip1 and trip2 members will be added to both histories..!! filter with through model field "trip_type"-bug
            g.status = 'idle'
            g.members.clear() #Bug-This clears all the members irrspective of trip_type- bug
            g.save()
            return redirect('rides:group_owner',group_id)
    group = Groups.objects.get(id = group_id)
    requests = Requests.objects.filter(group_id = group_id).filter(request_status='pending')
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

    return render(request, 'rides/group_owner.html', context)

@login_required
def configure_ride(request, group_id):
    group = Groups.objects.get(id = group_id)
    if request.method == 'POST':
        if 'cancel' in request.POST :
            return redirect('rides:group_owner',group_id)
        post_data = request.POST.copy()
        post_data['owner'] = group.owner_id
        post_data['car'] = group.car_id     #Add if configure ride disabled ride, remove members and delete requests related to that trip type.
        form_return = ConfigureRideForm(post_data, instance = group)
        print(form_return.is_valid())
        print(form_return.errors)
        if form_return.is_valid():
            form_return.save()
            if post_data['start_point'] == '1' :
                group.trip1_intermediate_points.clear()
            if post_data['end_point'] == '1' :
                group.trip2_intermediate_points.clear()
            return redirect('rides:group_owner',group_id)
    form = ConfigureRideForm(instance = group)

    context = {
     'form': form,
     'group': group
     }
    return render(request, 'rides/configure_ride.html', context)
    #Add constraints to configure by considering riders also


@login_required
def search_ride(request):
    if request.method == 'POST' :
        point_id = int(request.POST['point'])
        return redirect('rides:search_results',  point_id)
    form = SearchRideForm()
    context = {
    'form' : form
    }
    return render(request, 'rides/search_ride.html', context)


@login_required
def search_results(request, point_id):
    user_id = request.user.id
    user = Users.objects.get(user_reference = user_id)
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
    'user_id' : user.id
    }
    return render(request, 'rides/search_results.html', context)


@login_required
def add_ride(request):
    user_id = request.user.id
    user = Users.objects.get(user_reference = user_id)
    form = AddRideForm()
    error_message = ''
    context = {
    'form' : form,
    'error_message' : error_message
    }
    if request.method == 'POST' :
        post_data = request.POST.copy()
        post_data['owner'] = user.id
        car_number = post_data['car_number']
        form_return = AddRideForm(post_data)
        if form_return.is_valid():
            print("reached ")
            form_return.save()
            car = Cars.objects.get(car_number = car_number)
            new_group = Groups.objects.create(owner = user, car = car)
            return redirect('rides:groups')
        else :
            error_message = 'ERROR: Car already exists.'
            form = AddRideForm()
            return render(request, 'rides/add_ride.html', context)
    return render(request, 'rides/add_ride.html', context)
