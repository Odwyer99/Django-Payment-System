# from .models import PaymentRequest
#
# def get_payment_request_or_false(sender, receiver, Amount):
#     try:
#         return PaymentRequest.objects.get(sender=sender, receiver=receiver, Amount=Amount, is_active=True)
#     except PaymentRequest.DoesNotExist:
#         return False