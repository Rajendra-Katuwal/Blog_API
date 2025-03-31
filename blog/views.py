from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogSerializer, CommentSerializer
from .models import Blog, Comments

# For fetching all the blogs from the database
@api_view(['GET'])
def get_all_blogs(request):
    all_blogs = Blog.objects.all()
    serializer = BlogSerializer(all_blogs, many=True)
    return Response({"all_blogs": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_by_id(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response({"message": "Blog doesn't exists"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blog)
    return Response({"blog": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_blog(request, id):
    try:
        blog = Blog.objects.get(pk=id)
        blog.delete()
        return Response({"message": "Blog deleted sucessufully."}, status=status.HTTP_200_OK)
    except Blog.DoesNotExist:
        return Response({"message": "Blog doesn't exists"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_blog(request):
    serializer = BlogSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"blog_data":serializer.data, "message":"Blog posted sucessfully"}, status=status.HTTP_201_CREATED)
    return Response({"error": serializer.errors, "message": serializer.error_messages}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_blog(request, id):
    try:
        blog = Blog.objects.get(pk=id)
    except Blog.DoesNotExist:
        return Response({"message": "Blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    serializer = BlogSerializer(blog, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"blog_data": serializer.data, "message": "Blog updated successfully."}, status=status.HTTP_200_OK)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# For posting comment in a certain blog
@api_view(["POST"])
def post_comment(request):
    data = request.data
    blog_id = data.get("blog_id")
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        return Response({"message": "Blog doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    blog_comment = {"comment_text": data.get("comment_text"), "blog": blog.id}
    if not blog_comment["comment_text"]:
        return Response({"message": "Cannot find the comment in the request."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = CommentSerializer(data=blog_comment)
    if serializer.is_valid():
        serializer.save()
        return Response({"comment": serializer.data, "message": "Comment posted successfully."}, status=status.HTTP_201_CREATED)
    return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_blog_comments(request, blog_id):
    try:
        comments = Comments.objects.filter(blog_id=blog_id)
    except Comments.DoesNotExist:
        return Response({"message": "No comments found."}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CommentSerializer(comments, many=True)
    return Response({"comments": serializer.data}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_comment(request, comment_id):
    try:
        comment = Comments.objects.get(pk=comment_id)
    except Comments.DoesNotExist:
        return Response({"message": "Comment with this id not found."}, status=status.HTTP_404_NOT_FOUND)

    comment.delete()
    return Response({"message": "Comment deleted sucessufully."}, status=status.HTTP_200_OK)








'''
Same stuff as above but using class based views, mixins and generic views
'''
from rest_framework.views import APIView
from django.http import Http404



class BlogListCreate(APIView):
    """
    List all the available blogs and create a new blog post.
    """

    def get(self, request):
        blogs = Blog.objects.all()
        if not blogs:
            return Response({"message": "No blogs posted yet."})
        serializer = BlogSerializer(blogs, many=True)
        return Response({"blogs": serializer.data}, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = BlogSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"blog": serializer.validated_data, "message": "Blog posted successfully."}, status=status.HTTP_201_CREATED)


class BlogDetails(APIView):
    """
    Retrieve, Update, Delete a instance of the Blog.
    """

    def get_object(self, id):
        try:
            return Blog.objects.get(pk=id)
        except Blog.DoesNotExist:
            return Response({"message": "No blog with this id found."}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, id):
        blog = self.get_object(id)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)
    
    def put(self, request, id):
        blog = self.get_object(id)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"blog": serializer.validated_data, "message": "Blog updated successfully."}, status=status.HTTP_200_OK)
        return Response({"message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id):
        blog = self.get_object(id)
        if not type(blog)==Blog:
            return blog
        blog.delete()
        return Response({"messge":"Blog deleted sucessfully."}, status=status.HTTP_200_OK)


# Using Mixin and generic api view

from rest_framework import generics
from rest_framework import mixins



class CommentListCreate(mixins.ListModelMixin, 
                        mixins.CreateModelMixin, 
                        generics.GenericAPIView):
    """
    List all the comments from the database and create a comment for a post.
    """
    # queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'blog_id'  # the field from the model with which we want to look up the data in the database
    lookup_url_kwarg = 'blog_id'  # Specify the URL keyword argument name to use for lookup
    # The above two attributes becomes like "lookup_field = look_url_kwarg" at last the 

    def get_queryset(self):
        blog_id = self.kwargs.get(self.lookup_url_kwarg)  # Get the blog_id from the URL kwargs
        # Check if the blog with the given blog_id exists
        if not Blog.objects.filter(pk=blog_id).exists():
            return Response({"message": "No blog with this id found."}, status=status.HTTP_404_NOT_FOUND)
        # Filter the queryset based on the blog_id
        return Comments.objects.filter(blog_id=blog_id)
    

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if type(queryset)==Response:
            return queryset
        if queryset==None:
            return Response({"message": "No comment yet."})
        return self.list(self, request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if type(queryset)==Response:
            return queryset
        # Get the blog_id from the URL kwargs
        blog_id = self.kwargs.get('blog_id')
        request.data['blog'] = blog_id  # Add the blog_id to the request data
        # Now call the create method to save the comment
        return self.create(request, *args, **kwargs)


class CommentDetail(mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    generics.GenericAPIView):
    """
    Retrieve, Delete, Update the comments from a particular blog.
    """
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'comment_id'  # Specify the field name to use for lookup

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

