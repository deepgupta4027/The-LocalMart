from http.client import responses
from django.shortcuts import render
from .models import Product, Contact, Orders, orderUpdate
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from paytm import Checksum
# Create your views here.
from django.http import HttpResponse
MERCHANT_KEY = 'kbJk1DSbJiV_03p5'

# Create your views here.

def index(request):
    products = Product.objects.all()
    print(products)
    # n = len(products)
    # nSlides = (n//4 + ceil((n/4) - (n//4)))

    # # params = { 'no_of_slides': nSlides, 'range' : range(1, nSlides+1), 'product' : products }

    # allProds = [[products, range(1, nSlides), nSlides],
    #             [products, range(1, nSlides), nSlides]]

    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = (n // 4 + ceil((n / 4) - (n // 4)))
        allProds.append([prod, range(1,nSlides),nSlides])

    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)

def searchMatch(query, item):
    '''Return only if query matches the result'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = (n // 4 + ceil((n / 4) - (n // 4)))
        if len(prod) > 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ''}
    if len(allProds) == 0 or len(query) < 3:
        params = {"msg": "No search found based on your search query"}
    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/about.html')

def basic(request):
    return render(request, '{shop/basic.html')

def tracker(request):
    if request.method=="POST":
        OrderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(Order_id=OrderId, email=email)
            if len(order)>0:
                update = orderUpdate.objects.filter(order_id=OrderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                resp = json.dumps([updates, order[0].items_json ], default=str)
                return HttpResponse(resp)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')
    return render(request, 'shop/tracker.html')



def contact(request):
    if request.method == "POST":
        # print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        desc = request.POST.get('desc','')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')

def productView(request,myid):
    product = Product.objects.filter(id=myid)
    return render(request, 'shop/productView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json= request.POST.get('itemsJson', '')
        name = request.POST.get('firstname','') + " " + request.POST.get('lastname','')
        email=request.POST.get('email', '')
        address=request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city=request.POST.get('city', '')
        pincode=request.POST.get('pincode', '')
        phone=request.POST.get('phone', '')

        order = Orders(items_json= items_json, name=name, email=email, address= address, city=city, pincode=pincode, phone=phone)
        order.save()
        thank=True
        print(order.Order_id, thank)
        id = order.Order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id':id})
    return render(request, 'shop/checkout.html')

# def checkout(request):
#     if request.method == "POST":
#         items_json = request.POST.get('itemsJson','')
#         name = request.POST.get('firstname','') + " " + request.POST.get('lastname','')
#         email = request.POST.get('email','')
#         amount = request.POST.get('amount', '')
#         phone = request.POST.get('phone','')
#         pincode = request.POST.get('pincode','')
#         city = request.POST.get('city', '')
#         address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
#         order = Orders(items_json= items_json, name=name, email=email, phone=phone, pincode=pincode, city=city, address=address, amount=amount)
#         order.save()
#         update = orderUpdate(order_id=order.Order_id, update_desc="The order has been placed")
#         update.save()
#         id = Order_id
#         thank = True
#
#
#         #request paytm to transfer the amount to your bank account after payment by user
#         return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
#         # request paytm to transfer the amount to your account after payment by user
#         # param_dict = {
#         #     'MID': 'VkzqXj20943782261219',
#         #     'ORDER_ID': str(order.Order_id),
#         #     'TXN_AMOUNT': str(amount),
#         #     'CUST_ID': 'CUST001',
#         #     'INDUSTRY_TYPE_ID': 'Retail',
#         #     'WEBSITE': 'WEBSTAGING',
#         #     'CHANNEL_ID': 'WEB',
#         #     'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
#         # }
#         #
#         # return render(request, 'shop/paytm.html', {'param_dict': param_dict})
#          # return render(request, 'shop/checkout.html', {'thank': thank})
#     return render(request, 'shop/checkout.html')
#
# @csrf_exempt
# def handlerequest(request):
#     # paytm will send you post request here
#     # return HttpResponse('done')
#     # pass
#     form = request.POST
#     response_dict = {}
#     for i in form.keys():
#         response_dict[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#
#     verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
#     if verify:
#         if response_dict['RESPCODE'] == '01':
#             print('order successful')
#         else:
#             print('order was not successful because' + response_dict['RESPMSG'])
#     return render(request, 'shop/paymentstatus.html', {'response': response_dict})
#

