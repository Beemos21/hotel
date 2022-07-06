from rest_framework import viewsets

from roomManager.models import HotelInfo, RoomType
from datetime import datetime
from datetime import date
from django.db import connection
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import views
from rest_framework.response import Response

from .serializers import AvalabilitySerializer,BranchesSerializer,RoomTypeSerializer,RoomTypeDetailSerializer
from rest_framework import mixins, viewsets

###############################################################
class GetBranchesViewSet(viewsets.ModelViewSet):
    queryset = HotelInfo.objects.all()  # mn ayy table badi jibon
    serializer_class = BranchesSerializer  # shu badu yesta3mel la ye2raya
###########################################################################

class GetAllRoomTypeView(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()  # mn ayy table badi jibon
    serializer_class = RoomTypeSerializer  # shu badu yesta3mel la ye2raya
################################################################

def getWhereAvalabilitydays( fromdate, todate):
    fromdateasdate = datetime.strptime(fromdate, '%Y-%m-%d')
    fromdateasint = int(fromdateasdate.strftime('%j'))

    todateasdate = datetime.strptime(todate, '%Y-%m-%d')
    todateasint = int(todateasdate.strftime('%j'))

    toreturnstr = ""
    if todateasint >= fromdateasint:
        for i in range(fromdateasint, todateasint + 1):
            toreturnstr = toreturnstr + "roomManager_availability_room.d" + str(i) + "='0'"
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "
    else:
        intermediate_str = str(fromdateasdate.year) + str("-12-31")
        intermediatedate = datetime.strptime(intermediate_str, '%Y-%m-%d')

        intermediateasint = int(intermediatedate.strftime('%j'))

        for i in range(fromdateasint, intermediateasint + 1):
            toreturnstr = toreturnstr + "roomManager_availability_room.d" + str(i) + "='0'"
            # if i==intermediateasint :
            #     continue
            toreturnstr = toreturnstr + " and "

        # toreturnstr= toreturnstr + " and "

        for i in range(1, todateasint + 1):
            toreturnstr = toreturnstr + "roomManager_availability_room.d" + str(i) + "='0'"
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "
    return toreturnstr

def getRoomAvailability( fromdate, todate, hotelid, nbadult, nbchildren, nbrooms):

    sql1 = " SELECT roomManager_roomtype.id,roomManager_roomtype.capacity ,roomManager_roomtype.type_name,roomManager_roomtype.type_name_ar," \
           " roomManager_roomtype.price_per_day ,Count(roomManager_room.id) as countofroom , roomManager_roomtype.description ,roomManager_roomtype.description_ar , " \
           " roomManager_roomtype.area,roomManager_roomtype.bedType,roomManager_roomtype.bedType_ar,roomManager_roomtype.special_features,roomManager_roomtype.special_features_ar,roomManager_roomtype.cover_image,currencyapp_currency.symbole " \
           " FROM roomManager_room  " \
           " INNER JOIN roomManager_roomtype on roomManager_room.rtype_id = roomManager_roomtype.id  INNER JOIN " \
           " roomManager_availability_room on roomManager_room.id = roomManager_availability_room.room_id " \
           " INNER JOIN currencyapp_currency on  currencyapp_currency.id = roomManager_roomtype.currency_id "


    sql = str(sql1) + " where " + getWhereAvalabilitydays(fromdate, todate)

    if int(hotelid) > 0:
        sql = str(sql) + " And roomManager_room.hotel_id= " + str(hotelid)
    capacity = int(nbadult) + int(nbchildren)
    if capacity > 0:
        sql = str(sql) + " And roomManager_roomtype.capacity>= " + str(capacity)
    sql = str(sql) + " GROUP BY roomManager_roomtype.id, roomManager_roomtype.capacity, " \
                         " roomManager_roomtype.type_name,roomManager_roomtype.type_name_ar,roomManager_roomtype.price_per_day, roomManager_roomtype.description ,roomManager_roomtype.description_ar ,"\
                         " roomManager_roomtype.area,roomManager_roomtype.bedType,roomManager_roomtype.bedType_ar, roomManager_roomtype.special_features,roomManager_roomtype.special_features_ar,roomManager_roomtype.cover_image,currencyapp_currency.symbole "

    print(sql)
    roomslist=[]

    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            if row[13]:
                imagepath = "media/" + str(row[13])
            else:
                imagepath = ""
            room1 = {
                'id': row[0],
                'capacity': row[1],
                'type_name': row[2],
                'type_name_ar': row[3],
                'price_per_day': row[4],
                'countofroom': row[5],
                'description': row[6],
                'description_ar': row[7],
                'area': row[8],
                'bedType': row[9],
                'bedType_ar': row[10],
                'special_features': row[11],
                'special_features_ar': row[12],
                'cover_image':imagepath,
                'symbole':row[14],



            }

            roomslist.append(room1)
    # print(roomslist)
    return roomslist

class AvalabilityView(mixins.ListModelMixin,viewsets.GenericViewSet):

    serializer_class = AvalabilitySerializer

    def get_object(self, queryset=None):
        obj = self.request

        return obj


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        getData = self.get_object()
        try:

            if getData.GET['fromdate']:
                fromdate=getData.GET['fromdate']
            else:
                fromdate = ""
        except:
            current_date = date.today()
            intermediate_str = str(current_date.year) + str("-01-01")
            fromdate = datetime.strptime(intermediate_str, '%Y-%m-%d')
        try:
            if getData.GET['todate']:
                todate = getData.GET['todate']
            else:
                todate = ""
        except:
            todate = fromdate

        try:
            if getData.GET['hotelid']:
                hotelid = getData.GET['hotelid']
            else:
                hotelid = "0"
        except:
            hotelid = "0"

        try:
            if getData.GET['nbadult']:
                nbadult = getData.GET['nbadult']
            else:
                nbadult = "0"
        except:
            nbadult = "0"

        try:
            if getData.GET['nbchildren']:
                nbchildren = getData.GET['nbchildren']
            else:
                nbchildren = "0"
        except:
            nbchildren = "0"


        try:
            if getData.GET['nbrooms']:
                nbrooms = getData.GET['nbrooms']
            else:
                nbrooms = "0"
        except:
            nbrooms = "0"



        queryset = getRoomAvailability(fromdate, todate, hotelid, nbadult, nbchildren, nbrooms)

        # queryset = getRoomAvailability(getData.GET['fromdate'], getData.GET['todate'], getData.GET['hotelid'], getData.GET['nbadult'], getData.GET['nbchildren'], getData.GET['nbrooms'])
        # queryset = getRoomAvailability("2022-01-01", "2022-01-01", "0", "0", "0", "0")

        # queryset = getRoomAvailability(one.data['fromdate'], one.data['todate'], 0, 0, 0, 0)
        return queryset
###############################################################



def getRoomTypeDetail( id):

    sql = " SELECT roomManager_roomtype.id,roomManager_roomtype.capacity ,roomManager_roomtype.type_name,roomManager_roomtype.type_name_ar," \
           " roomManager_roomtype.price_per_day , roomManager_roomtype.description ,roomManager_roomtype.description_ar , " \
           " roomManager_roomtype.area,roomManager_roomtype.bedType,roomManager_roomtype.bedType_ar,roomManager_roomtype.special_features,roomManager_roomtype.special_features_ar,roomManager_roomtype.cover_image  " \
           " FROM  roomManager_roomtype  where roomManager_roomtype.id =" + str(id)


    roomslist = []
    roomslistimage = []
    roomslistservices = []
    row = []

    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
        if row[12]:
            imagepath = "media/" + str(row[12])
        else:
            imagepath = ""

    sqlimages = " SELECT roomManager_roomtypedisplayimages.display_images FROM  roomManager_roomtypedisplayimages  where roomManager_roomtypedisplayimages.roomtype_id =" + str(id)


    with connection.cursor() as cursor:
        cursor.execute(sqlimages)
        rows = cursor.fetchall()

        for rowim in rows:
            if rowim[0]:
                imagepath = "media/" + str(rowim[0])
            else:
                imagepath = ""
            roomimage = {
                'images': imagepath
            }

            roomslistimage.append(roomimage)

    sqlservices = " SELECT roomManager_service.name,roomManager_service.name_ar,roomManager_roomservice.available,roomManager_roomservice.free " \
                  " FROM roomManager_service INNER JOIN roomManager_roomservice ON roomManager_service.id = roomManager_roomservice.service_id " \
                  " where roomManager_roomservice.roomtype_id =  " + str(id)
    with connection.cursor() as cursor:
        cursor.execute(sqlservices)
        rows = cursor.fetchall()

        for rowservices in rows:

            roomservices = {
                'services': rowservices[0],
                'services_ar': rowservices[1],
                'available': rowservices[2],
                'free': rowservices[3]
            }

            roomslistservices.append(roomservices)

    room1 = {
        'id': row[0],
        'capacity': row[1],
        'type_name': row[2],
        'type_name_ar': row[3],
        'price_per_day': row[4],
        'description': row[5],
        'description_ar': row[6],
        'area': row[7],
        'bedType': row[8],
        'bedType_ar': row[9],
        'special_features': row[10],
        'special_features_ar': row[11],
        'cover_image':imagepath,
        'images':roomslistimage,
        'services': roomslistservices

        }


    roomslist.append(room1)
    print(roomslist)
    return roomslist

class GetRoomTypeDetailView(mixins.ListModelMixin,viewsets.GenericViewSet):

    serializer_class = RoomTypeDetailSerializer

    def get_object(self, queryset=None):
        obj = self.request

        return obj


    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """

        getData = self.get_object()
        id = getData.GET['id']

        queryset = getRoomTypeDetail(id)


        return queryset



