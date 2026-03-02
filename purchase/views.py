
from django.shortcuts import render, redirect
from django.db.models import Case, When, Value, CharField, F
from .models import Product, Purchase, purchase_product, Denomination
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse 
import json
import threading
from .help import send_invoice_email


# Create your views here.
#go to billing page
@ensure_csrf_cookie
def billing(request):
    return render(request, 'billEntry.html')

#process the input data
def processBill(request):
    try:
        payload = json.loads(request.body)
        productData = payload.get('products')
        email = payload.get('email')
        cash = payload.get('cash_paid')
        denominationData = payload.get('denomination')
        total_price = 0
        tax_total = 0
        for obj in productData:
            print(obj)
            print("first object " + obj['quantity'])
            try:
                product = Product.objects.get(product_token=obj['product_id'])
            except Product.DoesNotExist:
                return JsonResponse({
                    "status": "error", "message":"Invalid product id: " + obj['product_id']
                }, status=400)
            if product.available_stock < int(obj['quantity']):
                return JsonResponse({
                    "status":"error", "message":"Insufficient stock"
                }, status=400)
            total_price = total_price + (product.price_with_tax * int(obj['quantity']))
            tax_total = tax_total + (product.get_tax_amount * int(obj['quantity']))
        for obj in productData:
            print("second for")
            purchase = Purchase.objects.create(email =email, total_price = total_price)
            productValue = Product.objects.get(product_token = obj['product_id'])
            purchase_product.objects.create(purchase = purchase, product = productValue, quantity = int(obj['quantity']))
            Product.objects.filter(product_token= obj['product_id']).update(available_stock=F('available_stock') - int(obj['quantity']))
        for key, value in denominationData.items():
            print("key: " + key)
            if value != 0:
                Denomination.objects.filter(name=key).update(available_quantity = F('available_quantity') + value)
        request.session['purchaseInfo'] = {
            "email": email,
            "cash": cash,
            "total_price": total_price,
            "tax_total": tax_total,
            "purchase_id": purchase.id
        }
        return JsonResponse({
            "status": "success", "message": "success"
        }, status = 200)
    except Exception as e:
        return JsonResponse({
            "status":"error", "message": str(e)
        }, status = 500)


#go to bill page
def finalBill(request):
    purchaseInfo = request.session.get('purchaseInfo')
    data = purchase_product.objects.select_related('product').filter(purchase=purchaseInfo['purchase_id'])
    denominationData = Denomination.objects.all()
    balanceList = []
    rounded = round(int(purchaseInfo['cash']) - purchaseInfo['total_price'])
    balance = rounded
    givenBalance = rounded
    for denoData in denominationData:
        if balance <= 0:
            break
        if int(denoData.name) <= balance and denoData.available_quantity != 0:
            newBalance = balance%int(denoData.name)
            quantity = (balance - newBalance) / int(denoData.name)
            if denoData.available_quantity < quantity:
                quantity = denoData.available_quantity
                balance = balance - (quantity * int(denoData.name))
            else:
                balance = newBalance
            balanceList.append({"name": denoData.name, "quantity": int(quantity)})
            Denomination.objects.filter(name = denoData.name).update(available_quantity= F('available_quantity') - quantity)
    contentData = {"purchaseInfo": purchaseInfo, "data": data, "rounded": round(purchaseInfo['total_price']), "balanceList": balanceList, "balance": balance, "givenBalance": givenBalance}
    thread = threading.Thread(target=send_invoice_email, args=(purchaseInfo['email'], contentData))
    thread.start()
    return render(request, 'finalBill.html', {"purchaseInfo": purchaseInfo, "data": data, "rounded": round(purchaseInfo['total_price']), "balanceList": balanceList, "balance": balance, "givenBalance": givenBalance})

#customer history
def customerHistory(request):
    return render(request, 'customerHistory.html')

#get purchase history
def purchaseList(request):
    try:
        email = request.POST.get('email')
        data = purchase_product.objects.select_related('product', 'purchase').filter(purchase__email = email)
        return render(request, 'customerHistory.html', {"purchaseData": data, "email": email})
    except Exception as e:
        return render(request, 'customerHistory.html', {"message": str(e)})
