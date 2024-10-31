from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from django.shortcuts import get_object_or_404

class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.AllowAny]

    def get_cart(self):
        if self.request.user.is_authenticated:
            return self.request.user.cart
        else:
            cart_id = self.request.session.get('cart_id')
            if cart_id:
                return get_object_or_404(Cart, id=cart_id)
            else:
                cart = Cart.objects.create()
                self.request.session['cart_id'] = cart.id
                return cart

    def get_object(self):
        return self.get_cart()

class CartItemCreateView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.AllowAny]

    def perform_create(self, serializer):
        cart = self.get_cart()
        serializer.save(cart=cart)

    def get_cart(self):
        if self.request.user.is_authenticated:
            return self.request.user.cart
        else:
            cart_id = self.request.session.get('cart_id')
            if cart_id:
                return get_object_or_404(Cart, id=cart_id)
            else:
                cart = Cart.objects.create()
                self.request.session['cart_id'] = cart.id
                return cart

class CartItemUpdateView(generics.UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated | permissions.AllowAny]

class CartItemDeleteView(generics.DestroyAPIView):
    queryset = CartItem.objects.all()
    permission_classes = [permissions.IsAuthenticated | permissions.AllowAny]
