function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');


    $.get('/api/1.0/areas', function (response) {
        if (response.errno === '0') {
            rendered_html = template("areas-tmpl", {areas: response.data});
            $('#area-id').html(rendered_html);

        }
        else {
            alert(response.errmsg)
        }

    });

    // TODO: 处理房屋基本信息提交的表单数据
    $('#form-house-info').submit(function (event) {
        event.preventDefault();
        var formdata = {};
        $(this).serializeArray().map(function (x) {
            formdata[x.name] = x.value;
        });
        var facilities = [];
        $('input:checkbox:checked[name=facility]').each(function (i, x) {
            facilities[i] = x.value;
        });
        formdata.facility = facilities;
        $.ajax({
            url: '/api/1.0/house',
            type: 'post',
            contentType: 'application/json',
            data: JSON.stringify(formdata),
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno === '0') {
                    $('#form-house-info').hide();
                    $('#form-house-image').show();
                    $('#house-id').val(response.data.house_id)
                }
                else if (response.errno === '4101') {
                    alert('请先登录');
                    window.href = '/';
                }
                else {
                    alert(response.errmsg)
                }
            }
        })


    });

    // TODO: 处理图片表单的数据
    $('#form-house-image').submit(function (event) {
        event.preventDefault();
        $(this).ajaxSubmit({
            url: '/api/1.0/house/images',
            type: 'post',
            headers: {"X-CSRFToken": getCookie('csrf_token')},
            success: function (response) {
                if (response.errno === '0') {
                    $('.house-image-cons').append('<img src="' + response.data.img_url + '">')
                }
                else if (errno === '4101') {
                    alert('请先登录');
                    location.href = '/';
                }
                else {
                    alert(response.errmsg);
                }
            }
        })
    })
});