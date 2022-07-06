from django.contrib import admin
from .models import *
from roomManager.models import Room
# Register your models here.
from django.db import connection




admin.site.register(Reservation,ReservationAdmin)


admin.site.register(Review)
admin.site.register(Visitor)
admin.site.register(RoomVisitor,)
admin.site.register(RoomBooked, RoomBookedAdmin)







# class BookingAdmin(admin.ModelAdmin):
#     # list_display = ('id', 'title')
#
#     def formfield_for_manytomany(self, db_field, request, **kwargs):
#         print(request)
#         print('request===================')
#         print(db_field)
#
#         if db_field.name == "rooms":
#             kwargs["queryset"] = Room.objects.filter(is_active=True)
#             # print(kwargs["queryset"])
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     "select * from room_manager_room where is_active=1")
#
#                 row = cursor.fetchall()
#                 # print(row)
#
#
#         return super(BookingAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)
#     class Media:
#         # js = ("booking/js/was.js",)
#         js = ("booking/js/restriction.js",)
#
#
#
#
# admin.site.register(Reservation,BookingAdmin)
# # admin.site.register(Booking)
# admin.site.register(Service)
# admin.site.register(Review)