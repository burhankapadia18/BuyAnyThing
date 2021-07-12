from django.contrib.sites import requests
from django.shortcuts import render
from django.http import HttpResponse
from .models import Product, Contact, Orders, OrderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum


# Create your views here.

def index(request):
    params = {}
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "shop/index.html", params)


def contact(request):
    f = 0
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        f = 1
    return render(request, "shop/contact.html", {'f': f})


def about(request):
    return render(request, "shop/about.html")


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps([updates, order[0].items_json, order[0].amount], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, "shop/search.html")


def prodView(request, pid):
    # fetch the product using id
    product = Product.objects.filter(id=pid)
    return render(request, "shop/prodView.html", {'product': product[0]})

MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        amount = request.POST.get('amount', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')

        order = Orders(items_json=items_json, amount=amount, name=name, email=email, address=address, city=city,
                       state=state,
                       zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        Oid = order.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': Oid})
        # request paytm to transfer the amount to your account after the payment by the user
        param_dict = dict()
        param_dict["body"] = {
            "requestType": "Payment",
            "mid": "YOUR_MID_HERE",
            # "websiteName": "WEBSTAGING",
            "WEBSITE": "WEBSTAGING",
            "orderId": str(order.order_id),
            "callbackUrl": "http://127.0.0.1:8000/shop/handlePayment/",
            "txnAmount": {
                "value": str(amount),
                "currency": "INR",
            },
            "userInfo": {
                "custId": email,
            },
        }
        checksum = Checksum.generateSignature(json.dumps(param_dict["body"]), MERCHANT_KEY)
        param_dict["head"] = {
            "CHECKSUMHASH": checksum
        }
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


@csrf_exempt
def handlePayment(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verifySignature(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentStatus.html', {'response': response_dict})
