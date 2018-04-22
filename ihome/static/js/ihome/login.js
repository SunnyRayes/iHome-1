function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $("#mobile").focus(function () {
        $("#mobile-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
    });
    // TODO: 添加登录表单提交操作
    $('.form-login').submit(function (event) {
        event.preventDefault();

        var mobile = $('#mobile').val();
        var password = $('#password').val();
        var params = {
            'mobile': mobile,
            'password': password
        };
        $.ajax({
            url: '/api/1.0/sessions',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(params),
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno === '0') {
                    location.href = '/';
                }
                else {
                    alert(response.errmsg)
                }
            }
        })
    })
});
