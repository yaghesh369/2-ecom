from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import CategorySerializer , ProductSerializer
from .models import Category , Product


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