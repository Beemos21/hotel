import datetime
from django.db import models
from djmoney.models.fields import MoneyField
from django.contrib.auth.models import User
from django.contrib import admin
from currencyapp.models import Currency
TYPE = (
    ('A', 'Air Conditioned'),
    ('NA', 'Non Air Conditioned')
)


def room_images_upload_path(instance, file_name):
    return f"room-cover/{file_name}"


def room_display_images_upload_path(instance, file_name):
    return f"room-display/{file_name}"





class City(models.Model):
    city_name = models.CharField(max_length=20)
    city_name_ar = models.CharField(max_length=20)

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.city_name


class HotelInfo(models.Model):
    name = models.CharField(max_length=255)
    name_ar = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    reg_number = models.CharField(max_length=10)
    owner_name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=400)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True)
    state = models.CharField(max_length=25, null=True)
    phone = models.CharField(max_length=20)
    user = models.ManyToManyField(User, related_name='users', through='HotelUser')
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.name


class HotelUser(models.Model):
    hotel = models.ForeignKey(HotelInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_default = models.BooleanField()

    # created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    # updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.hotel.name


class HotelUser_Inline(admin.TabularInline):
    model = HotelUser
    extra = 1


class Room(models.Model):
    title = models.CharField(max_length=30)
    rtype = models.ForeignKey('RoomType', on_delete=models.CASCADE, null=True)
    rfloor = models.IntegerField(default=1, null=True)
    cover_image = models.ImageField(upload_to=room_images_upload_path)
    is_active = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    room_status = models.ForeignKey('RoomStatus', on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey('HotelInfo', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=50)
    name_ar = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    currency = models.ForeignKey(Currency,  on_delete=models.CASCADE,blank=True,
        null=True)
    description = models.TextField(max_length=250)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.name


class RoomType(models.Model):
    room_type = (('Single room', 'Single room'), ('Twin room', 'Twin room'), ('Double room', 'Double room'),
                 ('Triple room', 'Triple room'), ('Quad room', 'Quad room'),
                 ('Double-Double room', 'Double-Double room'),
                 ('Queen room', 'Queen room'),  ('King room', 'Suite'), ('King room', 'Suite'),
                 ('Presidential suite', 'Presidential suite'), ('Studio', 'Studio'),
                 ('Connecting rooms', 'Connecting rooms'), ('Junior Suite', 'Junior Suite'))
    type_name = models.CharField(max_length=20, choices=room_type, default='Twin room')
    room_type_ar = (('غرفه مفرده', 'غرفه مفرده'), ('غرفة توأم', 'غرفة توأم'), ('غرفة مزدوجة ', 'غرفة مزدوجة '),
                 ('غرفه ثلاثيه', 'غرفه ثلاثيه'), ('غرفه رباعيه', 'غرفه رباعيه'),
                 ('مزدوج مزدوجة ثنائية', 'مزدوج مزدوجة ثنائية'),
                 ('غرفة الملكة', 'غرفة الملكة'), ('غرفة الملك', 'غرفة الملك'), ('جناح', 'جناح'),
                 ('جناح الرئيس | الجناح الرئاسي', 'جناح الرئيس | الجناح الرئاسي'),
                    ('الاستوديو', 'الاستوديو'),
                 ('الغرف المتصلة', 'الغرف المتصلة'),('جناح صغير' ,'جناح صغير'))
    type_name_ar = models.CharField(max_length=30, choices=room_type_ar, default='Twin room')
    area = models.IntegerField(default=10)
    Bed_ = (('1 double bed', '1 double bed'),
            ('1 double bed and 1 Sofa', '1 double bed and 1 Sofa'),
            ('2 single beds', '2 single beds'),
            ('1 Sofa and 1 single bed', '1 Single Sofa Bed and 1 single bed'),
            ('king Bed', 'king Bed')
            )
    bedType = models.CharField(max_length=23, choices=Bed_, default='1 double bed')
    Bed_ar = (('سرير لفردين', 'سرير لفردين'),
            ('1 سرير لفردين و 1 سرير أريكة', '1 سرير لفردين 1 سرير أريكة'),
            ('2 سرير لفرد واحد', '2 سرير لفرد واحد'),
            ('1 سرير أريكة 1 سرير لفرد واحد', '1 سرير أريكة 1 سرير لفرد واحد'),
            (' سرير كبير لفردين','سرير كبير لفردين'))

    bedType_ar = models.CharField(max_length=30, choices=Bed_ar, default='سرير لفردين ')
    capacity = models.IntegerField(default=2)
    cover_image = models.ImageField(upload_to=room_images_upload_path)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=3)
    currency = models.ForeignKey(Currency,on_delete= models.PROTECT, default=None ,blank=True,
        null=True)
    description = models.CharField(max_length=50)
    special_features = models.CharField(max_length=50)
    description_ar = models.CharField(max_length=50)
    special_features_ar = models.CharField(max_length=50)
    services = models.ManyToManyField(Service, related_name='sevices', through='RoomService')
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.type_name


class RoomService(models.Model):
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    available = models.BooleanField()
    free = models.BooleanField()

    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)


