from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

from axfApp.models import Product, Category, ChildCategory, Slider, MainDescription, Customer, Address, Cart, Order

# Create your views here.
def index(request):
    return redirect("/home/")
def home(request):
    # 获取轮播图数据
    sliders = Slider.objects.all()

    # 主体信息数据
    mainDescriptions = MainDescription.objects.all()
    for mainDescription in mainDescriptions:
        products = []
        products.append(Product.objects.filter(categoryId=mainDescription.categoryId).get(productId=mainDescription.product1))
        products.append(Product.objects.filter(categoryId=mainDescription.categoryId).get(productId=mainDescription.product2))
        products.append(Product.objects.filter(categoryId=mainDescription.categoryId).get(productId=mainDescription.product3))
        mainDescription.products = products
    return render(request, "axfApp/home/home.html", {"sliders": sliders, "mainDescriptions": mainDescriptions})


def market(request, categoryId, childId, sortId):
    # 获取分组数据
    categories = Category.objects.all()

    # 获取子组数据
    childCategories = ChildCategory.objects.filter(category__categoryId=categoryId)

    # 获取商品数据
    products = Product.objects.filter(categoryId=categoryId)
    #子组
    if childId != "0":
        products = products.filter(childCid=childId)
    # 排序
    if sortId == "1":
        products = products.order_by("-price")
    elif sortId == "2":
        products = products.order_by("price")
    elif sortId == "3":
        pass

    #找到该用户添加过的该组的所有购物车信息
    cts = Cart.objects.filter(customer__phone=request.session.get("phone")).filter(product__categoryId=categoryId)
    if childId != "0":
        cts = cts.filter(product__childCid=childId)
    for ct in cts:
        for product in products:
            if ct.product.productId == product.productId:
                product.num = ct.num
                break

    return render(request, "axfApp/market/market.html", {"categories": categories, "childCategories": childCategories, "products": products, "gid": categoryId, "cid": childId})





def cart(request):
    # 获取当前用户的购物车信息
    cts = Cart.objects.filter(customer__phone=request.phone)
    return render(request, "axfApp/cart/cart.html", {"cts": cts})
def changeCart(request):
    # 1、先看看该用户是否购买过该商品
    num = int(request.GET.get("num"))
    if num:
        gid = request.GET.get("gid")
        pid = request.GET.get("pid")
        product = Product.objects.filter(categoryId=gid).get(productId=pid)
        user = Customer.objects.get(phone=request.phone)
    else:
        sid = request.GET.get("sid")
    ct = None
    try:
        if num:
            ct = Cart.objects.filter(customer__phone=request.phone).filter(product__categoryId=gid).get(product__productId=pid)
            ct.num += num
            if ct.num == 0:
                ct.delete()
            else:
                ct.save()
        else:
            ct = Cart.objects.get(pk=sid)
            ct.isChoice = not ct.isChoice
            ct.save()
    except Cart.DoesNotExist as e:
        #没有买过
        if num != -1:
            ct = Cart.create(user, product, 1)
            ct.save()
    count = 0
    if ct:
        count = ct.num
    return JsonResponse({"code": 200, "error": 0, "data":{"count":count, "flag":ct.isChoice}})
def addOrder(request):
    #验证库存的问题

    orderid = str(uuid.uuid4())
    phone = request.session.get("phone")
    user = Customer.objects.get(phone=phone)
    address = Address.objects.get(pk=1)
    #将该用户被选中的购物车数据的isOrder设置为True,并计算总价
    cts = Cart.objects.filter(customer__phone=phone).filter(isChoice=True)
    price = 0
    order = Order.create(orderid, user, address, 0)
    order.save()
    for ct in cts:
        ct.isOrder = True
        ct.order = order
        ct.save()
        price += (ct.product.price * ct.num)
    order.price = price
    order.save()
    return redirect("/cart/")







def mine(request):
    phone = request.session.get("phone")
    if not phone:
        phone = "未登录"
    return render(request, "axfApp/mine/mine.html", {"phone": phone})
#登陆
import uuid
from django.core.cache import cache
def login(request):
    fromPath = request.GET.get("from")
    if request.method == "GET":
        return render(request, "axfApp/mine/login.html", {"fromPath": fromPath})
    else:
        # 第一次为注册并登陆，后面都属于登陆
        phone = request.POST.get("phone")
        token = str(uuid.uuid4())
        try:
            user = Customer.objects.get(phone=phone)
        except Customer.DoesNotExist as e:
            #注册
            user = Customer.create(phone, token)

        # 状态保持
        request.session["phone"] = phone

        # 写缓存
        cache.set(phone, token)

        user.token = token
        user.save()

        fromPath = "/" + fromPath + "/"
        response = redirect(fromPath)
        # 写名为token的cookie
        response.set_cookie("token", token)

        return response

from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect("/mine/")

from axfApp.sms2 import send_sms
import random
def sms(request):
    mobile = request.GET.get("phone")
    sr = ""
    for i in range(6):
        sr += random.choice("0123456789")
    text = "您的验证码是：%s。请不要把验证码泄露给其他人。"%sr
    # send_sms(text, mobile)
    # 存储session
    sr = "666666"
    request.session["verifycode"] = sr
    print("-----------------------sr=%s"%sr)
    return JsonResponse({"code":200, "error": 0, "data":"验证码发送成功%s"%sr})


#地址
def showAddress(request):
    userPhone = request.session.get("phone")
    addresses = Address.objects.filter(customer__phone=userPhone)
    return render(request, "axfApp/mine/showAddress.html", {"addresses": addresses})
def changeAddress(request):
    if request.method == "GET":
        #获取当前地址的信息
        address = Address.objects.get(pk=int(request.GET.get("addressid")))
        return render(request, "axfApp/mine/changeAddress.html", {"address": address})
    else:
        address = Address.objects.get(pk=int(request.POST.get("address")))
        address.name = request.POST.get("name")
        address.phone = request.POST.get("phone")
        address.sex = int(request.POST.get("sex"))
        address.city = request.POST.get("city")
        address.area = request.POST.get("area")
        address.location = request.POST.get("location")
        address.save()
        return redirect("/showAddress/")
def addAddress(request):
    if request.method == "GET":
        return render(request, "axfApp/mine/addAddress.html")
    else:
        name = request.POST.get("name")
        sex = int(request.POST.get("sex"))
        phone = request.POST.get("phone")
        city = request.POST.get("city")
        area = request.POST.get("area")
        location = request.POST.get("location")
        userPhone = request.session.get("phone")
        user = Customer.objects.get(phone=userPhone)
        address = Address.create(name,sex,phone,city,area,location,user)
        address.save()
        return redirect("/showAddress/")