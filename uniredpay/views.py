import json

import requests
from django.conf import settings

from django.db.models import F
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from home.models import Users, Course, Order, Speaker
from simplejwt.backends import TokenBackend
from uniredpay import models
from uniredpay.models import PayForBalance, PercentageOfSpeaker, UserSms
from uniredpay.serializers import PayForBalanceSerializers, CourseOrderSerializers
from uniredpay.unired_sms import sms_send

unired_url = {
    '9860': settings.UNICOIN_HOST_HUMO,
    '8600': settings.UNICOIN_HOST_UZCARD
}


# HUMO
# ID мерчанта: 011860000118613
# ID терминала: 23610C9U
# point_code: 100010104110
#
# UZCARD
# ID мерчанта: 90489428
# ID терминала: 92415924
# port: 1010


# Card Register
# data = {
#     'card_number': 'karta raqami',
#     'expire': 'amal qilish vaqti'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def card_register(request):
    url = unired_url.get(request.data.get('card_number')[:4])
    if not url:
        return Response({'result': 'Wrong card number!!!'})
    return Response(
        data=get_request_result(url=url, access_token=login(url), data=request.data, method='card.register'))


# Card Info
# data = {
#     'card_number': 'karta raqami',
#     'expire': 'amal qilish vaqti'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def card_info(request):
    url = unired_url.get(request.data.get('card_number')[:4])
    if not url:
        return Response({'result': 'Wrong card number!!!'})
    return Response(
        data=get_request_result(url=url, access_token=login(url), data=request.data, method='card.info'))


# Card History
# data = {
#     "card_number": "9860040102963614",
#     "expire": "0526",
#     "start_date": "20210910",
#     "end_date": "20211004"
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def card_history(request):
    url = unired_url.get(request.data.get('card_number')[:4])
    if not url:
        return Response({'result': 'Wrong card number!!!'})
    return Response(
        data=get_request_result(url=url, access_token=login(url), data=request.data, method='card.history'))


# Terminal qo'shish
# data: {
#     "merchant": 'merchant_id',
#     "terminal": 'terminal_id'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def add_terminal(request):
    merchant = request.data.get('merchant')
    if len(merchant.strip()) == 8:
        url = settings.UNICOIN_HOST_UZCARD
        data = {
            'merchant': request.data.get('merchant'),
            'terminal': request.data.get('terminal'),
            "type": 1,
            "port": 1010,
            "purpose": "Online to’lovlar amalga oshirish"
        }
    else:
        url = settings.UNICOIN_HOST_HUMO
        data = {
            "merchant": request.data.get('merchant'),
            "terminal": request.data.get('terminal'),
            "type": 1,
            "purpose": "Tolov omalga oshirish",
            "point_code": "100010104110",
            "originator": "Test Trade ",
            "centre_id": "Test eportal"
        }
    return Response(get_request_result(url=url, access_token=login(url), data=data, method='terminal.add'))


# Terminalni tekshirish
# data: {
#     "merchant": 'merchant_id',
#     "terminal": 'terminal_id'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def check_terminal(request):
    merchant = request.data.get('merchant')
    if len(merchant.strip()) >= 15:
        url = settings.UNICOIN_HOST_HUMO
    else:
        url = settings.UNICOIN_HOST_UZCARD
    return Response(
        get_request_result(url=url, access_token=login(url), data=request.data, method='terminal.check'))


# Terminalni o'chirish
# data: {
#     "merchant": 'merchant_id',
#     "terminal": 'terminal_id'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def remove_terminal(request):
    merchant = request.data.get('merchant')
    if len(merchant.strip()) >= 15:
        url = settings.UNICOIN_HOST_HUMO
    else:
        url = settings.UNICOIN_HOST_UZCARD
    return Response(
        get_request_result(url=url, access_token=login(url), data=request.data, method='terminal.remove'))


