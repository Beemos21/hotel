from django.db import models
from django.contrib.auth.models import User
import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from djmoney.models.fields import MoneyField
from django_countries.fields import CountryField
from roomManager.models import Room, RoomType
from django.contrib import admin


class Visitor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Identity_Card = (('Passport', 'Passport'), ('National ID', 'national identity'),)
    Identity_card_type = models.CharField(max_length=11, choices=Identity_Card, default='Passport')
    passport_picture = models.ImageField(null=True, upload_to='_img/')

    Identity_Card_number = models.CharField(max_length=20, null=True)
    birth_date = models.DateField(null=True, blank=True)
    nationality = CountryField(blank=True, default='Saudi Arabia')

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.user.username


class Service(models.Model):
    name = models.CharField(max_length=20)
    price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.name


class Reservation(models.Model):
    BOOKING_type = (('B', 'Booking'),
                    ('R', 'Reception'),
                    ('T', 'Telephon'),
                    ('E', 'Email'))
    type = models.CharField(max_length=20, choices=BOOKING_type, default='B')
    BOOKING_STATUS = (('A', 'Available'),
                      ('B', 'Booked'),
                      ('C1', 'Cancelled by user'),
                      ('C2', 'Cancelled by Manager')
                      )
    booking_status = models.CharField(max_length=2, choices=BOOKING_STATUS, default='B')
    customer = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    From_date = models.DateTimeField(verbose_name="From", blank=True, null=True)
    To_date = models.DateTimeField(verbose_name="To", null=True, blank=True)
    nb_days = models.PositiveIntegerField(verbose_name="nb_days", default=1)
    deadline_free_Cancelation = models.DateTimeField(blank=True, null=True)
    roomtype = models.ManyToManyField(RoomType, through='RoomBooked')
    _total_cost = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    _discounted_price = MoneyField(
        decimal_places=2,
        default=0,
        default_currency='USD',
        max_digits=11,
    )
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.customer.user.username


class RoomBooked(models.Model):
    type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    booking = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    nb_Adults = models.PositiveIntegerField(verbose_name="Adults", default=1)  # nb od guests 1 or 2
    nb_Children = models.PositiveIntegerField(verbose_name="Children", default=0)  # nb od guests 1 or 2
    services = models.ManyToManyField(Service, related_name='services', through='ServiceBooked')
    visitor = models.ManyToManyField(Visitor, related_name='visitors', through='RoomVisitor')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class RoomBooked_Inline(admin.TabularInline):
    model = RoomBooked
    extra = 1


class RoomVisitor(models.Model):
    roombooked = models.ForeignKey(RoomBooked, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class RoomVisitor_Inline(admin.TabularInline):
    model = RoomVisitor
    extra = 1


class RoomVisitorAdmin(admin.ModelAdmin):
    inlines = (RoomVisitor_Inline,)


class ServiceBooked(models.Model):
    room = models.ForeignKey('RoomBooked', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    qte = models.PositiveIntegerField()

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class ServiceBooked_Inline(admin.TabularInline):
    model = ServiceBooked
    extra = 1


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['booking_status', 'customer', 'From_date', 'To_date', 'nb_days',
                    'deadline_free_Cancelation', '_total_cost', '_discounted_price']
    fields = [('booking_status', 'customer'), ('From_date', 'To_date'),
              'nb_days', 'deadline_free_Cancelation', ('_total_cost', '_discounted_price')]
    inlines = (RoomBooked_Inline,)


class RoomBookedAdmin(admin.ModelAdmin):
    fields = ['room', ('nb_Adults', 'nb_Children')]
    inlines = (ServiceBooked_Inline,)


class CheckIn(models.Model):
    booking = models.ForeignKey(Reservation, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Visitor, related_name='customer', on_delete=models.CASCADE, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)
    check_in_date = models.DateTimeField(auto_now_add=True)
    check_out_date = models.DateTimeField(auto_now_add=True)
    nb_Adults = models.PositiveIntegerField(verbose_name="Adults", default=1)  # nb od guests 1 or 2
    nb_Children = models.PositiveIntegerField(verbose_name="Children", default=0)  # nb od guests 1 or 2
    visitor = models.ManyToManyField(Visitor, through='CheckInVisitor')

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.room.title


class CheckInVisitor(models.Model):
    checkin = models.ForeignKey(CheckIn, on_delete=models.CASCADE)
    visitor = models.ForeignKey(Visitor, on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class CheckInVisitor_Inline(admin.TabularInline):
    model = CheckInVisitor
    extra = 1


class CheckInVisitorAdmin(admin.ModelAdmin):
    inlines = (CheckInVisitor_Inline,)


class Review(models.Model):
    usr = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=29, null=True)
    comment = models.TextField(max_length=250)  # models.IntegerField(default = 0)
    rate = models.PositiveIntegerField(default=3, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.comment


class Payment(models.Model):
    customer = models.ForeignKey('Visitor', on_delete=models.CASCADE)

    def __str__(self):
        return self.customer
