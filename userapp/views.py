from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import bookprofile, Cart, CartItem
from django.shortcuts import render
import stripe
from django.conf import settings
from django.urls import reverse
# Create your views here.

# user.
def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('password1')

        if password == cpassword:
            if User.objects.filter(username=username):
                messages.info(request, 'the user is already in')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'this email is already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'this password is not matching')
            return redirect('register')
    return render(request, 'user/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'please provide correct details')
            return redirect('login')
    return render(request, 'user/login.html')


def logout(request):
    auth.logout(request)
    return redirect('login')


def home(request):
    return render(request, 'home.html')


def home(request):
    vls = bookprofile.objects.all()
    return render(request, 'user/home.html', {'vls': vls})

def filtersearch(request):
    query = None
    books = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        books = bookprofile.objects.filter(Q(bookname__icontains=query))
    else:
        books = []
    return render(request, 'user/searchuser.html', {'books': books, 'query': query})

def userbookdetails(request, p_id):
    p = bookprofile.objects.get(id=p_id)
    return render(request, 'user/userbookdetails.html', {'p': p})


def addtocart(request,book_id):
    book=bookprofile.objects.get(id=book_id)

    if book.quantity>0:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item,item_created= CartItem.objects.get_or_create(cart=cart,book=book)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
    return redirect('view_cart')

def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items=cart.cartitem_set.all()
    cart_item=CartItem.objects.all()
    total_price = sum(item.book.bookprice * item.quantity for item in cart_items)
    total_items=cart_items.count()

    context={'cart_items':cart_items,'cart_item':cart_item,'total_price':total_price,'total_items':total_items}
    return render(request,'user/addtocart.html',context)

def increase_quantity(request,item_id):
    cart_item=CartItem.objects.get(id=item_id)
    if cart_item.quantity<cart_item.book.quantity:
        cart_item.quantity+=1
        cart_item.save()
    return redirect('view_cart')


def decrease_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect('view_cart')

def create_checkout_session(request):
    cart_items=CartItem.objects.all()

    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':

            line_items=[]
            for cart_item in cart_items:
                if cart_item.book:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.book.bookprice * 100),
                            'product_data':{
                                'name':cart_item.book.bookname
                            },
                        },
                        'quantity': cart_item.quantity
                    }
                    line_items.append(line_item)

            if line_item:

                   checkout_session=stripe.checkout.Session.create(
                       payment_method_types=['card'],
                       line_items=line_items,
                       mode='payment',
                       success_url=request.build_absolute_uri(reverse('success')),
                       cancel_url=request.build_absolute_uri(reverse('cancel'))


                   )

                   return redirect(checkout_session.url,code=303)



def success(request):
    cart_items=CartItem.objects.all()
    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity >=cart_item.quantity:
            product.quantity-=cart_item.quantity
            product.save()

    cart_items.delete()

    return render(request,'user/success.html')



def cancel(request):
    return render(request,'user/cancel.html')