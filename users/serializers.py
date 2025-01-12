from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = ['id', 'email', 'phone', 'city', 'avatar', 'groups']
        fields = [
            "id",
            "email",
            "password",
            "phone",
            "city",
            "avatar",
            "groups",
            "is_superuser",
            "is_staff",
        ]
        # fields = "__all__"


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserDetailSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = "__all__"
