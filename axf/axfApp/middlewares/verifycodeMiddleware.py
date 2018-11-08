# -*- coding:utf-8 -*-
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect

class VerifycodeMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 判断验证码是否正确
        if request.path == "/login/" and request.method == "POST":
            ccode = request.POST.get("verifycode")
            scode = request.session.get("verifycode")
            if ccode != scode:
                fromPath = request.GET.get("from")
                return redirect("/login/?from=%s" % fromPath)
        return None
