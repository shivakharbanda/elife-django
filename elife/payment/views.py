from django.shortcuts import render
from plans.models import Plans, Orders
from django.http import HttpResponse, HttpResponseRedirect
import razorpay
from elife import settings
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
# Create your views here.

import razorpay


razorpay_client = razorpay.Client(auth=(settings.razorpay_id, settings.razorpay_account_id))

"""
@login_required
def payment(request):
    if request.method == "POST":
        try:
            order = Orders.objects.get(user = request.user)
            plan = Plans.objects.get(plan_name = order.pack)
            amount = plan.price
        except:
            return HttpResponse("Something went wrong")

        order.total_amount = amount
        total_amount = amount
        order.save()

        order_currency = "INR"
        callback_url = str(get_current_site(request)) + "/handlerequest/"
        print(callback_url)
        razorpay_order = razorpay_client.order.Create(dict(amount= total_amount*100, currency = order_currency, receipt = order.order_id, payment_capture = "0"))
        print(razorpay_order["id"])
        order.razorpay_order_id = razorpay_order["id"]
        order.save()

    return render(request, 'payment/paymentsummaryrazorpay.html', {"order": order, "order_id": razorpay_order["id"], "orderId": order.order_id, "final_price": total_amount * 100, "razorpay_merchant_id": settings.razorpay_id, "callback_url":callback_url})

"""

def payment_confirm(request):
    if request.method =="GET":
        order = Orders.objects.get(user = request.user)
        amount = order.total_amount
        ctx = {
            "order":order,
            "amount": amount
        }
        return render(request, "payment/payment_confirm.html", ctx)
    if request.method == "POST":
        success_url = reverse_lazy('payment- summary')
        return HttpResponseRedirect(success_url)

@login_required
def payment(request):

    order = Orders.objects.get(user = request.user)
    plan = Plans.objects.get(plan_name = order.pack)
    amount = plan.price
    order.total_amount = amount
    total_amount = amount
    order.save()

    order_currency = 'INR'

    callback_url =str(get_current_site(request))+"/handlerequest/"
    print(callback_url)
    notes = {'order-type': "basic order from the website", 'key':'value'}
    razorpay_order = razorpay_client.order.create(dict(amount=total_amount*100, currency=order_currency, notes = notes, receipt=order.order_id, payment_capture='0'))
    print(razorpay_order['id'])
    order.razorpay_order_id = razorpay_order['id']
    order.save()
    ctx = {
        'order':order, 
        'order_id': razorpay_order['id'], 
        'orderId':order.order_id, 
        'final_price':total_amount, 
        'razorpay_merchant_id':settings.razorpay_id, 
        'callback_url':callback_url
    }
    
    return render(request, 'payment/paymentsummaryrazorpay.html', ctx)


@csrf_exempt
def handlerequest(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', "")
            order_id = request.POST.get('razorpay_order_id', "")
            signature = request.POST.get('razorpay_signature', "")

            param_dict = {
                "razorpay_order_id":order_id,
                "razorpay_payment_id": payment_id,
                "razorpay_signature": signature

            }
            print("here 1")
            print(order_id)
            try:
                order_db = Orders.objects.get(razorpay_order_id= order_id)
            except:
                return HttpResponse("505 Not found 1")

            order_db.razorpay_payment_id = payment_id
            order_db.razorpay_signature = signature
            order_db.save()
            result = razorpay_client.utility.verify_payment_signature(param_dict)
            print(result)
            if result==True:
                amount = order_db.total_amount * 100 
                try:
                    razorpay_client.payment.capture(payment_id, amount)
                    print("here3")
                    order_db.payment_status = 1
                    order_db.save()
                    return render(request, "payment/payment_success.html")
                except:
                    order_db.payment_status = 2
                    order_db.save()
                    return render(request, "payment/payment_failed.html")
        except:
            return HttpResponse("505 no0 found!!!!!!!!!!!")