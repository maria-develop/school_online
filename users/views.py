from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ('payment_date',)
    ordering = ('-payment_date',)
    search_fields = ('amount',)

# class PaymentListAPIView(ListAPIView):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer
    # filter_backends = [DjangoFilterBackend, OrderingFilter]
    # filterset_fields = ['course', 'lesson', 'payment_method']  # Фильтры
    # ordering_fields = ['payment_date']  # Поля для сортировки
    # ordering = ['-payment_date']  # Сортировка по умолчанию
