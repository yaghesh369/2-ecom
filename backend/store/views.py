from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CategorySerializer , ProductSerializer,cartItemSerializer,cartSerializer
from .models import Category , Product , CartItem,Cart

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
def getcart(request):
    cart, created = Cart.objects.get_or_create(user=None)
    serializer = cartSerializer(cart)
    return Response({'items': serializer.data.get('items', []), 'total': cart.Total})
@api_view(['POST'])
def addtocart(request):
    product_id=request.data.get('product_id')
    product=Product.objects.get(id=product_id)
    cart,created=Cart.objects.get_or_create(user=None)
    item,created=CartItem.objects.get_or_create(cart=cart,product=product,defaults={'quantity': 1})
    if not created:
        item.quantity+=1
        item.save()
    return Response({"message":"Item added to cart",'cart':cartSerializer(cart).data})

@api_view(['POST'])
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
def removefromcart(request):
    item_id=request.data.get('item_id')
    CartItem.objects.get(id=item_id).delete()
    return Response({"message":"Item removed from cart"})
