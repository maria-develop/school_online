from rest_framework.serializers import ModelSerializer
from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
