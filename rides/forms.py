from django import forms
from .models import Requests, Groups, Points, Cars, Users
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm


class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'E-mail'})
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        labels = {
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
            'email': _('E-Mail Id'),
        }


class UsersForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sex'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Sex'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contact Number'})
        self.fields['dl_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Driving License Number'})
        self.fields['blood_group'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Blood Group'})
        self.fields['employee_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Employee Number'})
        self.fields['card_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Card Number'})
    class Meta:
        model = Users
        fields = ['sex', 'phone_number', 'dl_number', 'blood_group', 'employee_number', 'card_number']
        labels = {
            'sex': _('Gender'),
            'phone_number': _('Contact Number'),
            'dl_number': _('Driving License Number'),
            'blood_group': _('Blood Group'),
            'employee_number': _('Employee Number'),
            'card_number': _('Card Number'),
        }


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['point'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Place'})
        self.fields['trip_type'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Select Ride'})
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_point'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Start Point'})
        self.fields['end_point'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Destination'})
        self.fields['trip1_intermediate_points'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enroute Intermediate Points'})
        self.fields['trip2_intermediate_points'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Return Intermediate Points'})
        self.fields['seats_offered'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Seats Offered'})
        self.fields['pay_status'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Pay Status'})
        self.fields['trip1_time'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enroute Start Time'})
        self.fields['trip2_time'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Return Start Time'})

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
