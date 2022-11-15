import recipes
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe

from .models import CustomUser, Subscription

User = get_user_model()


class CurrentUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
        extra_kwargs = {"password": {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=request.user, author=obj
        ).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.author.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        if Subscription.objects.filter(
                user=user,
                author=current_user
        ).exists():
            return True
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            queryset = Recipe.objects.filter(
                author=obj.author)[:recipe_limit]
        else:
            queryset = Recipe.objects.filter(
                author=obj.author)
        serializer = recipes.serializers.ShortRecipeSerializer(
            queryset, read_only=True, many=True
        )
        return serializer.data


class SubscribeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    author = serializers.SlugRelatedField(
        slug_field='id',
        queryset=CustomUser.objects.all(),
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        validators = UniqueTogetherValidator(
            queryset=CustomUser.objects.all(),
            fields=('user', 'author'),
            message='Такая подписка уже существует!'
        )

    def validate(self, data):
        request = self.context['request']
        if data['user'] == data['author'] and request.method == 'POST':
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return SubscriptionSerializer(
            instance.author,
            context={'request': request}
        ).data
