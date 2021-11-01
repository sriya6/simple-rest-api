#from django.shortcuts import render
import json
from django.views import View
from django.http import JsonResponse
from .models import CartItem

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCart(View):

    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        p_name = data.get("product_name")
        p_price = data.get("product_price")
        p_quantity = data.get("product_quantity")

        product_data = {
            'product_name': p_name,
            'product_price': p_price,
            'product_quantity': p_quantity
        }

        cart_item = CartItem.objects.create(**product_data)

        data = {
            "message": f"New item added to the Cart with id: {cart_item.id}"
        }

        return JsonResponse(data, status=201)

    def get(self, request):
        items_count = CartItem.objects.count()
        items = CartItem.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                'product_name': item.product_name,
                'product_price': item.product_price,
                'product_quantity': item.product_quantity
            })

        data = {
            'items': items_data,
            'count': items_count
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class ShoppingCartUpdate(View):

    def patch(self, request, item_id):
        req_body = json.loads(request.body.decode("utf-8"))
        item = CartItem.objects.get(id=item_id)
        # Not allowed to modify product name or price, so only quantity can be modified in shopping cart
        item.product_quantity = req_body['product_quantity']
        item.save()

        data = {
            'message': f'Item {item_id} has been updated'
        }

        return JsonResponse(data)

    def delete(self, request, item_id):
        item = CartItem.objects.get(id=item_id)
        item.delete()

        data = {
            'message': f'Item {item_id} has been deleted'
        }

        return JsonResponse(data)
