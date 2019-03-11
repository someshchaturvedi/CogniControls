from controls.models import *


def sync(data):
    print(data['message'])
    for payment in data['payments']:
        if Participant.objects.filter(cogni_id=payment['UserId']).exists():
                p = Participant.objects.get(cogni_id=payment['UserId'])
        else:
            user = payment['User']
            p = Participant(
                name=user['name'],
                cogni_id=user['id'],
                email=user['email'],
                mobile=user['mobile'],
                address=user['address'],
                city=user['city'],
                state=user['state'],
                college=user['college'],
                gender=user['gender'],
                is_workshop_payment_done=user['workshopPaymentStatus'],
                is_central_payement_done=user['centralPaymentStatus'],
            )
            p.save()
        r = Reciept(
            p_id=payment['id'],
            participant=p,
            amount=int(payment['amount'] / 100),
            payment_id=payment['PaymentId'],
            method=payment['method'],
            payment_type=payment['type']
        )
        r.save()
        print('.')