# Hold yaratish
# data: {
#     "card_number": 'karta raqami',
#     "expire": 'amal qilish vaqti'
#     "amount": 'miqdori'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def hold_create(request):
    url = unired_url.get(request.data.get('card_number')[:4])
    if url == settings.UNICOIN_HOST_UZCARD:
        data = {
            "card_number": request.data.get('card_number'),
            "expire": request.data.get('expire'),
            "amount": request.data.get('amount'),
            "time": 1,
            "merchant": settings.UZCARD_MERCHANT_ID,
            "terminal": settings.UZCARD_TERMINAL_ID
        }
    else:
        data = {
            "card_number": request.data.get('card_number'),
            "expire": request.data.get('expire'),
            "amount": 100,
            "time": 60,
            "merchant": settings.HUMO_MERCHANT_ID,
            "terminal": settings.HUMO_TERMINAL_ID
        }
    return Response(
        data=get_request_result(url=url, access_token=login(url), data=data, method='hold.create'))


# Hold ni bekor qilish
# HUmo
# data: {
#     "hold_id": 'hold_id',
#     "uuid": '{uuid}'
# }
#
# Uzcard
# data = {
#     "hold_id": '{hold_id}'
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def hold_dismiss(request):
    uu_id = request.data.get('uuid')
    if uu_id:
        url = settings.UNICOIN_HOST_HUMO
    else:
        url = settings.UNICOIN_HOST_UZCARD
    return Response(data=get_request_result(url, login(url), request.data, 'hold.dismiss'))


# Hold ni amalga oshirish
# HUmo
# data: {
#     "hold_id": 'hold_id',
#     "uuid": '{uuid}'
#     "amount": midor int
# }
#
# Uzcard
# data = {
#     "hold_id": '{hold_id}'
#     "amount": int
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def hold_charge(request):
    uu_id = request.data.get('uuid')
    if uu_id:
        url = settings.UNICOIN_HOST_HUMO
    else:
        url = settings.UNICOIN_HOST_UZCARD
    return Response(data=get_request_result(url, login(url), request.data, 'hold.charge'))


def payment(card_number, amount, user, expire):
    url = unired_url.get(card_number[:4])

    data = {
        "card_number": card_number,
        "expire": expire,
        "amount": int(amount) * 100,
    }
    if not url:
        return Response({'result': 'Wrong card number!!!'})
    elif url == settings.UNICOIN_HOST_HUMO:
        data['merchant'] = settings.HUMO_MERCHANT_ID
        data['terminal'] = settings.HUMO_TERMINAL_ID
    else:
        data['merchant'] = settings.UZCARD_MERCHANT_ID
        data['terminal'] = settings.UZCARD_TERMINAL_ID

    data1 = get_request_result(url=url, access_token=login(url), data=data, method='payment')
    if data1.get('status'):
        try:
            user.cash += int(amount)
            user.save()
            PayForBalance.objects.create(user=user, amount=int(amount),
                                         payment_id=data1['result']['payment']['id'],
                                         uu_id=data1['result']['payment']['uuid'])
        except:
            Response({
                'status': False,
                'error': "Unexpected Error!!!"
            })
    return Response(data1)


# balansni to'ldirish
# data = {
#     'card_number': '',
#     'expire': ''
#     'amount': ''
#     'is_save': ''
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def send_sms_to_user(request):
    url = unired_url.get(request.data.get('card_number')[:4])

    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = Users.objects.get(id=valid_data['user_id'])
    except:
        return Response({
            'status': False,
            'error_type': "validation error",
        })

    data = {
        "card_number": request.data.get('card_number'),
        "expire": request.data.get('expire'),
    }
    if not url:
        return Response({'result': 'Wrong card number!!!'})
    elif url == settings.UNICOIN_HOST_HUMO:
        data['merchant'] = settings.HUMO_MERCHANT_ID
        data['terminal'] = settings.HUMO_TERMINAL_ID
    else:
        data['merchant'] = settings.UZCARD_MERCHANT_ID
        data['terminal'] = settings.UZCARD_TERMINAL_ID

    data1 = get_request_result(url=url, access_token=login(url), data=data, method='card.register')

    if data1.get('status'):
        try:
            UserSms.objects.filter(user=user).delete()
            if request.data.get('amount'):
                UserSms.objects.create(user=user, sms_code=sms_send(data1['result']['phone']),
                                       card_number=request.data.get('card_number'),
                                       card_expire=request.data.get('expire'),
                                       amount=int(request.data.get('amount')))
            else:
                UserSms.objects.create(user=user, sms_code=sms_send(data1['result']['phone']),
                                       card_number=request.data.get('card_number'),
                                       card_expire=request.data.get('expire'),
                                       amount=0)
            if request.data.get('is_save'):
                user.card_number = request.data.get('card_number')
                user.card_expire = request.data.get('expire')
                user.save(update_fields=['card_number', 'card_expire'])
        except:
            return Response({
                'status': False,
                'error': 'Foydalanuvchida xatolik!!!'
            })

        return Response({
            'status': True,
            'message': f"SMS {data1['result']['phone']} telefon raqamiga jo'natildi!!!"
        })

    return Response(data1)


