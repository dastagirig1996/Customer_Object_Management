from django.shortcuts import render,redirect
from django.http import JsonResponse
# from django.http import 
import datetime
import json

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer
from .serializers import CustomerSerializer
import jwt
from django.contrib.auth import authenticate
from customers.auth import JWTAuth
import time 
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

ACCESS_TOKEN_EXPIRY = 20
REFRESH_TOKEN_EXPIRY = 60*60*24*7


private_key = "gchvbnmpltfb3opmfnic4+54sff"

def create_access_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': time.time() + ACCESS_TOKEN_EXPIRY,
    }
    access_token = jwt.encode(payload, private_key, algorithm='HS256')
    return access_token

def create_refresh_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': time.time()  + REFRESH_TOKEN_EXPIRY,
    }
    refresh_token = jwt.encode(payload, private_key, algorithm='HS256')
    return refresh_token


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data
        resp_data = {"acces_token": None,"refresh_token":None, "message": ""}
        user = authenticate(**data)
        user_id = user.id
        print("came"*10)
        print(request, "n"*10)
        # print(request.Meta)
        if user:
            access_token = create_access_token(user_id)
            resp_data["acces_token"] = access_token
            refresh_token = create_refresh_token(user_id)
            resp_data["refresh_token"] = refresh_token
            resp_data["message"] = "OK"
            return Response(resp_data, status=status.HTTP_201_CREATED)
        return Response(resp_data, status=status.HTTP_401_UNAUTHORIZED)

class Refresh_token(APIView):
    def get(request,token):
        refersh_token = Refresh_token.objects.get(name = token)
        print(refersh_token)
        if refersh_token:
            return redirect('login/',)
        else:
            return Response({"message":"Please login again"},  status=status.HTTP_403_FORBIDDEN)



def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, private_key, algorithms=['HS256'])
        return payload['user_id']
    except ExpiredSignatureError:
        raise Exception('Refresh token has expired')
    except InvalidTokenError:
        raise Exception('Invalid token')


def refresh_access_token_view(request):
    if request.method == 'POST':
        try:
            print("get refresh token from cookie")
            refresh_token = request.COOKIES.get('refresh_token')
        except:
            print("get refresh token from request_body")
            body = json.loads(request.body)
            refresh_token = body.get('refresh_token')
        
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token is missing'}, status=400)

        user_id = decode_refresh_token(refresh_token)
        if isinstance(user_id, JsonResponse):
            return user_id  
        new_access_token = create_access_token(user_id)
        return JsonResponse({'access_token': new_access_token})
    return JsonResponse({'error': 'Invalid request method'}, status=405)





class CustomerDetailView(APIView):
    def get(self, request, id=None):
        if id:
            try:
                customer = Customer.objects.get(id=id)
                serializer = CustomerSerializer(customer)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id=None):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id=None):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        customer.delete()
        return Response({"message": "Customer deletion done"}, status=status.HTTP_204_NO_CONTENT)
    














# class Ref
# def refresh_access_token(refresh_token):
#     try:
#         # Validate the refresh token
#         user_id = decode_refresh_token(refresh_token)
        
#         # If valid, create a new access token
#         new_access_token = create_access_token(user_id)
#         return new_access_token
    
#     except Exception as err:
#         return {"error": err}







# class LoginAPI(APIView):
#     authentication_classes = []
#     permission_classes = []
#     def post(self, request):
#         data = request.data
#         resp_data = {"token": None, "message": ""}
#         user = authenticate(**data)
#         print("came"*100)
#         if user:
#             payload = {"userId": user.id}
#             resp_data["token"] = jwt.encode(payload,private_key, algorithm="HS256")
#             # resp_data["token"] = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
#             resp_data["message"] = "OK"
#             return Response(resp_data, status=status.HTTP_201_CREATED)
#         return Response(resp_data, status=status.HTTP_401_UNAUTHORIZED)


# def create_tokens(user_id):
#     # Access Token Payload
#     access_payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.now() + datetime.timedelta(minutes=15),  # Access token expires in 15 minutes
#         'iat': datetime.datetime.utcnow()  # Issued at
#     }
    
