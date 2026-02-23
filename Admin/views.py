from django.shortcuts import render, redirect, get_object_or_404
from django_daraja.mpesa.core import MpesaClient
from Admin.models import Product


# Create your views here.
def admin(request):
    products = Product.objects.all()
    return render(request, 'admin.html',{'products':products})

def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')

        Product.objects.create(name=name, price=price, description=description)
        return redirect('admin')
    return render(request, 'add_item.html')

def delete_item(request,id):
    products = get_object_or_404(Product,id=id)
    products.delete()
    return redirect('admin')

def mpesa_pay(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        amount = int(request.POST.get('amount'))

        client = MpesaClient()

        account_ref = "Emobilis Tech Institute"
        desc = "School fees payment"

        callback_url = "https://emobilis.co.ke/callback"
        response = client.stk_push(phone,amount,account_ref,desc,callback_url)
        return render(request, 'payment_form.html',{"message":"STK push sent"})
    return render(request,'payment_form.html')
