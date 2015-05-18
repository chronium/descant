from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from rest_framework import generics
from rest_framework.permissions import AllowAny, DjangoObjectPermissions
from rest_framework.throttling import UserRateThrottle
from guardian.shortcuts import assign_perm
from djoser.signals import user_activated

from .models import Post, Tag
from .serializers import PostSerializer, TopicSerializer, TagSerializer, UserSerializer, UserGravatarSerializer, \
    PostOrTopicSerializer


class DjangoObjectPermissionsOrAnonReadOnly(DjangoObjectPermissions):
    """
    Unauthenticated users aren't automatically rejected.
    """
    authenticated_users_only = False


class StandardThrottle(UserRateThrottle):
    rate = '15/min'  # 1 per 4 seconds

class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    throttle_classes = (StandardThrottle,)


class TopicList(generics.ListCreateAPIView):
    # TODO: logic to set is_topic to true, etc.
    queryset = Post.objects.all().filter(is_topic=True)
    serializer_class = TopicSerializer
    permission_classes = (DjangoObjectPermissionsOrAnonReadOnly,)
    throttle_classes = (StandardThrottle,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, is_topic=True)
        assign_perm('forums.change_post', self.request.user, serializer.instance)
        assign_perm('forums.delete_post', self.request.user, serializer.instance)

class TopicDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().filter(is_topic=True)
    serializer_class = TopicSerializer
    permission_classes = (DjangoObjectPermissionsOrAnonReadOnly,)


class ReplyList(generics.ListCreateAPIView):
    # TODO: Edit creation logic.
    queryset = Post.objects.all().filter(is_topic=False)
    serializer_class = PostSerializer
    permission_classes = (DjangoObjectPermissionsOrAnonReadOnly,)
    throttle_classes = (StandardThrottle,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, reply_to=self.kwargs['reply_to'])
        assign_perm('forums.change_post', self.request.user, serializer.instance)
        assign_perm('forums.delete_post', self.request.user, serializer.instance)

    def get_queryset(self):
        return Post.objects.all().filter(is_topic=False, reply_to=self.kwargs['reply_to'])


class ReplyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all().filter(is_topic=False)
    serializer_class = PostSerializer
    permission_classes = (DjangoObjectPermissionsOrAnonReadOnly,)
    throttle_classes = (StandardThrottle,)


class AnyPostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostOrTopicSerializer
    permission_classes = (DjangoObjectPermissionsOrAnonReadOnly,)
    throttle_classes = (StandardThrottle,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (StandardThrottle,)


class GravatarLink(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserGravatarSerializer
    permission_classes = (AllowAny,)
    throttle_classes = (StandardThrottle,)

@receiver(user_activated)
def add_user_to_group(sender, **kwargs):
    ### TODO: ACTUALLY CREATE THIS GROUP ON MIGRATE!!!
    grp = Group.objects.get(name='registered')
    print (kwargs['user'])
    grp.user_set.add(kwargs['user'])
