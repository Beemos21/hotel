import os
from django.conf import settings
from django.core.mail import send_mail
from reportlab.lib.pagesizes import letter

import arabic_reshaper
from bidi.algorithm import get_display
from .models import Reservation

from roomManager.models import *
from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from django.core import serializers
from django.http import HttpResponse
from datetime import datetime
from django.db import connection
from datetime import date


from wkhtmltopdf.views import PDFTemplateView


def customers(request):

    # data = json.loads(request.body)
    cities = Reservation.objects.all()

    qs_json = serializers.serialize('json', cities)
    return JsonResponse(qs_json, safe=False)



class MyPDF(PDFTemplateView):
    def get_context_data(self, **kwargs):
        context = super(MyPDF, self).get_context_data(**kwargs)
        booking = Reservation.objects.all()
        # template_path = 'pdfReport.html'

        context = {
            'datatoshow': booking,
            'hostname': settings.HOSTNAME,

        }
        return context


def newbooking(request):
    booking = Reservation.objects.all()

    # if request.method == "POST":
    #     city = int(request.POST['city'])
    #     roomtype = int(request.POST['roomtype'])
    #     checkin = request.POST['checkin']
    #     checkout = request.POST['checkout']
    #
    #
    #     # return redirect('search_booking', city=city,roomtype=roomtype,checkin=checkin,checkout=checkout)
    #
    #     parametre = {
    #         'city': city,
    #         'roomtype': roomtype,
    #         'checkin': checkin,
    #         'checkout': checkout,
    #     }
    #
    #     return render(request, "search_booking.html", {'parametre': parametre})
    print(booking[0])
    returnvalue={
        'booking': booking,
        'type': booking[0],
    }
    return render(request,"new_booking.html",returnvalue)

def searchbooking(request,city,roomtype,checkin,checkout):

    parametre ={
        'city': city,
        'roomtype': roomtype,
        'checkin': checkin,
        'checkout': checkout,
    }
    return render(request,"search_booking.html",parametre)


def searchforroom(request):
    roomslist=[]
    rooms={}
    groomtype = RoomType.objects.all()


    rooms = {
        'rooms': roomslist,
        'groomtype': groomtype
    }

    # send_mail(
    #     'This is the subject of my mail hello everybody',
    #     'This is the test message body from django product management website',
    #     'ts2tpwindows@gmail.com',
    #     ['wassimakel@gmail.com'],
    #     fail_silently=False
    # )
    if 'form3' in request.POST:
        print('form3')

        print(request.POST)
        roomid = request.POST['roomid']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        nbadult = request.POST['nbadult']
        nbchildren = request.POST['nbchildren']
        BOOKING_type = request.POST['BOOKING_type']
        BOOKING_STATUS = request.POST['BOOKING_STATUS']




        roomdata = {
            'roomid': roomid,
            'checkin': checkin,
            'checkout': checkout,

        }


        return render(request, "book_room/success.html", roomdata)
    elif 'form2' in request.POST:

        roomid = request.POST['roomid']
        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        nbadult = request.POST['nbadult']
        nbchildren = request.POST['nbchildren']
        BOOKING_type = (('B', 'Booking'),
                        ('R', 'Reception'),
                        ('T', 'Telephone'),
                        ('E', 'Email'))
        BOOKING_STATUS = (('A', 'Available'),
                          ('B', 'Booked'),
                          ('C1', 'Cancelled by user'),
                          ('C2', 'Cancelled by Manager')
                          )
        roomtitle = Room.objects.filter(id=roomid).all().values()

        roomtype_id = roomtitle[0]['rtype_id']
        roomtype = RoomType.objects.filter(id=roomtype_id).all().values()

        checkindate = datetime.strptime(checkin, '%Y-%m-%d')
        checkoutdate = datetime.strptime(checkout, '%Y-%m-%d')

        delta = checkoutdate - checkindate
        print('delta')
        print(delta)
        nbdays=delta.days
        print(nbdays)
        roomdata = {
            'roomid': roomid,
            'title': roomtitle[0]['title'],
            'checkin': checkin,
            'checkout': checkout,
            'total_cost':roomtype[0]['price_per_day']*nbdays

        }
        print(roomdata)
        return render(request, "book_room/reserveroom.html", roomdata)

    elif request.method == "POST":
        # if request.POST['city'] != '':
        #     city = int(request.POST['city'])
        # else:
        #     city = 0

        if request.POST['roomtype'] != '':
            roomtype = int(request.POST['roomtype'])
        else:
            roomtype = 0


        checkin = request.POST['checkin']
        checkout = request.POST['checkout']
        nbadult = request.POST['nbadult']
        nbchildren = request.POST['nbchildren']


        getroom = list(Room.objects.all().filter(id=1).all().values())
        roomtype = list(RoomType.objects.all().filter(id=getroom[0]['rtype_id']).all().values())

        # room1 = {
        #     'id': getroom[0]['id'] ,
        #     'title': getroom[0]['title'],
        #     'roomtype': roomtype[0]['type_name'],
        #     'price_per_day':roomtype[0]['price_per_day'],
        #     'checkin': checkin,
        #     'checkout': checkout,
        #     'nbadult': nbadult,
        #     'nbchildren': nbchildren,
        # }
        nbrooms=1
        hotelid=0
        current_user = request.user
        myhotel = HotelUser.objects.filter(user=current_user).all().values()
        print('myhotel')
        print(myhotel)
        # print(myhotel[0]['id'])

        if myhotel:
            hotelid=0
        roomslist = getRoomAvailability(checkin, checkout, hotelid, nbadult, nbchildren, nbrooms)

        # roomslist.append(room1)

        rooms={
            'rooms' : roomslist,
            'groomtype' : groomtype
        }
        return render(request, "availabilityroom.html", rooms)
    else:
        return render(request, "availabilityroom.html", rooms)


    # return render(request, "availabilityroom.html", rooms)

