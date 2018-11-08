$(function () {
    var $isChoses = $(".ischose");
    $isChoses.bind("click", function () {
        var sid = $(this).attr("sid");
        var data = {
            num: 0,
            sid: sid,
            from: "home"
        };
        $.ajax({
            url: "/changeCart/",
            type: "get",
            data: data,
            success: function(data, status) {
                // 找到span
                var $span = $(document.getElementById(sid));
                if (data.error == 0) {
                    if (data.data.flag) {
                        $span.text("√")
                    } else {
                        $span.text("")
                    }
                }
                console.log(data, status)
            }
        })
    });
});