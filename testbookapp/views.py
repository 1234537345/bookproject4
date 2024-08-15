from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import bookprofile
#from .models import bookprofile,Cart,Cart_item


def wlcmpage(request):
    return render(request, 'admin/wlcmpage.html')


def createbook(request):
    if request.method == 'POST':
        bookname = request.POST.get('bookname')
        bookprice = request.POST.get('bookprice')
        author = request.POST.get('author')
        bookimage = request.FILES.get('bookimage')
        quantity=request.POST.get('quantity')
        p = bookprofile(
            bookname=bookname, bookprice=bookprice, author=author, bookimage=bookimage, quantity=quantity)
        p.save()
    return render(request, 'admin/createbook.html')


def index(request):
    return render(request, 'admin/base.html')


def viewdetails(request, p_id):
    p = bookprofile.objects.get(id=p_id)
    return render(request, 'admin/viewdetails.html', {'p': p})


def listdetails(request):
    values = bookprofile.objects.all()
    return render(request, 'admin/listbook.html', {'values': values})


def updatebook(request, p_id):
    p = bookprofile.objects.get(id=p_id)
    if request.method == 'POST':
        bookname = request.POST.get('bookname')
        bookprice = request.POST.get('bookprice')
        author = request.POST.get('author')
        bookimage = request.FILES.get('bookimage')
        quantity= request.POST.get('quantity')
        p.bookname = bookname
        p.bookprice = bookprice
        p.author = author
        p.bookimage = bookimage
        p.quantity = quantity
        p.save()
    return render(request, 'admin/updatedetails.html', {'p': p})


def deletedetails(request, p_id):
    p = bookprofile.objects.get(id=p_id)
    p.delete()
    return redirect('list')


def searchbook(request):
    query = None
    books = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        books = bookprofile.objects.filter(Q(bookname__icontains=query))
    else:
        books = []
    return render(request, 'admin/search.html', {'books': books, 'query': query})


