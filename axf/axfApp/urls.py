from django.conf.urls import url
from axfApp import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^home/$', views.home, name="home"),
    url(r'^market/(\w+)/(\w+)/(\w+)/$', views.market, name="market"),


    url(r'^cart/$', views.cart, name="cart"),
    # 修改购物车
    url(r'^changeCart/$', views.changeCart),
    # 添加订单
    url(r'^addOrder/$', views.addOrder),


    url(r'^mine/$', views.mine, name="mine"),
    # 登陆
    url(r'^login/$', views.login, name="login"),
    # 验证码
    url(r'^sms/$', views.sms, name="sms"),
    # 退出
    url(r'^quit/$', views.quit, name="quit"),
    # 地址相关
    url(r'^showAddress/$', views.showAddress),
    url(r'^changeAddress/$', views.changeAddress),
    url(r'^addAddress/$', views.addAddress),
]