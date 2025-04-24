from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model

from .utils import send_email_verification_mail
from threading import Thread


User = get_user_model()


# This view is to get the user details of the logged in user using the access token
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_me(request):
    auth_headers = request.headers.get('Authorization')
    if auth_headers and auth_headers.startswith('Bearer '):
        token = auth_headers.split(' ')[1]
        try:
            access_token = AccessToken(token=token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Send email verification asynchronously
    # Thread(target=send_email_verification_mail, args=(request, user)).start()

        return Response({"message": "Account Created. Verify your email to activate."}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_email(request):
    token = request.data.get('token')
    try:
        access_token = AccessToken(token=token)
        user_id = access_token['user_id']
        user = User.objects.get(id=user_id)

        # If user email is already verified, return a message
        if user.is_email_verified:
            return Response({'message': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)
        user.is_active = True
        user.is_email_verified = True
        user.save()
        return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if user.check_password(password):
        if not user.is_email_verified:
            return Response({'error': 'Email not verified'}, status=status.HTTP_400_BAD_REQUEST)
        # Generate JWT tokens
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        return Response({
            'refresh': str(refresh_token),
            'access': str(access_token),
        }, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['POST'])
def logout(request):
    try:
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        # We can only blacklist the refresh token, not the access token
        # The access token is short-lived and does not need to be blacklisted, It will expire on its own in a short time.
        token.blacklist() 
        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def user_list(request):
    '''
    View that accepts get request and sends list of all the users as response.
    '''
    queryset = User.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_detail(request, pk):
    '''
    Accepts a GET request and a primarykey(pk) from the url parameter and sends info about that paricular user.
    '''
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def user_profile(request):
    user = request.user
    if user.is_authenticated:
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([IsAuthenticated])
@api_view(['PUT', "PATCH"])
def update_user_profile(request):
    user = request.user
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def deactivate_user(request):
    user = request.user
    user.is_active = False
    user.save()
    return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([IsAuthenticated])
@api_view(['DELETE'])
def delete_user(request):
    user = request.user
    if (user.is_active == False):
        return Response({"message": "The user is currently not active."}, status=status.HTTP_400_BAD_REQUEST)
    user.delete()
    return Response

