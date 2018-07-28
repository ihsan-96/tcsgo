from django import forms

from .models import Requests, Groups, Points, Cars

from django.utils.translation import gettext_lazy as _


class AddRideForm(forms.ModelForm):
    class Meta:
        model = Cars
        fields = ['car_number', 'owner', 'car_name', 'mileage']
        widgets = { 'owner': forms.HiddenInput() }
        labels = {
            'car_number': _('Car Registration Number'),
            'car_name': _('Car Model'),
            'mileage': _('Mileage'),
        }
        help_texts = {
            'car_number': _('Ex : KL 07 AH 4050'),
            'car_name': _('Ex : Honda City'),
        }


class RequestRideForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['group', 'user', 'point', 'trip_type']
        widgets = { 'group': forms.HiddenInput(), 'user': forms.HiddenInput() }
        labels = {
            'point': _('Request Point'),
            'trip_type': _('Select Ride'),
        }
        help_texts = {
            'point': _('Place you wish.'),
            'trip_type': _('Select whether the ride is from or to the company'),
        }


class ConfigureRideForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ['owner', 'car', 'start_point', 'end_point',
        'trip1_intermediate_points', 'trip2_intermediate_points',
        'seats_offered', 'pay_status',
        'trip1_time', 'trip2_time'
        ]
        widgets = { 'owner': forms.HiddenInput(), 'car': forms.HiddenInput() }
        labels = {
            'start_point': _('Starting Point'),
            'end_point': _('Destination'),
            'trip1_intermediate_points': _('Enroute Touch Points'),
            'trip2_intermediate_points': _('Return Touch Points'),
            'seats_offered': _('Seats Offered'),
            'pay_status': _('Payment'),
            'trip1_time': _('Enroute Start Time'),
            'trip2_time': _('Return Start Time')
        }
        help_texts = {
            'start_point': _('Starting point of your enroute trip. Set "Not Set" itself to disable ride'),
            'end_point': _('Destination of your return trip. Set "Not Set" itself to disable ride'),
            'trip1_intermediate_points': _('Select the points where riders can join you in enroute trip'),
            'trip2_intermediate_points': _('Select the points where riders can join you in enroute trip'),
            'seats_offered': _('Seats offered in your car'),
            'pay_status': _('Set whether the ride is paid or not'),
            'trip1_time': _('Starting time of your enroute trip in "HH:MM:SS" format'),
            'trip2_time': _('Starting point of your return trip in "HH:MM:SS" format')
        }


class SearchRideForm(forms.Form):
    point = forms.ModelChoiceField(queryset=Points.objects.exclude(id = 1))
