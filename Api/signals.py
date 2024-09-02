# signals.py
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from store.models import Cart

@receiver(user_logged_in)
def merge_cart(sender, user, request, **kwargs):
    session_id = request.session.session_key
    if session_id:
        try:
            # Find an anonymous cart with the session_id
            anonymous_cart = Cart.objects.get(session_id=session_id, owner=None)
            
            # Assign the cart to the logged-in user
            anonymous_cart.owner = user.customer
            anonymous_cart.session_id = None  # Clear the session_id after linking the cart
            anonymous_cart.save()
        except Cart.DoesNotExist:
            pass
