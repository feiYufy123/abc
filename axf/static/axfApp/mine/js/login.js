$(function () {
    $("#smsBtn").bind("click", function () {
        $.ajax({
            url:"/sms/?phone="+$("#phone").val(),
            type:"get",
            success:function(data, status){
                // console.log(data)
            }
        });
    });
});