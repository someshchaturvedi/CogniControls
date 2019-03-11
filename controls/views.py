from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from controls.sync_func import sync
# from django.core.serializers import serialize
from controls.models import *
import requests
import datetime
import json
from django.db.models import Max


@login_required(login_url='login')
def controls(request):
    if request.user.username == 'hulksmash':
        return render(request, 'controls/admin.html')
    elif request.user.username == 'cogni_c1':
        return render(request, 'controls/controls1.html')

    elif request.user.username == 'cogni_c2':
        return render(request, 'controls/controls2.html')

    elif request.user.username == 'cogni_c3':
        return render(request, 'controls/controls3.html')

    return redirect('login')


@login_required()
def search(request):
    if(request.method == 'POST'):
        data = request.POST.copy()
        if not Participant.objects.filter(cogni_id=data['cogni_id']).exists():
            return JsonResponse(
                {'message': 'ID does not exsist'}, status=404)
        p = Participant.objects.get(cogni_id=data['cogni_id'])
        if(CheckIn.objects.filter(
                participant__cogni_id=data['cogni_id']).exists()):
            return JsonResponse(
                {'message': 'Controls 1 completed'}, status=404)
        data = {
            "results": []
        }
        for r in p.reciepts.all():
            obj = {
                    "cogni_id": p.cogni_id,
                    "name": p.name,
                    "address": p.address,
                    "college": p.college,
                    "contact": p.mobile,
                    "payment_id": r.payment_id,
                    "amount": r.amount,
                    "method": r.method,
                    "type": r.payment_type,
                    "events": 'Cognizance',
                }
            data['results'].append(obj)
        return JsonResponse(data, safe=True)


@login_required()
def controls2_data(request):
    data = {"results": []}
    for c in CheckIn.objects.filter(controls1_done=True, controls2_done=False):
        _object = {
            "cogni_id": c.participant.cogni_id,
            "checkin_id": c.id,
            "amount": Reciept.objects.filter(
                participant=c.participant, payment_type='central')[0].amount,
            "name": c.participant.name,
            "college": c.participant.college,
            "kit_issued": c.kit_issued,
            "id_issued": c.id_issued
        }
        data["results"].append(_object)
    return JsonResponse(data, safe=True)


@login_required()
def search3(request):
    if(request.method == 'POST'):
        data = request.POST.copy()
        if not Participant.objects.filter(cogni_id=data['cogni_id']).exists():
            return JsonResponse(
                {'message': 'ID does not exsist'}, status=404)
        p = Participant.objects.filter(cogni_id=data['cogni_id'])[0]
        c = CheckIn.objects.filter(participant=p)[0]
        if c.caution is True:
            return JsonResponse(
                {'message': 'Caution Money Already Refunded'}, status=404)
        central = False
        if(len(p.reciepts.all()) == 0):
            return JsonResponse(
                {'message': 'Payment not done'}, status=404)
        for r in p.reciepts.all():
            if r.payment_type == 'central':
                central = True
        if central is False:
            return JsonResponse(
                {'message': 'No central payment done'}, status=404)
        data = {
            "results": []
        }
        obj = {
                    "cogni_id": p.cogni_id,
                    "name": p.name,
                    "college": p.college,
                    "mobile": p.mobile,
                    "email": p.email,
                    "gender": p.gender,
                    "controls1_at": c.controls1_at,
                    "controls2_at": c.controls2_at,
            }
        data['results'].append(obj)
        return JsonResponse(data, safe=True)


@login_required()
def controls3_submit(request):
    if(request.method == 'POST'):
        data = request.POST.copy()
        p = Participant.objects.get(cogni_id=data['cogni_id'])
        c = CheckIn.objects.filter(participant=p)[0]
        c.controls3_at = datetime.datetime.now()
        c.caution = True
        c.save()
        return JsonResponse({"message": "done"}, safe=True)


@login_required()
def controls2_allot(request):
    if(request.method == 'POST'):
        data = request.POST.copy()
        checkin_obj = CheckIn.objects.get(id=data['checkin_id'])
        if data['kit_issued'] == 'true':
            data['kit_issued'] = True
        else:
            data['kit_issued'] = False
        if data['id_issued'] == 'true':
            data['id_issued'] = True
        else:
            data['id_issued'] = False
        checkin_obj.kit_issued = data['kit_issued']
        checkin_obj.id_issued = data['id_issued']
        if(checkin_obj.kit_issued is True and checkin_obj.id_issued is True):
            checkin_obj.controls2_done = True
            checkin_obj.controls2_at = datetime.datetime.now()
        checkin_obj.save()
        return JsonResponse({"message": "done"}, safe=True)


@login_required()
def controls1_submit(request):
    if(request.method == 'POST'):
        print('yo')
        data = request.POST.copy()
        p = Participant.objects.get(cogni_id=data['cogni_id'])
        c = CheckIn(
            participant=p,
            noc=True,
            college_id=True,
            controls1_done=True,
            controls1_at=datetime.datetime.now()
        )
        c.save()
        return JsonResponse({"message": "done"}, safe=True)


@login_required()
def sync_db(request):
    if request.user.username != 'hulksmash':
        return JsonResponse(
            {'message': 'Not Allowed'}, status=403)
    else:
        last_id = 0
        if(len(Reciept.objects.all()) > 0):
            last_id = Reciept.objects.all().\
                aggregate(Max('p_id'))['p_id__max']
        url = 'https://api.cognizance.org.in/api/members/login/'
        data = {
            'email': 'controls@cognizance.org.in',
            'password': 'controls2018cognizance'
        }
        headers = {'content-type': 'application/json'}

        r = requests.post(url, data=json.dumps(data), headers=headers)
        token = json.loads(r.text)['token']
        url = 'https://api.cognizance.org.in/api/admin/controls/reciept/' +\
            str(last_id)
        request_headers = {
            "Authorization": "Token " + token,
        }

        r = requests.get(url, headers=request_headers)
        data = json.loads(r.text)
        sync(data)
        return JsonResponse({"message": "done"}, safe=True)