# balansni to'ldirish
# data = {
#     'sms_code': '',
#     'course_id': ''
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def check_sms_and_payment(request):
    sms_code = request.data.get('sms_code')

    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = Users.objects.get(id=valid_data['user_id'])
    except:
        return Response({
            'status': False,
            'error_type': "validation error",
        })

    try:
        validate = UserSms.objects.get(user=user, sms_code=sms_code)
    except:
        return Response({
            'status': False,
            'error': 'SMS kod xato!!!'
        })

    if request.data.get('course_id'):
        return payment_to_course(card_number=validate.card_number, expire=validate.card_expire, user=user,
                                 course_id=int(request.data.get('course_id')))
    else:
        return payment(card_number=validate.card_number, expire=validate.card_expire, amount=validate.amount, user=user)


def payment_to_course(card_number, expire, user, course_id):
    url = unired_url.get(card_number[:4])

    voucher = user.bonus
    balance = user.cash

    try:
        # course_id = int(request.data.get('course_id'))
        course = Course.objects.get(id=course_id)
        price = course.price
        discount = course.discount
        price -= discount
    except:
        return Response({
            'status': False,
            'error': 'Course not found!'
        })

    data = {
        "card_number": card_number,
        "expire": expire,
    }

    pay_for_balance_amount = 0

    if price <= (voucher + balance):
        data['amount'] = 0
        if price > voucher:
            user.bonus = 0
            user.cash = (voucher + balance) - price
            summa = price - voucher
        else:
            user.bonus = voucher - price
            summa = 0
    else:
        data['amount'] = (price - (voucher + balance)) * 100
        user.bonus = 0
        user.cash = 0
        summa = price - voucher
        pay_for_balance_amount = (price - (voucher + balance))

    if not url:
        return Response({'result': 'Wrong card number!!!'})
    elif url == settings.UNICOIN_HOST_HUMO:
        data['merchant'] = settings.HUMO_MERCHANT_ID
        data['terminal'] = settings.HUMO_TERMINAL_ID
    else:
        data['merchant'] = settings.UZCARD_MERCHANT_ID
        data['terminal'] = settings.UZCARD_TERMINAL_ID

    data1 = get_request_result(url=url, access_token=login(url), data=data, method='payment')

    if data1.get('status'):
        p_of_speaker = PercentageOfSpeaker.objects.get_or_create()[0]
        p_for_speaker = p_of_speaker.from_user * price / 100
        if summa <= p_for_speaker:
            p_for_eduon = 0
        else:
            p_for_eduon = summa - p_for_speaker
        Order.objects.create(course=course, user=user, summa=summa, bonus=min(voucher, price),
                             sp_summa=p_for_speaker, discount=discount,
                             for_eduon=p_for_eduon)
        Speaker.objects.filter(id=course.author.id).update(cash=F('cash') + p_for_speaker)
        if pay_for_balance_amount > 0:
            PayForBalance.objects.create(user=user, amount=pay_for_balance_amount,
                                         payment_id=data1['result']['payment']['id'],
                                         uu_id=data1['result']['payment']['uuid'])
        user.save()
    return Response(data1)


