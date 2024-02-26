from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .emails import *
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout

# class RegisterAPI(APIView):
#     def post(self,request):
#         try:
#             data=request.data
#             serializer=PasswordResetSerializer(data=data)
#             if serializer.is_valid():
#                 user_mail=User.objects.filter(email=serializer.validated_data['email'])
#                 if user_mail:
#                     serializer.save()
#                     print("account exists")
#                     send_otp_via_email(serializer.data['email'])
#                     return Response({
#                         'status':200,
#                         'message':'please check mail',
#                         'data':serializer.data, 
#                     })
                
            
#                 return Response({
#                     'status':400,
#                     'message':'something went wrong',
#                     'data':'Account with this mail does not exist',

#                 })
#             # print("87909")
#             return Response({
#                     'status':400,
#                     'message':'something went wrong',
#                     'data':serializer.errors,

#                 })
            
#         except Exception as e:
#             # print("123s")
#             print(e)
#             return Response({'key': 'value'}, status=status.HTTP_200_OK)
        
class VerifyOTP(APIView):

    def post(self, request, email):
      
        data=request.data
        serializer=VerifyOTPSerializer(data=data)
       
        if serializer.is_valid():
            
            otp=serializer.data['otp']
            new_p = serializer.data['new_password']
            # serializer.data['mail']=email
            user=User.objects.filter(email=email)
            
            if not user.exists():
                return Response({
                'status':400,
                'message':'something went wrong',
                'data':'invalid mail',

            })
            if user[0].otp!=otp:
                return Response({
                'status':400,
                'message':'something went wrong',
                'data':'wrong otp',

            })

            user=user.first()
            user.set_password(new_p)
            print(new_p)
            # print("Earlier pwd", user.password)
            user.password=new_p
            # print("New pwd", user.password)
            user.is_verified=True
            user.save()
            
            return Response({
            'status':200,
            'message':'Account verified',
            'data':{},

            })


        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        # except Exception as e:
        #     return Response({'key': 'value'}, status=status.HTTP_200_OK)
        
class VerifyEmail(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = EmailVerificationSerializer(data=request.data)
        print("!23")
        if serializer.is_valid():
            print("8977")
            user=User.objects.filter(email=serializer.validated_data['mail'])
            if user:
                send_otp_via_email(serializer.data['mail'])
                
                return Response({
                    'status':200,
                    'message':'email sent',
                    'data':serializer.data,
                })

            #user with that mail does not exist
            return Response({
                    'status':400,
                    'message':'something went wrong',
                    'data':'Account with this mail does not exist',

                })
            
        return Response({
                    'status':400,
                    'message':'something went wrong',
                    'data':serializer.errors,

                })

# class ResetPassword(APIView):
#     def post(self, )
    
class SignIn(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user=User.objects.get(email=serializer.validated_data['email'])
            if user and authenticate(username=serializer.validated_data['email'], password=serializer.validated_data['password']):
                login(request, user)
                return Response({
                    'status':200,
                    'message':'User logged in',
                    'data':serializer.data,
                })

            #user with that mail does not exist
            return Response({
                    'status':400,
                    'message':'something went wrong',
                    'data':'Wrong password',

                })
            
        return Response({
                    'status':400,
                    'message':'something went wrong',
                    'data':serializer.errors,

                })
    
class SignOut(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            usr = request.user
            logout(request)
            return Response({
                'status':200,
                'message':'User logged out',
                'data':usr.email,
            })
        except:
            return Response({
                    'status':400,
                    'message':'something went wrong',

                })
    
class AdminMonitor(APIView):
   
    def get_object(self, queryset=None):
        return self.request.user
    
    def patch(self, request, *args, **kwargs):
        self.object = self.get_object()
        user = request.user
        serializer = EmailVerificationSerializer(data=request.data)
        try:
            if serializer.is_valid():
                if user.is_admin == True:
                    usr=User.objects.get(email=serializer.validated_data['mail'])
                    e = usr.email
                    usr.delete()
                    return Response({
                        'status':200,
                        'message':'User deleted',
                        'user':e,
                    })
                return Response({
                    'status':400,
                    'message':'Permission denied',
                })
            return Response({
                        'status':400,
                        'message':'something went wrong',
                        'data':serializer.errors,

                    })
        except:
            return Response({
                'status':400,
                'message':'something went wrong',
                'data':serializer.errors,
            })