class RoomService_Inline(admin.TabularInline):
    model = RoomService
    extra = 1


class RoomStatus(models.Model):
    roomstatus = models.CharField(max_length=30)
    description = models.CharField(max_length=30)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        verbose_name_plural = "Room Status"

    def __str__(self):
        return self.roomstatus


class RoomDisplayImages(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    display_images = models.ImageField(upload_to=room_display_images_upload_path)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.room.title


class RoomTypeDisplayImages(models.Model):
    roomtype = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    display_images = models.ImageField(upload_to=room_display_images_upload_path)
    created_at = models.DateTimeField(default=datetime.datetime.now, blank=True)
    updated_at = models.DateTimeField(default=datetime.datetime.now, blank=True)

    def __str__(self):
        return self.roomtype.type_name


class Availability_Room(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE)
    d1 = models.CharField(max_length=2, default="0")
    d2 = models.CharField(max_length=2, default="0")
    d3 = models.CharField(max_length=2, default="0")
    d4 = models.CharField(max_length=2, default="0")
    d5 = models.CharField(max_length=2, default="0")
    d6 = models.CharField(max_length=2, default="0")
    d7 = models.CharField(max_length=2, default="0")
    d8 = models.CharField(max_length=2, default="0")
    d9 = models.CharField(max_length=2, default="0")
    d10 = models.CharField(max_length=2, default="0")
    d11 = models.CharField(max_length=2, default="0")
    d12 = models.CharField(max_length=2, default="0")
    d13 = models.CharField(max_length=2, default="0")
    d14 = models.CharField(max_length=2, default="0")
    d15 = models.CharField(max_length=2, default="0")
    d16 = models.CharField(max_length=2, default="0")
    d17 = models.CharField(max_length=2, default="0")
    d18 = models.CharField(max_length=2, default="0")
    d19 = models.CharField(max_length=2, default="0")
    d20 = models.CharField(max_length=2, default="0")
    d21 = models.CharField(max_length=2, default="0")
    d22 = models.CharField(max_length=2, default="0")
    d23 = models.CharField(max_length=2, default="0")
    d24 = models.CharField(max_length=2, default="0")
    d25 = models.CharField(max_length=2, default="0")
    d26 = models.CharField(max_length=2, default="0")
    d27 = models.CharField(max_length=2, default="0")
    d28 = models.CharField(max_length=2, default="0")
    d29 = models.CharField(max_length=2, default="0")
    d30 = models.CharField(max_length=2, default="0")
    d31 = models.CharField(max_length=2, default="0")
    d32 = models.CharField(max_length=2, default="0")
    d33 = models.CharField(max_length=2, default="0")
    d34 = models.CharField(max_length=2, default="0")
    d35 = models.CharField(max_length=2, default="0")
    d36 = models.CharField(max_length=2, default="0")
    d37 = models.CharField(max_length=2, default="0")
    d38 = models.CharField(max_length=2, default="0")
    d39 = models.CharField(max_length=2, default="0")
    d40 = models.CharField(max_length=2, default="0")
    d41 = models.CharField(max_length=2, default="0")
    d42 = models.CharField(max_length=2, default="0")
    d43 = models.CharField(max_length=2, default="0")
    d44 = models.CharField(max_length=2, default="0")
    d45 = models.CharField(max_length=2, default="0")
    d46 = models.CharField(max_length=2, default="0")
    d47 = models.CharField(max_length=2, default="0")
    d48 = models.CharField(max_length=2, default="0")
    d49 = models.CharField(max_length=2, default="0")
    d50 = models.CharField(max_length=2, default="0")
    d51 = models.CharField(max_length=2, default="0")
    d52 = models.CharField(max_length=2, default="0")
    d53 = models.CharField(max_length=2, default="0")
    d54 = models.CharField(max_length=2, default="0")
    d55 = models.CharField(max_length=2, default="0")
    d56 = models.CharField(max_length=2, default="0")
    d57 = models.CharField(max_length=2, default="0")
    d58 = models.CharField(max_length=2, default="0")
    d59 = models.CharField(max_length=2, default="0")
    d60 = models.CharField(max_length=2, default="0")
    d61 = models.CharField(max_length=2, default="0")
    d62 = models.CharField(max_length=2, default="0")
    d63 = models.CharField(max_length=2, default="0")
    d64 = models.CharField(max_length=2, default="0")
    d65 = models.CharField(max_length=2, default="0")
    d66 = models.CharField(max_length=2, default="0")
    d67 = models.CharField(max_length=2, default="0")
    d68 = models.CharField(max_length=2, default="0")
    d69 = models.CharField(max_length=2, default="0")
    d70 = models.CharField(max_length=2, default="0")
    d71 = models.CharField(max_length=2, default="0")
    d72 = models.CharField(max_length=2, default="0")
    d73 = models.CharField(max_length=2, default="0")
    d74 = models.CharField(max_length=2, default="0")
    d75 = models.CharField(max_length=2, default="0")
    d76 = models.CharField(max_length=2, default="0")
    d77 = models.CharField(max_length=2, default="0")
    d78 = models.CharField(max_length=2, default="0")
    d79 = models.CharField(max_length=2, default="0")
    d80 = models.CharField(max_length=2, default="0")
    d81 = models.CharField(max_length=2, default="0")
    d82 = models.CharField(max_length=2, default="0")
    d83 = models.CharField(max_length=2, default="0")
    d84 = models.CharField(max_length=2, default="0")
    d85 = models.CharField(max_length=2, default="0")
    d86 = models.CharField(max_length=2, default="0")
    d87 = models.CharField(max_length=2, default="0")
    d88 = models.CharField(max_length=2, default="0")
    d89 = models.CharField(max_length=2, default="0")
    d90 = models.CharField(max_length=2, default="0")
    d91 = models.CharField(max_length=2, default="0")
    d92 = models.CharField(max_length=2, default="0")
    d93 = models.CharField(max_length=2, default="0")
    d94 = models.CharField(max_length=2, default="0")
    d95 = models.CharField(max_length=2, default="0")
    d96 = models.CharField(max_length=2, default="0")
    d97 = models.CharField(max_length=2, default="0")
    d98 = models.CharField(max_length=2, default="0")
    d99 = models.CharField(max_length=2, default="0")
    d100 = models.CharField(max_length=2, default="0")
    d101 = models.CharField(max_length=2, default="0")
    d102 = models.CharField(max_length=2, default="0")
    d103 = models.CharField(max_length=2, default="0")
    d104 = models.CharField(max_length=2, default="0")
    d105 = models.CharField(max_length=2, default="0")
    d106 = models.CharField(max_length=2, default="0")
    d107 = models.CharField(max_length=2, default="0")
    d108 = models.CharField(max_length=2, default="0")
    d109 = models.CharField(max_length=2, default="0")
    d110 = models.CharField(max_length=2, default="0")
    d111 = models.CharField(max_length=2, default="0")
    d112 = models.CharField(max_length=2, default="0")
    d113 = models.CharField(max_length=2, default="0")
    d114 = models.CharField(max_length=2, default="0")
    d115 = models.CharField(max_length=2, default="0")
    d116 = models.CharField(max_length=2, default="0")
    d117 = models.CharField(max_length=2, default="0")
    d118 = models.CharField(max_length=2, default="0")
    d119 = models.CharField(max_length=2, default="0")
    d120 = models.CharField(max_length=2, default="0")
    d121 = models.CharField(max_length=2, default="0")
    d122 = models.CharField(max_length=2, default="0")
    d123 = models.CharField(max_length=2, default="0")
    d124 = models.CharField(max_length=2, default="0")
    d125 = models.CharField(max_length=2, default="0")
    d126 = models.CharField(max_length=2, default="0")
    d127 = models.CharField(max_length=2, default="0")
    d128 = models.CharField(max_length=2, default="0")
    d129 = models.CharField(max_length=2, default="0")
    d130 = models.CharField(max_length=2, default="0")
    d131 = models.CharField(max_length=2, default="0")
    d132 = models.CharField(max_length=2, default="0")
    d133 = models.CharField(max_length=2, default="0")
    d134 = models.CharField(max_length=2, default="0")
    d135 = models.CharField(max_length=2, default="0")
    d136 = models.CharField(max_length=2, default="0")
    d137 = models.CharField(max_length=2, default="0")
    d138 = models.CharField(max_length=2, default="0")
    d139 = models.CharField(max_length=2, default="0")
    d140 = models.CharField(max_length=2, default="0")
    d141 = models.CharField(max_length=2, default="0")
    d142 = models.CharField(max_length=2, default="0")
    d143 = models.CharField(max_length=2, default="0")
    d144 = models.CharField(max_length=2, default="0")
    d145 = models.CharField(max_length=2, default="0")
    d146 = models.CharField(max_length=2, default="0")
    d147 = models.CharField(max_length=2, default="0")
    d148 = models.CharField(max_length=2, default="0")
    d149 = models.CharField(max_length=2, default="0")
    d150 = models.CharField(max_length=2, default="0")
    d151 = models.CharField(max_length=2, default="0")
    d152 = models.CharField(max_length=2, default="0")
    d153 = models.CharField(max_length=2, default="0")
    d154 = models.CharField(max_length=2, default="0")
    d155 = models.CharField(max_length=2, default="0")
    d156 = models.CharField(max_length=2, default="0")
    d157 = models.CharField(max_length=2, default="0")
    d158 = models.CharField(max_length=2, default="0")
    d159 = models.CharField(max_length=2, default="0")
    d160 = models.CharField(max_length=2, default="0")
    d161 = models.CharField(max_length=2, default="0")
    d162 = models.CharField(max_length=2, default="0")
    d163 = models.CharField(max_length=2, default="0")
    d164 = models.CharField(max_length=2, default="0")
    d165 = models.CharField(max_length=2, default="0")
    d166 = models.CharField(max_length=2, default="0")
    d167 = models.CharField(max_length=2, default="0")
    d168 = models.CharField(max_length=2, default="0")
    d169 = models.CharField(max_length=2, default="0")
    d170 = models.CharField(max_length=2, default="0")
    d171 = models.CharField(max_length=2, default="0")
    d172 = models.CharField(max_length=2, default="0")
    d173 = models.CharField(max_length=2, default="0")
    d174 = models.CharField(max_length=2, default="0")
    d175 = models.CharField(max_length=2, default="0")
    d176 = models.CharField(max_length=2, default="0")
    d177 = models.CharField(max_length=2, default="0")
    d178 = models.CharField(max_length=2, default="0")
    d179 = models.CharField(max_length=2, default="0")
    d180 = models.CharField(max_length=2, default="0")
    d181 = models.CharField(max_length=2, default="0")
    d182 = models.CharField(max_length=2, default="0")
    d183 = models.CharField(max_length=2, default="0")
    d184 = models.CharField(max_length=2, default="0")
    d185 = models.CharField(max_length=2, default="0")
    d186 = models.CharField(max_length=2, default="0")
    d187 = models.CharField(max_length=2, default="0")
    d188 = models.CharField(max_length=2, default="0")
    d189 = models.CharField(max_length=2, default="0")
    d190 = models.CharField(max_length=2, default="0")
    d191 = models.CharField(max_length=2, default="0")
    d192 = models.CharField(max_length=2, default="0")
    d193 = models.CharField(max_length=2, default="0")
    d194 = models.CharField(max_length=2, default="0")
    d195 = models.CharField(max_length=2, default="0")
    d196 = models.CharField(max_length=2, default="0")
    d197 = models.CharField(max_length=2, default="0")
    d198 = models.CharField(max_length=2, default="0")
    d199 = models.CharField(max_length=2, default="0")
    d200 = models.CharField(max_length=2, default="0")
    d201 = models.CharField(max_length=2, default="0")
    d202 = models.CharField(max_length=2, default="0")
    d203 = models.CharField(max_length=2, default="0")
    d204 = models.CharField(max_length=2, default="0")
    d205 = models.CharField(max_length=2, default="0")
    d206 = models.CharField(max_length=2, default="0")
    d207 = models.CharField(max_length=2, default="0")
    d208 = models.CharField(max_length=2, default="0")
    d209 = models.CharField(max_length=2, default="0")
    d210 = models.CharField(max_length=2, default="0")
    d211 = models.CharField(max_length=2, default="0")
    d212 = models.CharField(max_length=2, default="0")
    d213 = models.CharField(max_length=2, default="0")
    d214 = models.CharField(max_length=2, default="0")
    d215 = models.CharField(max_length=2, default="0")
    d216 = models.CharField(max_length=2, default="0")
    d217 = models.CharField(max_length=2, default="0")
    d218 = models.CharField(max_length=2, default="0")
    d219 = models.CharField(max_length=2, default="0")
    d220 = models.CharField(max_length=2, default="0")
    d221 = models.CharField(max_length=2, default="0")
    d222 = models.CharField(max_length=2, default="0")
    d223 = models.CharField(max_length=2, default="0")
    d224 = models.CharField(max_length=2, default="0")
    d225 = models.CharField(max_length=2, default="0")
    d226 = models.CharField(max_length=2, default="0")
    d227 = models.CharField(max_length=2, default="0")
    d228 = models.CharField(max_length=2, default="0")
    d229 = models.CharField(max_length=2, default="0")
    d230 = models.CharField(max_length=2, default="0")
    d231 = models.CharField(max_length=2, default="0")
    d232 = models.CharField(max_length=2, default="0")
    d233 = models.CharField(max_length=2, default="0")
    d234 = models.CharField(max_length=2, default="0")
    d235 = models.CharField(max_length=2, default="0")
    d236 = models.CharField(max_length=2, default="0")
    d237 = models.CharField(max_length=2, default="0")
    d238 = models.CharField(max_length=2, default="0")
    d239 = models.CharField(max_length=2, default="0")
    d240 = models.CharField(max_length=2, default="0")
    d241 = models.CharField(max_length=2, default="0")
    d242 = models.CharField(max_length=2, default="0")
    d243 = models.CharField(max_length=2, default="0")
    d244 = models.CharField(max_length=2, default="0")
    d245 = models.CharField(max_length=2, default="0")
    d246 = models.CharField(max_length=2, default="0")
    d247 = models.CharField(max_length=2, default="0")
    d248 = models.CharField(max_length=2, default="0")
    d249 = models.CharField(max_length=2, default="0")
    d250 = models.CharField(max_length=2, default="0")
    d251 = models.CharField(max_length=2, default="0")
    d252 = models.CharField(max_length=2, default="0")
    d253 = models.CharField(max_length=2, default="0")
    d254 = models.CharField(max_length=2, default="0")
    d255 = models.CharField(max_length=2, default="0")
    d256 = models.CharField(max_length=2, default="0")
    d257 = models.CharField(max_length=2, default="0")
    d258 = models.CharField(max_length=2, default="0")
    d259 = models.CharField(max_length=2, default="0")
    d260 = models.CharField(max_length=2, default="0")
    d261 = models.CharField(max_length=2, default="0")
    d262 = models.CharField(max_length=2, default="0")
    d263 = models.CharField(max_length=2, default="0")
    d264 = models.CharField(max_length=2, default="0")
    d265 = models.CharField(max_length=2, default="0")
    d266 = models.CharField(max_length=2, default="0")
    d267 = models.CharField(max_length=2, default="0")
    d268 = models.CharField(max_length=2, default="0")
    d269 = models.CharField(max_length=2, default="0")
    d270 = models.CharField(max_length=2, default="0")
    d271 = models.CharField(max_length=2, default="0")
    d272 = models.CharField(max_length=2, default="0")
    d273 = models.CharField(max_length=2, default="0")
    d274 = models.CharField(max_length=2, default="0")
    d275 = models.CharField(max_length=2, default="0")
    d276 = models.CharField(max_length=2, default="0")
    d277 = models.CharField(max_length=2, default="0")
    d278 = models.CharField(max_length=2, default="0")
    d279 = models.CharField(max_length=2, default="0")
    d280 = models.CharField(max_length=2, default="0")
    d281 = models.CharField(max_length=2, default="0")
    d282 = models.CharField(max_length=2, default="0")
    d283 = models.CharField(max_length=2, default="0")
    d284 = models.CharField(max_length=2, default="0")
    d285 = models.CharField(max_length=2, default="0")
    d286 = models.CharField(max_length=2, default="0")
    d287 = models.CharField(max_length=2, default="0")
    d288 = models.CharField(max_length=2, default="0")
    d289 = models.CharField(max_length=2, default="0")
    d290 = models.CharField(max_length=2, default="0")
    d291 = models.CharField(max_length=2, default="0")
    d292 = models.CharField(max_length=2, default="0")
    d293 = models.CharField(max_length=2, default="0")
    d294 = models.CharField(max_length=2, default="0")
    d295 = models.CharField(max_length=2, default="0")
    d296 = models.CharField(max_length=2, default="0")
    d297 = models.CharField(max_length=2, default="0")
    d298 = models.CharField(max_length=2, default="0")
    d299 = models.CharField(max_length=2, default="0")
    d300 = models.CharField(max_length=2, default="0")
    d301 = models.CharField(max_length=2, default="0")
    d302 = models.CharField(max_length=2, default="0")
    d303 = models.CharField(max_length=2, default="0")
    d304 = models.CharField(max_length=2, default="0")
    d305 = models.CharField(max_length=2, default="0")
    d306 = models.CharField(max_length=2, default="0")
    d307 = models.CharField(max_length=2, default="0")
    d308 = models.CharField(max_length=2, default="0")
    d309 = models.CharField(max_length=2, default="0")
    d310 = models.CharField(max_length=2, default="0")
    d311 = models.CharField(max_length=2, default="0")
    d312 = models.CharField(max_length=2, default="0")
    d313 = models.CharField(max_length=2, default="0")
    d314 = models.CharField(max_length=2, default="0")
    d315 = models.CharField(max_length=2, default="0")
    d316 = models.CharField(max_length=2, default="0")
    d317 = models.CharField(max_length=2, default="0")
    d318 = models.CharField(max_length=2, default="0")
    d319 = models.CharField(max_length=2, default="0")
    d320 = models.CharField(max_length=2, default="0")
    d321 = models.CharField(max_length=2, default="0")
    d322 = models.CharField(max_length=2, default="0")
    d323 = models.CharField(max_length=2, default="0")
    d324 = models.CharField(max_length=2, default="0")
    d325 = models.CharField(max_length=2, default="0")
    d326 = models.CharField(max_length=2, default="0")
    d327 = models.CharField(max_length=2, default="0")
    d328 = models.CharField(max_length=2, default="0")
    d329 = models.CharField(max_length=2, default="0")
    d330 = models.CharField(max_length=2, default="0")
    d331 = models.CharField(max_length=2, default="0")
    d332 = models.CharField(max_length=2, default="0")
    d333 = models.CharField(max_length=2, default="0")
    d334 = models.CharField(max_length=2, default="0")
    d335 = models.CharField(max_length=2, default="0")
    d336 = models.CharField(max_length=2, default="0")
    d337 = models.CharField(max_length=2, default="0")
    d338 = models.CharField(max_length=2, default="0")
    d339 = models.CharField(max_length=2, default="0")
    d340 = models.CharField(max_length=2, default="0")
    d341 = models.CharField(max_length=2, default="0")
    d342 = models.CharField(max_length=2, default="0")
    d343 = models.CharField(max_length=2, default="0")
    d344 = models.CharField(max_length=2, default="0")
    d345 = models.CharField(max_length=2, default="0")
    d346 = models.CharField(max_length=2, default="0")
    d347 = models.CharField(max_length=2, default="0")
    d348 = models.CharField(max_length=2, default="0")
    d349 = models.CharField(max_length=2, default="0")
    d350 = models.CharField(max_length=2, default="0")
    d351 = models.CharField(max_length=2, default="0")
    d352 = models.CharField(max_length=2, default="0")
    d353 = models.CharField(max_length=2, default="0")
    d354 = models.CharField(max_length=2, default="0")
    d355 = models.CharField(max_length=2, default="0")
    d356 = models.CharField(max_length=2, default="0")
    d357 = models.CharField(max_length=2, default="0")
    d358 = models.CharField(max_length=2, default="0")
    d359 = models.CharField(max_length=2, default="0")
    d360 = models.CharField(max_length=2, default="0")
    d361 = models.CharField(max_length=2, default="0")
    d362 = models.CharField(max_length=2, default="0")
    d363 = models.CharField(max_length=2, default="0")
    d364 = models.CharField(max_length=2, default="0")
    d365 = models.CharField(max_length=2, default="0")
    d366 = models.CharField(max_length=2, default="0")