# Kursga to'lov qilish balance dan
# data = {
#     'course_id': ''
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def payment_to_course_from_balance(request):
    try:
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        valid_data = TokenBackend(algorithm='HS256').decode(token, verify=False)
        user = Users.objects.get(id=valid_data['user_id'])
        voucher = user.bonus
        balance = user.cash
    except:
        return Response({
            'status': False,
            'error_type': "validation error",
        })

    try:
        course_id = int(request.data.get('course_id'))
        course = Course.objects.get(id=course_id)
        price = course.price
        discount = course.discount
        price -= discount
    except:
        return Response({
            'status': False,
            'error': 'Course not found!'
        })

    if price <= (voucher + balance):
        if price > voucher:
            user.bonus = 0
            user.cash = (voucher + balance) - price
            summa = price - voucher
        else:
            user.bonus = voucher - price
            summa = 0
        p_of_speaker = PercentageOfSpeaker.objects.get_or_create()[0]
        p_for_speaker = p_of_speaker.from_user * price / 100
        if summa <= p_for_speaker:
            p_for_eduon = 0
        else:
            p_for_eduon = summa - p_for_speaker
        Order.objects.create(course=course, user=user, summa=summa, bonus=min(voucher, price),
                             sp_summa=p_for_speaker, discount=discount,
                             for_eduon=p_for_eduon)
        Speaker.objects.filter(id=course.author.id).update(cash=F('cash') + p_for_speaker)
        user.save()
        return Response({
            'status': True,
            'error': "To'lov muvoffaqiyatli amalga oshirildi!!!"
        })
    else:
        return Response({
            'status': False,
            'error': 'Hisobingizda mablag\' yetarli emas!!!'
        })


# To'lov ni bekor qilish
# Humo
# data = {
#     "payment_id": "{{payment_id}}",
#     "uuid": "{{uuid}}"
# }
# UZcard
# data = {
#     "payment_id": "{{payment_id}}",
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def payment_cancel(request):
    uu_id = request.data.get('uuid')
    if uu_id:
        url = settings.UNICOIN_HOST_HUMO
    else:
        url = settings.UNICOIN_HOST_UZCARD
    return Response(data=get_request_result(url, login(url), request.data, 'payment.cancel'))


# To'lov check
# Humo
# data = {
#     "payment_id": "{{payment_id}}",
#     "uuid": "{{uuid}}"
# }
# UZcard
# data = {
#     "payment_id": "{{payment_id}}",
# }
@api_view(['post'])
@authentication_classes([])
@permission_classes([])
def payment_check(request):
    uu_id = request.data.get('uuid')
    if uu_id:
        url = settings.UNICOIN_HOST_HUMO
    else:
        url = settings.UNICOIN_HOST_UZCARD
    return Response(data=get_request_result(url, login(url), request.data, 'payment.check'))


def login(url):
    try:
        data = dict(
            id="1",
            method="login",
            params=dict(
                login=settings.UNICOIN_LOGIN,
                password=settings.UNICOIN_PASSWORD
            )
        )
        headers = {'Content-type': 'Application/json', 'Accept': 'Application/json'}
        rq = requests.post(url, data=json.dumps(data), headers=headers)

        rsp = rq.json()
    except Exception as e:
        rsp = {
            "status": False,
            "message": "{}".format(e),
            "result": None
        }

    if rsp.get('status'):
        return rsp['result']['access_token']
    else:
        return Response(rsp)


def get_request_result(url, access_token, data, method):
    headers = {
        'Unisoft-Authorization': 'Bearer ' + access_token,
        'Content-type': 'application/json',
        'Accept': 'Application/json'
    }
    data = dict(
        id="1",
        method=method,
        params=data,
    )
    rq = requests.post(url, headers=headers, data=json.dumps(data))
    return rq.json()


class GetPaymentListClass(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = models.PayForBalance.objects.all()
    serializer_class = PayForBalanceSerializers


class GetCourseOrdersList(ListAPIView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = CourseOrderSerializers
