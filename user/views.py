from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'user': UserSerializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
        print(user)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    if user.check_password(password):
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return Response({
            'refresh': str(refresh_token),
            'access': str(access_token),
            'message': 'Login successful',
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def user_list(request):
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)