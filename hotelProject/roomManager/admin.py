from django.conf import settings
from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'rtype', 'room_slug', 'rfloor', 'is_active', 'cover_image', 'featured',
                    'room_status', 'hotel']
    fields = [('title', 'rtype'), ('featured', 'is_active'), ('room_slug', 'cover_image'),
              ('room_status', 'hotel')]
    actions = ['set_room_to_book', ]

    def set_room_to_book(self, request, queryset):
        count = queryset.update(is_booked=False)
        self.message_user(request, '{} room change successfully.'.format(count))
    set_room_to_book.short_description = 'Mark selected Room to free'


admin.site.register(Room, RoomAdmin)


class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'reg_number', 'owner_name', 'address', 'city', 'state', 'phone']


admin.site.register(HotelInfo, HotelAdmin)
#

# admin.site.site_header = str(settings.STATIC_ROOT)  # 'Hotel Management System'
# admin.site.site_title = 'DAS-360 HMS '
# admin.site.index_title = 'Admin Panel- Das 360'


admin.site.register(RoomStatus)


class CityAdmin(admin.ModelAdmin):
    list_display = ['city_name', ]


admin.site.register(City, CityAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'area', 'bedType', 'capacity', 'price_per_Day', 'description',
                    'Air_Conditioning', 'wifi', 'tv', 'towels', 'hairdryer', 'bathrobe', 'toiletries', 'heater',
                    'Shampoo', 'Conditioner', 'bathtub', 'bidet', 'smooking', 'minibar', 'bottled_water', 'coffee',
                    'Electric_kettle', 'has_window', 'view', ]
    fields = ['type_name', ('area','bedType'), ('capacity', 'price_per_Day', 'description'),
                   ( 'Air_Conditioning', 'wifi', 'tv', 'towels'), ('hairdryer', 'bathrobe', 'toiletries', 'heater'),
                    ('Shampoo', 'Conditioner', 'bathtub', 'bidet', 'smooking'), ('minibar', 'bottled_water', 'coffee'),
                    ('Electric_kettle', 'has_window', 'view',) ]


admin.site.register(RoomType, TypeAdmin)
admin.site.register(Availability_Room)


