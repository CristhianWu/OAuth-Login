from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from .models import user_info_extend
from .serializers import UserRegisterSerializer

from supertokens_python.recipe.emailpassword.syncio import sign_up, sign_in, update_email_or_password, \
    reset_password_using_token
from supertokens_python.recipe.userroles.syncio import add_role_to_user
from supertokens_python.recipe.session.syncio import create_new_session, get_session, revoke_session
from supertokens_python.recipe.emailpassword.interfaces import RecipeUserId, WrongCredentialsError, \
    EmailAlreadyExistsError
from supertokens_python.recipe.emailverification.asyncio import send_email_verification_email, is_email_verified

# Error handling imports
from supertokens_python.recipe.emailpassword.interfaces import (
    UpdateEmailOrPasswordOkResult, PasswordPolicyViolationError,
    PasswordResetTokenInvalidError, UnknownUserIdError)

from supertokens_python.recipe.emailverification.interfaces import CreateEmailVerificationTokenOkResult, \
    SendEmailVerificationEmailAlreadyVerifiedError, CreateEmailVerificationTokenEmailAlreadyVerifiedError, \
    VerifyEmailUsingTokenOkResult, VerifyEmailUsingTokenInvalidTokenError

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        tenant_id = "public"
        app_id = "public"

        try:
            if user_info_extend.objects.filter(id_document=request.data['id_document']).exists():
                return Response({'error': 'This ID is already used'}, status=status.HTTP_409_CONFLICT)
        
            # SuperTokens register
            new_user = sign_up(
                tenant_id=tenant_id,
                email=request.data['email'],
                password=request.data['password']
            )

            # If email is already in use
            if isinstance(new_user, EmailAlreadyExistsError):
                return Response({
                    'error': 'El correo ingresado ya está en uso',
                    'status': EmailAlreadyExistsError.status
                }, status=status.HTTP_409_CONFLICT)
            
            # Add role to user
            add_role_to_user(
                tenant_id=tenant_id,
                user_id=new_user.user.id,
                role=request.data['role']
            )

            # Save user extended information
            with transaction.atomic():
                user_info_extend.objects.create(
                    app_id=app_id,
                    user_id=new_user.user.id,
                    name=request.data['name'],
                    last_name=request.data['last_name'],
                    id_document=request.data['id_document']
                )

            return Response({
                'message': 'Usuario registrado con éxito',
                'user_id': new_user.user.id
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"[Error] Registro: {e}")
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginUserView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Both email and password are required'}, status=400)

        tenant_id = "public"

        try:
            # Login from supertokens
            user = sign_in(
                tenant_id=tenant_id,
                email=email,
                password=password
            )

            # Manually create session
            session = create_new_session(
                request=request,
                tenant_id=tenant_id,
                recipe_user_id=RecipeUserId(user.user.id)
            )

            # User data ready to be returned
            user_data = {
                "user_id": user.user.id,
                "email": user.user.emails,
                "time_joined": user.user.time_joined,
            }

            access_token = session.access_token

            return Response({
                'mensaje': 'Usuario logeado con éxito',
                'user': user_data,
                'tokens': {
                    'access_token': access_token,
                }
            }, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=400)