def getwhereofAvalabilitydays( fromdate, todate):
    fromdateasdate = datetime.strptime(fromdate, '%Y-%m-%d')
    fromdateasint = int(fromdateasdate.strftime('%j'))

    todateasdate = datetime.strptime(todate, '%Y-%m-%d')
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
            # if i==intermediateasint :
            #     continue
            toreturnstr = toreturnstr + " and "

        # toreturnstr= toreturnstr + " and "

        for i in range(1, todateasint + 1):
            toreturnstr = toreturnstr + "d" + str(i) + "=0"
            if i == todateasint:
                continue
            toreturnstr = toreturnstr + " and "

    return toreturnstr


def getRoomAvailability(fromdate, todate, hotelid, nbadult, nbchildren, nbrooms):

    sql1 = " SELECT roomManager_room.id,roomManager_room.title,roomManager_roomtype.capacity ,roomManager_roomtype.type_name,roomManager_roomtype.type_name_ar,roomManager_roomtype.price_per_day FROM roomManager_room  INNER JOIN roomManager_roomtype on roomManager_room.rtype_id = roomManager_roomtype.id  INNER JOIN roomManager_availability_room on roomManager_room.id = roomManager_availability_room.room_id "
    sql = str(sql1) + " where " + getwhereofAvalabilitydays(fromdate, todate)


    if int(hotelid) > 0:
        sql = str(sql) + " And roomManager_room.hotel_id= " + str(hotelid)

    capacity =  int(nbadult) + int(nbchildren)
    if capacity > 0:
        sql = str(sql) + " And roomManager_roomtype.capacity>= " + str(capacity)

    # print(sql)
    # roomslist.append(room1)
    roomslist=[]
    room1 = {
        'id': '',
        'title': '',
        'capacity': '',
        'roomtype': '',
        'roomtype_ar': '',
        'price_per_day': '',
        'checkin': fromdate,
        'checkout': todate,
        'nbadult': nbadult,
        'nbchildren': nbchildren,
    }
    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()

        for row in rows:
            room1 = {
                'id': row[0],
                'title': row[1],
                'capacity': row[2],
                'roomtype': row[3],
                'roomtype_ar': row[4],
                'price_per_day': row[5],
                'checkin': fromdate,
                'checkout': todate,
                'nbadult': nbadult,
                'nbchildren': nbchildren,
            }
            roomslist.append(room1)
    return roomslist