$(function () {
    var url = location.href;
    var idStr = "yellow" + url.split("/")[4];
    var $span = $(document.getElementById(idStr));
    $span.addClass("yellow");



    //点击分类和排序
    var $typeBtn = $("#typeBtn");
    var $sortBtn = $("#sortBtn");
    var $typeDiv = $("#typeDiv");
    var $sortDiv = $("#sortDiv");

    $typeBtn.bind("click", function () {
        $typeDiv.toggle();
        $sortDiv.hide();
    });
    $sortBtn.bind("click", function () {
        $sortDiv.toggle();
        $typeDiv.hide();
    });
    function func() {
        $(this).hide()
    }
    $typeDiv.bind("click", func);
    $sortDiv.bind("click", func);



    //修改购物车
    var $addBtns = $(".addBtn");
    var $subBtns = $(".subBtn");

    function changeCart() {
        pid = $(this).attr("pid");
        var data = {
            gid: $(this).attr("gid"),
            pid: pid,
            num: $(this).attr("num"),
            from: "home"
        };
        $.ajax({
            url: "/changeCart/",
            type: "get",
            data: data,
            success: function (data, status) {
                if (data.error == 0) {
                    var $span = $(document.getElementById(pid));
                    $span.text(data.data.count);
                } else if (data.error == 1) {
                    location.href = data.data;
                }
            }
        });
    }
    $addBtns.bind("click", changeCart);
    $subBtns.bind("click", changeCart);
});