from django.db import models

# Create your models here.

'''
商品表：  products
    name
    longName
    productId
    storeNums
    specifics
    sort
    marketPrice
    price
    categoryId
    childCid
    img
    keywords
    brandId
    brandName
    safeDay
    safeUnit
    safeUnitDesc
    isDelete
'''
class Product(models.Model):
    name = models.CharField(max_length=64)
    longName = models.CharField(max_length=128)
    productId = models.CharField(max_length=64)
    storeNums = models.IntegerField()
    specifics = models.CharField(max_length=32)
    sort = models.IntegerField()
    marketPrice = models.FloatField()
    price = models.FloatField()
    categoryId = models.CharField(max_length=64)
    childCid = models.CharField(max_length=64)
    img = models.CharField(max_length=256)
    keywords = models.CharField(max_length=256)
    brandId = models.CharField(max_length=64)
    brandName = models.CharField(max_length=64)
    safeDay = models.CharField(max_length=64)
    safeUnit = models.CharField(max_length=64)
    safeUnitDesc = models.CharField(max_length=64)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "products"



'''
分组表：categories
    categoryId
    categoryName
    sort 
    isDelete
'''
class Category(models.Model):
    categoryId = models.CharField(max_length=64)
    categoryName = models.CharField(max_length=64)
    sort = models.IntegerField()
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "categories"

'''
子组表：childcategories
    childId   
    childName
    sort
    category    (外键，所属的组)
    isDelete
'''
class ChildCategory(models.Model):
    childId = models.CharField(max_length=64)
    childName = models.CharField(max_length=64)
    sort = models.IntegerField()
    category = models.ForeignKey("Category")
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "childcategories"






'''
轮播图表：sliders
    name
    img
    sort
    trackid
'''
class Slider(models.Model):
    name = models.CharField(max_length=64)
    img = models.CharField(max_length=256)
    sort = models.IntegerField()
    trackid = models.CharField(max_length=64)
    class Meta:
        db_table = "sliders"



'''
主体信息表：maindescriptions
    categoryId
    categoryName
    sort
    img
    product1
    product2
    product3
'''
class MainDescription(models.Model):
    categoryId = models.CharField(max_length=64)
    categoryName = models.CharField(max_length=64)
    sort = models.IntegerField()
    img = models.CharField(max_length=256)
    product1 = models.CharField(max_length=64)
    product2 = models.CharField(max_length=64)
    product3 = models.CharField(max_length=64)
    class Meta:
        db_table = "maindescriptions"





'''
手机号    （主键）
token值   （唯一）
创建时间
最后登录时间
是否注销
'''
class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDelete=False)
class Customer(models.Model):
    objects = CustomerManager()
    phone = models.CharField(max_length=32, primary_key=True)
    token = models.CharField(max_length=128, unique=True)
    createTime = models.DateTimeField(auto_now_add=True)
    lastTime = models.DateTimeField(auto_now=True)
    isDelete = models.BooleanField(default=False)
    class Meta:
        db_table = "customers"
    @classmethod
    def create(cls, phone, token):
        return cls(phone=phone, token=token)





'''
收货地址表：
    联系人姓名
    性别
    电话
    城市
    地区
    详细地址
    地址
    所属用户
'''
class Address(models.Model):
    name = models.CharField(max_length=64)
    sex = models.BooleanField()
    phone = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    area = models.CharField(max_length=64)
    location = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    customer = models.ForeignKey("Customer")
    @classmethod
    def create(cls, name, sex, phone, city, area, location, customer):
        address = city+area+location
        return cls(name=name, sex=sex, phone=phone, city=city, area=area, location=location, customer=customer, address=address)
    class Meta:
        db_table = "addresses"



'''
购物车表：
    所属用户  （外键）
    商品   （外键）
    所属订单  （外键，允许为空）
    数量
    是否选中
    是否进入订单
'''
class CartManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isOrder=False)
class Cart(models.Model):
    objects = CartManager()
    customer = models.ForeignKey("Customer")
    product = models.ForeignKey("Product")
    order = models.ForeignKey("Order", null=True)
    num = models.IntegerField()
    isChoice = models.BooleanField(default=True)
    isOrder = models.BooleanField(default=False)
    @classmethod
    def create(cls, customer, product, num):
        return cls(customer=customer, product=product, num=num)
    class Meta:
        db_table = "carts"



'''
订单表：
    订单编号  （主键）
    所属用户  （外键）
    邮寄地址  （外键）
    总价
    状态
    创建时间
    修改时间
    是否删除
'''
class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(isDelete=False)
class Order(models.Model):
    objects = OrderManager()
    orderId = models.CharField(max_length=128, primary_key=True)
    customer = models.ForeignKey("Customer")
    address = models.ForeignKey("Address")
    price = models.FloatField()
    # 0 1 2 3 4 5
    flag = models.IntegerField(default=1)
    createTime = models.DateTimeField(auto_now_add=True)
    lastTime = models.DateTimeField(auto_now=True)
    isDelete = models.BooleanField(default=False)
    @classmethod
    def create(cls, orderId, customer, address, price):
        return cls(orderId=orderId, customer=customer, address=address, price=price)
    class Meta:
        db_table = "orders"


