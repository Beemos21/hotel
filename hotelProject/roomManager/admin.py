from django.conf import settings
from django.contrib import admin
from .models import *


class RoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'rtype', 'rfloor', 'is_active', 'cover_image', 'featured',
                    'room_status', 'hotel']
    fields = [('title', 'rtype'), 'rfloor', ('featured', 'is_active'),
              ('room_status', 'hotel')]
    actions = ['set_room_to_book', ]

    def set_room_to_book(self, request, queryset):
        count = queryset.update(is_booked=False)
        self.message_user(request, '{} room change successfully.'.format(count))
    set_room_to_book.short_description = 'Mark selected Room to free'


admin.site.register(Room, RoomAdmin)


class HotelAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'reg_number', 'owner_name', 'address', 'city', 'state', 'phone']
    inlines = (HotelUser_Inline,)


admin.site.register(HotelInfo, HotelAdmin)
#

# admin.site.site_header = str(settings.STATIC_ROOT)  # 'Hotel Management System'
# admin.site.site_title = 'DAS-360 HMS '
# admin.site.index_title = 'Admin Panel- Das 360'


admin.site.register(RoomStatus)


admin.site.register(RoomService)


class CityAdmin(admin.ModelAdmin):
    list_display = ['city_name', ]


admin.site.register(City, CityAdmin)


class TypeAdmin(admin.ModelAdmin):
    list_display = ['type_name', 'type_name_ar', 'area', 'bedType','bedType_ar', 'capacity',
                    'price_per_day', 'description', 'special_features','cover_image','currency']
    fields = [('type_name', 'type_name_ar'), ('area', 'bedType', 'bedType_ar'),
              ('capacity', 'price_per_day', 'description'), 'special_features','cover_image','currency']
    inlines = (RoomService_Inline,)


class HotelUserAdmin(admin.ModelAdmin):
    list_display = ['user', 'hotel', 'is_default']


admin.site.register(RoomType, TypeAdmin)
admin.site.register(Availability_Room)
admin.site.register(HotelUser, HotelUserAdmin)
admin.site.register(Service)
admin.site.register(RoomDisplayImages)
admin.site.register(RoomTypeDisplayImages)

admin.site.register(Currency )




