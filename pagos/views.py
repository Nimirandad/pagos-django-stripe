from django.conf import settings
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

import stripe


class VistaInicio(TemplateView):
    template_name = 'index.html'


class VistaAprobado(TemplateView):
    template_name = 'aprobado.html'


class VistaCancelado(TemplateView):
    template_name = 'cancelado.html'


@csrf_exempt
def configuracion_stripe(request):
    if request.method == 'GET':
        config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(config, safe=False)


@csrf_exempt
def proceder_pago_orden(request):
    if request.method == 'GET':
        url_app = 'http://127.0.0.1:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY

        try:
            revision_pago = stripe.checkout.Session.create(
                client_reference_id = request.user.id if request.user.is_authenticated else None,
                success_url=url_app + 'aprobado?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=url_app + 'cancelado/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'price': settings.PRECIO_PRODUCTO,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': revision_pago['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    evento = None

    try:
        evento = stripe.Webhook.construct_event(
            payload, signature_header, endpoint
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if evento['type'] == 'checkout.session.completed':
        print('El pago fue exitoso')

    return HttpResponse(status=200)