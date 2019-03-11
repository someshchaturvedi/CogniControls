from django.db import models
import datetime


class Participant(models.Model):
    name = models.CharField(max_length=100)
    cogni_id = models.IntegerField()
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    college = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    is_workshop_payment_done = models.BooleanField(default=False)
    is_central_payement_done = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reciept(models.Model):
    p_id = models.IntegerField(default=0)
    participant = models.ForeignKey(
        Participant, related_name='reciepts', on_delete=models.CASCADE)
    amount = models.IntegerField()
    payment_id = models.CharField(max_length=100, blank=True)
    method = models.CharField(max_length=100, blank=True)
    decription = models.CharField(max_length=100, blank=True)
    payment_type = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.participant.name + '--' + self.payment_type


class CheckIn(models.Model):
    participant = models.OneToOneField(
        Participant, related_name='check_in', on_delete=models.CASCADE)
    noc = models.BooleanField(default=False)
    college_id = models.BooleanField(default=False)
    is_acco = models.BooleanField(default=False)
    kit_issued = models.BooleanField(default=False)
    id_issued = models.BooleanField(default=False)
    caution = models.BooleanField(default=False)
    bhawan = models.CharField(max_length=100, blank=True)
    room_no = models.CharField(max_length=100, blank=True)
    controls1_done = models.BooleanField(default=False)
    controls2_done = models.BooleanField(default=False)
    controls1_at = models.DateTimeField(default=datetime.datetime.now)
    controls2_at = models.DateTimeField(default=datetime.datetime.now)
    controls3_at = models.DateTimeField(default=datetime.datetime.now)

    def __str__(self):
        return self.participant.name
