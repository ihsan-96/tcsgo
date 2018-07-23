from django import forms

from .models import Requests

from django.utils.translation import gettext_lazy as _

# class DeleteRequestForm(forms.ModelForm):
#     class Meta:
#         model = Requests
#         fields = ['point']
#         widgets = { 'point': forms.HiddenInput() }

class GroupMemberForm(forms.ModelForm):
    class Meta:
        model = Requests
        fields = ['group', 'user', 'point', 'trip_type']
        widgets = { 'group': forms.HiddenInput(), 'user': forms.HiddenInput() }
        labels = {
            'point': _('Request Point'),
            'trip_type': _('Select Ride'),
        }
        help_texts = {
            'point': _('Place you wish to enter.'),
            'trip_type': _('Select whether the ride is from or to the company'),
        }
