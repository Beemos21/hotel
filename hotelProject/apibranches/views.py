from rest_framework import viewsets
from .serializers import BranchesSerializer, AvailableRoomsSerializer
from roomManager.models import HotelInfo, RoomType
from datetime import datetime
from django.db import connection

from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication


# Create your views here.


class GetBranchesViewSet(viewsets.ModelViewSet):
    queryset = HotelInfo.objects.all()  # mn ayy table badi jibon
    serializer_class = BranchesSerializer  # shu badu yesta3mel la ye2raya


def getWhereAvalabilitydays(self, request, *args, **kwargs):
    self.object = self.get_object()
    serializer = self.get_serializer(data=request.data)

    fromdateasdate = datetime.strptime(serializer.data.get("fromdate"), '%Y-%m-%d')
    fromdateasint = int(fromdateasdate.strftime('%j'))

    todateasdate = datetime.strptime(serializer.data.get("todate"), '%Y-%m-%d')
    todateasint = int(todateasdate.strftime('%j'))

    toreturnstr = ""
    if todateasint >= fromdateasint:
        for i in range(fromdateasint, todateasint + 1):
            toreturnstr = toreturnstr + "d" + str(i) + "=0"
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "
    else:
        intermediate_str = str(fromdateasdate.year) + str("-12-31")
        intermediatedate = datetime.strptime(intermediate_str, '%Y-%m-%d')

        intermediateasint = int(intermediatedate.strftime('%j'))

        for i in range(fromdateasint, intermediateasint + 1):
            toreturnstr = toreturnstr + "d" + str(i) + "=0"
            toreturnstr = toreturnstr + " and "

        for i in range(1, todateasint + 1):
            toreturnstr = toreturnstr + "d" + str(i) + "=0"
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "
    return toreturnstr


def getRoomAvailability(self, request, *args, **kwargs):
    self.object = self.get_object()
    serializer = self.get_serializer(data=request.data)
    sql1 = "SELECT roomManager_roomtype.id,roomManager_roomtype.capacity ,roomManager_roomtype.type_name," \
           "roomManager_roomtype.price_per_day , Count(roomManager_room.id) as countofroom FROM roomManager_room " \
           "INNER JOIN roomManager_roomtype on roomManager_room.rtype_id = roomManager_roomtype.id  INNER JOIN " \
           "roomManager_availability_room on roomManager_room.id = roomManager_availability_room.room_id "
    sql = str(sql1) + " where " + self.getWhereAvalabilitydays(serializer.data.get("fromdate"),
                                                               serializer.data.get("todate"))
    if int(serializer.data.get("hotelid")) > 0:
        sql = str(sql) + " And roomManager_room.hotelid= " + str(serializer.data.get("hotelid"))
    capacity = int(serializer.data.get("nbadult")) + int(serializer.data.get("nbchildren"))
    if capacity > 0:
        # sql = str(sql) + " And roomManager_roomtype.capacity>= " + str(capacity)
        sql = str(sql) + "GROUP BY roomManager_roomtype.id, roomManager_roomtype.capacity, " \
                         "roomManager_roomtype.type_name,roomManager_roomtype.price_per_day "

    roomslist = []
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            room1 = {
                'id': row[0],
                'capacity': row[1],
                'type_name': row[2],
                'roomtype': row[3],
                'price_per_day': row[4],
                'countofroom': row[5],

            }
            roomslist.append(room1)
        print(roomslist)
    return roomslist


class GetRoomAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()  # mn ayy table badi jibon
    serializer_class = AvailableRoomsSerializer  # shu badu yesta3mel la ye2raya
    model = RoomType

    def get_object(self, queryset=None):
        obj = self.request
        return obj

    # def get_queryset(self):
    #     self.request.RoomType
