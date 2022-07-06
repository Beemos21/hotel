from django.shortcuts import render
from datetime import datetime
from datetime import date
from django.db import connection
# from .serializers import AvalabilitySerializer, BranchesSerializer, RoomTypeSerializer
from rest_framework import mixins, viewsets


# Create your views here.


def getWhereAvalabilitydays(fromdate, todate, availableornot):
    fromdateasdate = datetime.strptime(fromdate, '%Y-%m-%d')
    fromdateasint = int(fromdateasdate.strftime('%j'))

    todateasdate = datetime.strptime(todate, '%Y-%m-%d')
    todateasint = int(todateasdate.strftime('%j'))

    toreturnstr = ""
    if todateasint >= fromdateasint:
        for i in range(fromdateasint, todateasint + 1):
            toreturnstr = toreturnstr + "roomManager_availability_room.d" + str(i) + "=" + str(availableornot)
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "
    else:
        intermediate_str = str(fromdateasdate.year) + str("-12-31")
        intermediatedate = datetime.strptime(intermediate_str, '%Y-%m-%d')

        intermediateasint = int(intermediatedate.strftime('%j'))

        for i in range(fromdateasint, intermediateasint + 1):
            toreturnstr = toreturnstr + "roomManager_availability_room.d" + str(i) + "=" + str(availableornot)
            # if i==intermediateasint :
            #     continue
            toreturnstr = toreturnstr + " and "

        # toreturnstr= toreturnstr + " and "

        for i in range(1, todateasint + 1):
            toreturnstr = toreturnstr + "roomManager_availability_room.d" + str(i) + "=" + availableornot
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "
    return toreturnstr


def getRoomAvailability(fromdate, todate, hotelid, nbadult, nbchildren, nbrooms, availableornot):
    sql1 = " SELECT roomManager_roomtype.id,roomManager_roomtype.capacity ,roomManager_roomtype.type_name,roomManager_roomtype.type_name_ar," \
           " roomManager_roomtype.price_per_day ,Count(roomManager_room.id) as countofroom , roomManager_roomtype.description ,roomManager_roomtype.description_ar , " \
           " roomManager_roomtype.area,roomManager_roomtype.bedType,roomManager_roomtype.bedType_ar,roomManager_roomtype.special_features,roomManager_roomtype.special_features_ar,roomManager_roomtype.cover_image,currencyapp_currency.symbole " \
           " FROM roomManager_room  " \
           " INNER JOIN roomManager_roomtype on roomManager_room.rtype_id = roomManager_roomtype.id  INNER JOIN " \
           " roomManager_availability_room on roomManager_room.id = roomManager_availability_room.room_id " \
           " INNER JOIN currencyapp_currency on  currencyapp_currency.id = roomManager_roomtype.currency_id "

    sql = str(sql1) + " where " + getWhereAvalabilitydays(fromdate, todate, availableornot)

    if int(hotelid) > 0:
        sql = str(sql) + " And roomManager_room.hotel_id= " + str(hotelid)
    capacity = int(nbadult) + int(nbchildren)
    if capacity > 0:
        sql = str(sql) + " And roomManager_roomtype.capacity>= " + str(capacity)
    sql = str(sql) + " GROUP BY roomManager_roomtype.id, roomManager_roomtype.capacity, " \
                     "roomManager_roomtype.type_name,roomManager_roomtype.type_name_ar," \
                     "roomManager_roomtype.price_per_day, roomManager_roomtype.description ," \
                     "roomManager_roomtype.description_ar ," \
                     "roomManager_roomtype.area,roomManager_roomtype.bedType,roomManager_roomtype.bedType_ar, " \
                     "roomManager_roomtype.special_features,roomManager_roomtype.special_features_ar," \
                     "roomManager_roomtype.cover_image,currencyapp_currency.symbole "

    print(sql)
    roomslist = []

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
                'cover_image': imagepath,
                'symbole': row[14],

            }

            roomslist.append(room1)
    # print(roomslist)
    return roomslist


def roomAvailabilityReportViews(request):
    availableRooms = getRoomAvailability('2022-07-06', '2022-07-07', 1, 2, 1, 0, 0)
    reservedRooms = getRoomAvailability('2022-07-06', '2022-07-07', 1, 2, 0, 0, 1)
    countA = 0
    countR = 0

    while availableRooms:
        countA += 1

    while reservedRooms:
        countR += 1

    return render(request, 'roomAvailabilityReport.html', {'countA': countA,
                                                           'countR': countR})
