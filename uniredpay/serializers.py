from rest_framework import serializers

from home.models import Order
from uniredpay.models import PayForBalance


class PayForBalanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = PayForBalance
        exclude = ['payment_id', 'uu_id']


class CourseOrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
