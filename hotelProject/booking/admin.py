from django.contrib import admin
from .models import *
from roomManager.models import Room
from django.contrib import admin
from .models import Visitor, Review, CheckIn, Reservation, Service, Payment
from django.conf import settings
from django.conf import settings


class inlineRoom(admin.StackedInline):
    model = Room
    extra = 1


class VisitorAdmin(admin.ModelAdmin):
    list_display = ['user', 'Identity_Card', 'birth_date', 'Identity_card_type', 'Identity_Card_number',
                    'passport_picture', 'nationality']


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'description']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['usr', 'title', 'comment', 'rate', 'created_at', 'updated_at']


class CheckInAdmin(admin.ModelAdmin):
    list_display = ['customer', 'room', 'check_in_date', 'check_out_date']


class ServiceBookedAdmin(admin.ModelAdmin):
    list_display = ['service', 'qte']


admin.site.register(ServiceBooked, ServiceBookedAdmin)
admin.site.register(RoomBooked, RoomBookedAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(CheckIn, CheckInAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Payment)
