from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import Recipe

from .models import CustomUser, Follow

User = get_user_model()


class CurrentUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_subscribed',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {"password": {'write_only': True}}

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request in None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(following=obj, user=user).exists()


class FollowListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.IntegerField(
        source='recipes.count',
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, user):
        current_user = self.context.get('current_user')
        other_user = user.following.all()
        if user.is_anonymous:
            return False
        if other_user.count() == 0:
            return False
        if Follow.objects.filter(user=user, following=current_user).exists():
            return True
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request.GET.get('recipe_limit'):
            recipe_limit = int(request.GET.get('recipe_limit'))
            recipes = Recipe.objects.filter(
                author=obj.author)[:recipe_limit]
        else:
            recipes = Recipe.objects.filter(
                author=obj.author)
        serializer = recipes.serializers.RecipeImageSerializer(
            recipes, read_only=True, many=True
        )
        return serializer.data


class UserFollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='id',
        queryset=User.objects.all(),
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        validators = UniqueTogetherValidator(
            queryset=User.objects.all(),
            fields=('user', 'following'),
            message='Такая подписка уже существует!'
        )

    def validate(self, data):
        request = self.context['request']
        if data['user'] == data['following'] and request.method == 'POST':
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.following,
            context={'request': request}
        ).data
