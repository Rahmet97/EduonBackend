from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import *

urlpatterns = [
    path('card-register/', csrf_exempt(card_register)),
    path('card-info/', csrf_exempt(card_info)),
    path('card-history/', csrf_exempt(card_history)),
    path('add-terminal/', csrf_exempt(add_terminal)),
    path('remove-terminal/', csrf_exempt(remove_terminal)),
    path('check-terminal/', csrf_exempt(check_terminal)),
    path('hold-create/', csrf_exempt(hold_create)),
    path('hold-dismiss/', csrf_exempt(hold_dismiss)),
    path('hold-charge/', csrf_exempt(hold_charge)),
    # path('payment/', csrf_exempt(payment)),
    # path('payment-to-course/', csrf_exempt(payment_to_course)),
    path('payment-to-course-from-balance/', csrf_exempt(payment_to_course_from_balance)),
    path('send-sms/', csrf_exempt(send_sms_to_user)),
    path('check-sms-and-payment/', csrf_exempt(check_sms_and_payment)),
    path('get-payment-history/', csrf_exempt(get_payment_history)),
    path('get-courses-order-list/', csrf_exempt(GetCourseOrdersList.as_view())),
]
