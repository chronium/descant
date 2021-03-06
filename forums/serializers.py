from hashlib import md5

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Post, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'colour', 'posts')


class TagForTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'colour')

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    was_edited = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'author_name', 'contents',
                  'post_date', 'last_edit_date', 'reply_to',
                  'was_edited', 'avatar_url', 'contents_marked_up',
                  'can_edit')

    def get_author_name(self, obj):
        return obj.author.username

    def get_was_edited(self, obj):
        return obj.was_edited()

    def get_avatar_url(self, obj):
        emailhash = md5(obj.author.email.strip().lower().encode('utf-8')).hexdigest()
        return "https://secure.gravatar.com/avatar/{}?d=identicon".format(emailhash)

    def get_can_edit(self, obj):
        if self.context['request'].user.is_authenticated():
            if self.context['request'].user.has_perm('forums.change_post', obj):
                return True
            else:
                return False
        return False


class TopicSerializer(serializers.ModelSerializer):
    reply_count = serializers.SerializerMethodField()
    author_name = serializers.SerializerMethodField()
    was_edited = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'tag_ids', 'author', 'author_name',
                  'contents', 'post_date', 'last_edit_date', 'reply_count',
                  'was_edited', 'avatar_url', 'contents_marked_up',
                  'is_locked', 'can_edit')

        read_only_fields = ('replies',)

    def get_reply_count(self, obj):
        return Post.objects.all().filter(reply_to=obj).count()

    def get_author_name(self, obj):
        return obj.author.username

    def get_was_edited(self, obj):
        return obj.was_edited()

    def get_avatar_url(self, obj):
        emailhash = md5(obj.author.email.strip().lower().encode('utf-8')).hexdigest()
        return "https://secure.gravatar.com/avatar/{}?d=identicon".format(emailhash)

    def get_can_edit(self, obj):
        if self.context['request'].user.is_authenticated():
            if self.context['request'].user.has_perm('forums.change_post', obj):
                return True
            else:
                return False
        return False


class PostOrTopicSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    was_edited = serializers.SerializerMethodField()
    avatar_url = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'author', 'author_name', 'contents',
                  'post_date', 'last_edit_date', 'is_topic',
                  'was_edited', 'avatar_url', 'contents_marked_up',
                  'can_edit')

    def get_author_name(self, obj):
        return obj.author.username

    def get_was_edited(self, obj):
        return obj.was_edited()

    def get_avatar_url(self, obj):
        email_hash = md5(obj.author.email.strip().lower().encode('utf-8')).hexdigest()
        return "https://secure.gravatar.com/avatar/{}?d=identicon".format(email_hash)

    def get_can_edit(self, obj):
        if self.context['request'].user.is_authenticated():
            if self.context['request'].user.has_perm('forums.change_post', obj):
                return True
            else:
                return False
        return False

class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'posts', 'date_joined', 'avatar_url')

    def get_avatar_url(self, obj):
        emailhash = md5(obj.email.strip().lower().encode('utf-8')).hexdigest()
        return "https://secure.gravatar.com/avatar/{}?d=identicon".format(emailhash)


class UserStatsSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'date_joined', 'avatar_url', 'post_count')

    def get_avatar_url(self, obj):
        emailhash = md5(obj.email.strip().lower().encode('utf-8')).hexdigest()
        return "https://secure.gravatar.com/avatar/{}?d=identicon".format(emailhash)

    def get_post_count(self, obj):
        return obj.posts.count()


class UserGravatarSerializer(serializers.ModelSerializer):
    gravatar_url = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('gravatar_url',)

    def get_gravatar_url(self, obj):
        emailhash = md5(obj.email.strip().lower().encode('utf-8')).hexdigest()
        return "https://secure.gravatar.com/avatar/{}?d=identicon".format(emailhash)
