from django.db import models
from django.contrib import admin

sex_choices = (
    ('1','male'),
    ('2','female'),
    ('3','other'),
)

blood_group_choices = (
    ('1','A+ve'),
    ('2','A-ve'),
    ('3','B+ve'),
    ('4','B-ve'),
    ('5','O+ve'),
    ('6','O-ve'),
    ('7','AB+ve'),
    ('8','AB-ve'),
)
class Users(models.Model):
    user_reference = models.IntegerField()
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    sex = models.CharField(max_length=10, choices=sex_choices)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    dl_number = models.CharField(max_length=15, unique=True)
    blood_group = models.CharField(max_length=5, choices=blood_group_choices)
    employee_number = models.CharField(max_length=25, unique=True)
    card_number = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

class Cars(models.Model):
    car_number = models.CharField(max_length=25, unique=True)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE)
    car_name = models.CharField(max_length=25)
    mileage = models.IntegerField(default=30)

    class Meta:
        unique_together = ('owner', 'car_number')

    def __str__(self):
        return self.car_number


class Points(models.Model):
    point_name = models.CharField(max_length=30)

    def __str__(self):
        return self.point_name

seats_offered_choices = (
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
    (6,'6'),
    (7,'7'),
)

pay_status_choices =(
    (0,'no pay'),
    (1,'paid'),
)

class Groups(models.Model):
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='owner')
    car = models.ForeignKey(Cars, on_delete=models.CASCADE)
    start_point = models.ForeignKey(Points, on_delete=models.CASCADE, default=1, related_name='start_point')
    end_point = models.ForeignKey(Points, on_delete=models.CASCADE, default=1, related_name='end_point')
    trip1_intermediate_points = models.ManyToManyField(Points, related_name='trip1_intermediate_points', default=1)
    trip2_intermediate_points = models.ManyToManyField(Points, related_name='trip2_intermediate_points', default=1)
    seats_offered = models.IntegerField(choices=seats_offered_choices, default=3)
    pay_status = models.IntegerField(choices=pay_status_choices,default=0)
    trip1_time = models.TimeField(blank=True, default='00:00:00')
    trip2_time = models.TimeField(blank=True, default='00:00:00')
    members = models.ManyToManyField(Users, through='Membership')

    class Meta:
        unique_together = ('owner', 'car')

    def __str__(self):
        return '%s %s - %s' % (self.owner.first_name, self.owner.last_name, self.car.car_name)

request_status_choices = (
    ('pending','pending'),
    ('ontrip','ontrip'),
    ('accepted','accepted'),
)


trip_type_choices = (
    (1,'Enroute'),
    (2,'Return'),
)


class Requests(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    point = models.ForeignKey(Points, on_delete=models.CASCADE, related_name='request_point')
    trip_type = models.IntegerField(choices=trip_type_choices, default=1)
    request_status = models.CharField(max_length=10, choices=request_status_choices,default='pending')

    class Meta:
        unique_together = ('group', 'user', 'point', 'trip_type')

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Membership(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    trip_type = models.IntegerField(choices=trip_type_choices)
    point = models.ForeignKey(Points, on_delete=models.CASCADE)


class GroupsHistory(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    source = models.ForeignKey(Points, on_delete=models.CASCADE, related_name='source')
    destination = models.ForeignKey(Points, on_delete=models.CASCADE, related_name='destination')
    pay_status = models.CharField(max_length=10)
    members = models.ManyToManyField(Users)
    date = models.DateField(auto_now=True)


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1


class UsersAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)


class GroupsAdmin(admin.ModelAdmin):
    inlines = (MembershipInline,)
