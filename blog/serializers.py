from rest_framework import serializers
from .models import Blog, Comments


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model=Blog
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    blog = serializers.PrimaryKeyRelatedField(queryset=Blog.objects.all())

    class Meta:
        model = Comments
        fields = "__all__"
