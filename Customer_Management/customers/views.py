from django.shortcuts import render
import datetime

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

private_key = "gchvbnmpltfb3opmfnic4+54sff"

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data
        resp_data = {"acces_token": None,"refresh_token":None, "message": ""}
        user = authenticate(**data)
        print("came"*10)
        print(request, "n"*10)
        print(request.Meta)
        if user:
            access_payload = { 'userId': user.id,
                                'exp': time.time()+60*5,
                                # 'iat': datetime.datetime.now()
                                  }
            resp_data["acces_token"] = jwt.encode(access_payload, private_key, algorithm="HS256")
  
            refresh_payload = {'userId': user.id,
                                'exp': time.time()+60*60*24*7,
                                # 'iat': datetime.datetime.now() 
                                }
            resp_data["refresh_token"] = jwt.encode(refresh_payload, private_key, algorithm="HS256")
            resp_data["message"] = "OK"
            return Response(resp_data, status=status.HTTP_201_CREATED)
        return Response(resp_data, status=status.HTTP_401_UNAUTHORIZED)

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