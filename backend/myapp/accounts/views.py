from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from .models import user_info_extend
from .serializers import UserRegisterSerializer

from supertokens_python.recipe.emailpassword.syncio import sign_up, sign_in
from supertokens_python.recipe.userroles.syncio import add_role_to_user
from supertokens_python.recipe.session.syncio import create_new_session, get_session, revoke_session
from supertokens_python.recipe.emailpassword.interfaces import RecipeUserId, EmailAlreadyExistsError
from supertokens_python.recipe.emailverification.syncio import send_email_verification_email, is_email_verified
from supertokens_python.recipe.emailverification.syncio import create_email_verification_token, verify_email_using_token

from supertokens_python.recipe.emailverification.interfaces import CreateEmailVerificationTokenOkResult, \
    SendEmailVerificationEmailAlreadyVerifiedError, CreateEmailVerificationTokenEmailAlreadyVerifiedError

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
                'message': 'User registered!',
                'user_id': new_user.user.id
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(f"[Error] Register: {e}")
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

            # Verify if email is verified
            is_verified = is_email_verified(recipe_user_id=RecipeUserId(user.user.id),
                                                        email=email)
            if not is_verified:
                return Response({
                    'error': 'Email not verified'
                }, status=401)

            # Create session
            access_token = session.access_token

            return Response({
                'message': 'User successfully logged',
                'user': user_data,
                'tokens': {
                    'access_token': access_token,
                }
            }, status=200)

        except Exception as e:
            return Response({'error': str(e)}, status=400)
        

class LogoutUserView(APIView):
    def post(self, request):
        try:
            # Get session
            session = get_session(request)

            if session is None:
                return Response({'mensaje': 'There is no active session'}, status=401)

            # Revoke session
            revoke_session(session.get_handle())

            return Response({'message': 'Logout Successfully'}, status=200)

        except Exception as e:
            return Response({'error': f"Logout error: {str(e)}"}, status=400)
        

class SendVerificationEmailView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        email = request.data.get('email')
        tenant_id = "public"

        if not user_id or not email:
            return Response({'error': 'user_id and email are required.'}, status=400)

        try:
            result = send_email_verification_email(
                tenant_id=tenant_id,
                user_id=user_id,
                recipe_user_id=RecipeUserId(user_id),
                email=email
            )
            # If email is already verified
            if isinstance(result, SendEmailVerificationEmailAlreadyVerifiedError):
                return Response({
                    'error': 'This email is already verified',
                    'status': result.status
                }, status=409)

            return Response({'message': 'Verification email sent successfully'}, status=200)

        except Exception as e:
            return Response({'error': f"Unexpected error: {str(e)}"}, status=400)
        

class ManuallyVerifyEmailView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        tenant_id = "public"

        if not user_id:
            return Response({'error': 'user_id is required.'}, status=400)

        try:
            token_res = create_email_verification_token(
                tenant_id=tenant_id,
                recipe_user_id=RecipeUserId(user_id)
            )
            # If email is already verified
            if isinstance(token_res, CreateEmailVerificationTokenEmailAlreadyVerifiedError):
                return Response({
                    'error': 'This email is already verified',
                    'status': token_res.status
                }, status=401)

            if isinstance(token_res, CreateEmailVerificationTokenOkResult):
                verify_email_using_token(tenant_id=tenant_id, token=token_res.token)

            return Response({'message': 'Email successfully verified'}, status=200)

        except Exception as e:
            return Response({'error': 'Invalid user ID or unexpected error.'}, status=401)