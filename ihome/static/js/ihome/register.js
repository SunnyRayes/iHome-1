function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if (window.performance && typeof window.performance.now === "function") {
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = (d + Math.random() * 16) % 16 | 0;
        d = Math.floor(d / 16);
        return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
    });
    return uuid;
}

var uuid = "";

// 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    // 1. 获取UUID
    uuid = generateUUID();
    // 2. 拼接URL
    var url = "/api/1.0/img_code?uuid=" + uuid;
    // 3. 修改请求地址
    $('.image-code>img').prop('src', url);

}

function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".phonecode-a").removeAttr("onclick");
    var mobile = $("#mobile").val();
    if (!mobile) {
        $("#mobile-err span").html("请填写正确的手机号！");
        $("#mobile-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err span").html("请填写验证码！");
        $("#image-code-err").show();
        $(".phonecode-a").attr("onclick", "sendSMSCode();");
        return;
    }

    // 通过ajax方式向后端接口发送请求，让后端发送短信验证码
    var params = {
        'mobile': mobile,
        'img_code': imageCode,
        'uuid': uuid
    };
    $.ajax({
        url: "/api/1.0/sms_code",
        method: "POST",
        data: JSON.stringify(params),
        headers: {'X-CSRFToken': getCookie('csrf_token')},
        contentType: "json",
        success: function (data) {
            if (data.errno === '0') {
                console.log(data.errmsg)
            } else {
                alert(data.errmsg)
            }

        }

    })
}

$(document).ready(function () {
    generateImageCode();  // 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性

    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#imagecode").focus(function () {
        $("#image-code-err").hide();
    });
    $("#phonecode").focus(function () {
        $("#phone-code-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
        $("#password2-err").hide();
    });
    $("#password2").focus(function () {
        $("#password2-err").hide();
    });


    $('.form-register').submit(function (event) {
        event.preventDefault();
        var mobile = $('#mobile').val();
        var sms_code = $('#phonecode').val();
        var password = $('#password').val();
        var password2 = $('#password2').val();

        params = {
            mobile: mobile,
            sms_code: sms_code,
            password: password,
            password2: password2
        };
        if(!mobile){
            $('#mobile-err span').html('请输入手机');
            $('#mobile-err span').show();
        }
         if(!mobile){
            $('#phone-code-err span').html('请输入手机验证码');
            $('#phone-code-err span').show();
        }
         if(!mobile){
            $('#password-err span').html('请输入密码');
            $('#password-err span').show();
        }
         if(!mobile){
            $('#password2-err span').html('请确认密码');
            $('#password2-err span').show();
        }
        if(password !== password2){
            $('#password2-err span').html('两次输入的密码不一致');
            $('#password2-err span').show();
        }
        $.ajax({
            url: "api/1.0/users",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(params),
            headers: {
                "X-CSRFToken": getCookie("csrf_token")
            },
            success: function (data) {
                if (data.errno === '0') {
                    location.href='/'
                }
                else {
                    alert(data.errmsg)
                }
            }
        })
    })

});
