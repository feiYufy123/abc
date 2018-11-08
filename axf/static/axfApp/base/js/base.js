$(function () {
    document.documentElement.style.fontSize = innerWidth / 10 + "px";

    //     http://www.sunck.wang:8000/cart/
    urlStr = location.href;
    idStr = urlStr.split("/")[3];
    $span = $(document.getElementById(idStr));
    $span.css("background", "url(/static/axfApp/base/img/"+idStr+"1.png)");
    $span.css("background-size", "0.8rem");
});