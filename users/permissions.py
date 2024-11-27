from rest_framework.permissions import BasePermission


class IsModer(BasePermission):
    """Проверяет, является ли пользователь модератором."""
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moders').exists()


# class NotModer(BasePermission):
#     def has_permission(self, request, view):
#         """Разрешение только для пользователей, которые не являются модераторами"""
#         return not request.user.is_moder


class IsOwner(BasePermission):
    """
    Разрешение на уровне объекта, позволяющее редактировать объект только его владельцам.
    Предполагается, что экземпляр модели имеет атрибут `owner`.
    """
    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
