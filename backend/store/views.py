from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from .serializers import ResgisterSerializer, Userserializer
from rest_framework import status
from .serializers import CategorySerializer , ProductSerializer,cartItemSerializer,cartSerializer
from .models import Category , Product , CartItem,Cart,Order, OrderItem

def home(request):
    return HttpResponse("welcome to store")
@api_view(['GET'])
def getproducts(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products , many=True)
    return Response(serializer.data)
   
@api_view(['GET'])
def getproduct(request , pk):
    try: 
        products=Product.objects.get(pk=pk)
        serializer = ProductSerializer(products , context={'request': request})
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"},status=404)

@api_view(['GET'])
def getcategory(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories , many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getcart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = cartSerializer(cart)
    return Response({'items': serializer.data.get('items', []), 'total': cart.Total})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addtocart(request):
    product_id=request.data.get('product_id')
    product=Product.objects.get(id=product_id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    item,created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={'quantity': 1})
    if not created:
        item.quantity+=1
        item.save()
    return Response({"message":"Item added to cart",'cart':cartSerializer(cart).data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updatecart(request):

    item_id=request.data.get('item_id')
    quantity=request.data.get('quantity')
    
    if not item_id or quantity is None:
        return Response({"error": "Item ID and quantity are required"},status=400)
    
    try:
        item=CartItem.objects.get(id=item_id)
        if int(quantity) < 1 :
            item.delete()
            return Response({"message":"Item removed from cart"})
        item.quantity=int(quantity)
        item.save()
        serializer=cartItemSerializer(item)
        return Response({"message":"Item quantity updated","item":serializer.data})
    except CartItem.DoesNotExist:
        return Response({"error": "Item not found"},status=404)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def removefromcart(request):
    item_id=request.data.get('item_id')
    CartItem.objects.get(id=item_id).delete()
    return Response({"message":"Item removed from cart"})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createorder(request):
    try:
        data=request.data
        name=data.get('name')
        address=data.get('address')
        phone=data.get('phone')
        payment_method=data.get('payment_method','COD')
        if not phone.isdigit() or len(phone) < 10:
            return Response({"error": "Invalid phone number"},status=400)
        cart,created=Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return Response({"error": "Cart is empty"},status=400)
        total= sum(item.product.price * item.quantity for item in cart.items.all())
        order = Order.objects.create(user=request.user,total_amount=total)
        for item in cart.items.all():
            OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)
        cart.items.all().delete()
        return Response({"message":"Order created successfully","order_id":order.id})
    except Exception as e:
        return Response({"error": str(e)},status=500)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    serializer = ResgisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message":"User created successfully","user":Userserializer(user).data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

