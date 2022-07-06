# Generated by Django 4.0.5 on 2022-07-06 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('roomManager', '0001_initial'),
        ('booking', '0001_initial'),
        ('currencyapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicebooked',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roomManager.service'),
        ),
        migrations.AddField(
            model_name='roomvisitor',
            name='roombooked',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.roombooked'),
        ),
        migrations.AddField(
            model_name='roomvisitor',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.visitor'),
        ),
        migrations.AddField(
            model_name='roombooked',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.reservation'),
        ),
        migrations.AddField(
            model_name='roombooked',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='roomManager.room'),
        ),
        migrations.AddField(
            model_name='roombooked',
            name='services',
            field=models.ManyToManyField(related_name='services', through='booking.ServiceBooked', to='roomManager.service'),
        ),
        migrations.AddField(
            model_name='roombooked',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roomManager.roomtype'),
        ),
        migrations.AddField(
            model_name='roombooked',
            name='visitor',
            field=models.ManyToManyField(related_name='visitors', through='booking.RoomVisitor', to='booking.visitor'),
        ),
        migrations.AddField(
            model_name='review',
            name='usr',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reservation',
            name='currency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='currencyapp.currency'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.visitor'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='roomtype',
            field=models.ManyToManyField(through='booking.RoomBooked', to='roomManager.roomtype'),
        ),
        migrations.AddField(
            model_name='checkinvisitor',
            name='checkin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.checkin'),
        ),
        migrations.AddField(
            model_name='checkinvisitor',
            name='visitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.visitor'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='booking',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='booking.reservation'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='booking.visitor'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roomManager.room'),
        ),
        migrations.AddField(
            model_name='checkin',
            name='visitor',
            field=models.ManyToManyField(through='booking.CheckInVisitor', to='booking.visitor'),
        ),
    ]
