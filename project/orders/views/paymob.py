from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from orders.models.order import Order
from orders.models.payment import Payment
from orders.paymobService import get_auth_token, create_paymob_order, generate_payment_key, verify_paymob_hmac
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def start_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.status == "cancelled":
        return Response(
            {"error": "This order is cancelled and cannot be paid."},
            status=400
        )
    
    if order.status in ["processing", "shipped", "delivered"]:
        return Response(
            {"error": "This order has already been paid."},
            status=400
        )
    
    if order.payments.filter(status="paid").exists():
        return Response(
            {"error": "This order already has a completed payment."},
            status=400
        )
    
    if order.items.count() == 0:
        return Response({"error": "Cannot pay for an empty order."}, status=400)

    payment = Payment.objects.create(
        order=order,
        amount=order.total_price,
        status="init"
    )

    amount_cents = int(order.total_price * 100)

    auth_token = get_auth_token()

    paymob_order_id = create_paymob_order(auth_token, amount_cents)
    payment.paymob_order_id = paymob_order_id
    payment.status = "pending"
    payment.save()

    billing_data = {
        "first_name": order.user.first_name or "User",
        "last_name": order.user.last_name or "Name",
        "email": order.user.email,
        "phone_number": order.phone_number or "01000000000",
        "apartment": "NA", "floor": "NA", "street": "NA",
        "building": "NA", "city": "Cairo", "country": "EG",
        "state": "NA"
    }

    token = generate_payment_key(auth_token, paymob_order_id, amount_cents, billing_data)

    payment.payment_token = token
    payment.save()

    iframe_url = (
        f"https://accept.paymob.com/api/acceptance/iframes/"
        f"{settings.PAYMOB_IFRAME_ID}?payment_token={token}"
    )

    return Response({"payment_url": iframe_url})



@csrf_exempt
@api_view(["GET"])
def paymob_callback(request):

    data = request.data if request.method == "POST" else request.GET

    # given_token = request.GET.get("token")
    # if given_token != settings.PAYMOB_CALLBACK_SECRET:
    #     return Response({"error": "Unauthorized callback"}, status=401)

    if not verify_paymob_hmac(data):
        return Response({"error": "Invalid HMAC signature"}, status=401)

    paymob_order_id = data.get('order')
    success = data.get('success') in ["true", "True", True, 1, "1"]
    transaction_id = data.get('id')

    if not paymob_order_id:
        return Response({"error": "order id missing"}, status=400)

    try:
        payment = Payment.objects.get(paymob_order_id=paymob_order_id)
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)

    payment.paymob_transaction_id = transaction_id

    if success:
        payment.status = "paid"
        payment.is_success = True
        payment.order.status = "processing"
        payment.order.save()
    else:
        payment.status = "failed"
        payment.is_success = False

    payment.save()
    return Response({"status": "ok"})