#     # Create the Access Token
#     access_token = jwt.encode(access_payload, SECRET_KEY, algorithm='HS256')
    
#     # Refresh Token Payload
#     refresh_payload = {
#         'user_id': user_id,
#         'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),  # Refresh token expires in 7 days
#         'iat': datetime.datetime.utcnow()
#     }
    
#     # Create the Refresh Token
#     refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm='HS256')
    
#     return access_token, refresh_token

# # Example usage
# user_id = 123  # Replace with actual user identifier
# access_token, refresh_token = create_tokens(user_id)

# print("Access Token:", access_token)
# print("Refresh Token:", refresh_token)


# from rest_framework import status
# from .utilits import encode_access_token, encode_refresh_token,decode_token
# from django.contrib.auth import authenticate

# class LoginView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
        
#         user = authenticate(username=username, password=password)
#         if user:
#             access_token = encode_access_token(user.id)
#             refresh_token = encode_refresh_token(user.id)
#             return Response({
#                 'access_token': access_token,
#                 'refresh_token': refresh_token
#             }, status=status.HTTP_200_OK)
#         return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)




# class CustomerDetailView(APIView):
#     def get(self, request, id=None):
#         if id:
#             try:
#                 customer = Customer.objects.get(id=id)
#                 serializer = CustomerSerializer(customer)
#             except Customer.DoesNotExist:
#                 return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             customers = Customer.objects.all()
#             serializer = CustomerSerializer(customers, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request):
#         serializer = CustomerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def put(self, request, id=None):
#         try:
#             customer = Customer.objects.get(id=id)
#         except Customer.DoesNotExist:
#             return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         serializer = CustomerSerializer(customer, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def delete(self, request, id=None):
#         try:
#             customer = Customer.objects.get(id=id)
#         except Customer.DoesNotExist:
#             return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
#         customer.delete()
#         return Response({"message": "Customer deletion done"}, status=status.HTTP_204_NO_CONTENT)
    
















''''


class CustomerDetailView(APIView):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None
        token = token.split(' ')[1]  # Remove 'Bearer' part
        user_id = decode_token(token)
        if isinstance(user_id, str):  # Token invalid or expired
            return None
        return user_id

    def get(self, request, id=None):
        id = self.authenticate(request)
        if id:
            try:
                customer = Customer.objects.get(id=id)
                serializer = CustomerSerializer(customer)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id=None):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, id=None):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        customer.delete()
        return Response({"message": "Customer deletion done"}, status=status.HTTP_204_NO_CONTENT)
    














'''


















'''
    
    class CustomerView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            user = Customer.objects.get(id=pk)
            customers_data = {
                "id":pk,
                "name":user.name,
                "phone":user.phone,
                "email":user.email,
                "address":user.address,
            }
        else:
            customers = Customer.objects.all()
            customers_data = [ { "id":customer.id, "name":customer.name,"phone":customer.phone ,"email":customer.email, 
                                "address":customer.address} for customer in customers]
        
        return Response(customers_data)
    


    def post(self,request):
        rd = request.data
        customer = Customer(name=rd.get("name"), phone=rd.get("phone"),
                           email=rd.get("email"), address=rd.get("address"))
        
        msg = ""
        try:
            customer.save()
            msg = "You have successfully registered"
        except Exception as err:
            msg = str(err)
        return Response(msg)
    

        
    def put(self, request, pk):
        data = json.loads(request.body) #dump
        modal_data = Customer.objects.get(id=pk)

        for key, value in data.items():
            if hasattr(modal_data, key):  
                setattr(modal_data, key, value)
        
        msg= ""
        try:
            modal_data.save()
            msg="You have successfully Updated"
        except Exception as err:
            msg = err

        return Response(msg)
    

    
    def delete(self, request, pk):
        instance = Customer.objects.get(id=pk)
        msg=""
        try:
            instance.delete()
            msg="Successfully deleted"
        except Exception as err:
            msg = str(err)
        return Response(msg)



        

    
    '''