function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // TODO: 在页面加载完毕向后端查询用户的信息
    $.get('/api/1.0/users', function (response) {
        if (response.errno === '0') {
            $('#user-name').val(response.data.name);
            $('#user-avatar').prop('src', response.data.avatar_url);
        }
        else if (response.errno === '4101') {
            location.href = '/';
        }
        else {
            alert(response.errmsg);
        }
    });
    // TODO: 管理上传用户头像表单的行为
    $('#form-avatar').submit(function (event) {
        event.preventDefault();

        $(this).ajaxSubmit({
            url: '/api/1.0/users/avatar',
            type: 'post',
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            contentType: 'application/json',
            success: function (response) {
                if (response.errno === '0') {
                    $('#user-avatar').prop('src', response.data.avatar_url);
                }
                else if (response.errno === '4101') {
                    location.href = '/';
                }
                else {
                    alert(response.errmsg)
                }
            }
        })
    });

    // TODO: 管理用户名修改的逻辑
    $('#form-name').submit(function (event) {
        event.preventDefault();
        var user_name = $('#user-name').val();
        if (!user_name) {
            alert('请填写用户名');
            return;
        }
        var params = {
            'user_name': user_name
        };
        $.ajax({
            url: '/api/1.0/users',
            type: 'put',
            contentType: 'application/json',
            data: JSON.stringify(params),
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno === '0') {
                    $('.error-msg').hide();
                    showSuccessMsg();
                }
                else if (response.errno === '4101') {
                    location.href = '/';
                }
                else {
                    alert(response.errmsg);
                }
            }
        })
    })

});

