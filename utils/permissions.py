# from django.contrib.auth import get_user_model
# from rest_framework import permissions
#
# from accounts.models import ProfileImage
# from items.models import Image
#
# User = get_user_model()
#
#
# class IsOwnerOrReadOnly(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         req_user = request.user.username
#         if obj.__class__ == User:
#             return obj.username == req_user
#         elif obj.__class__ == ProfileImage:
#             return obj.profile.user.username == req_user
#         elif obj.__class__ == Image:
#             return obj.item.user.username == req_user
#         else:
#             return obj.user == request.user
