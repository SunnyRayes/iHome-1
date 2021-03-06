function hrefBack() {
    history.go(-1);
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

function showErrorMsg() {
    $('.popup_con').fadeIn('fast', function () {
        setTimeout(function () {
            $('.popup_con').fadeOut('fast', function () {
            });
        }, 1000)
    });
}

$(document).ready(function () {
    // TODO: 判断用户是否登录

    $(".input-daterange").datepicker({
        format: "yyyy-mm-dd",
        startDate: "today",
        language: "zh-CN",
        autoclose: true
    });
    $(".input-daterange").on("changeDate", function () {
        var startDate = $("#start-date").val();
        var endDate = $("#end-date").val();

        if (startDate && endDate && startDate > endDate) {
            showErrorMsg("日期有误，请重新选择!");
        } else {
            var sd = new Date(startDate);
            var ed = new Date(endDate);
            days = (ed - sd) / (1000 * 3600 * 24);
            var price = $(".house-text>p>span").html();
            var amount = days * parseFloat(price);
            $(".order-amount>span").html(amount.toFixed(2) + "(共" + days + "晚)");
        }
    });
    var queryData = decodeQuery();
    var houseId = queryData["hid"];

    $.get('/api/1.0/house/' + houseId, function (response) {
        if (response.errno === '0') {
            $('.house-info>img').prop('src', response.data.avatar_url);
            $('.house-text>h3').text(response.data.title);
            $('.house-text span').text((response.data.price / 100).toFixed(2));
        }
        else if (response.errno === '4101') {
            location.href = 'login.html'
        }
        else {
            alert(response.errmsg)
        }
    });

    // TODO: 订单提交
    $('.submit-btn').on('click', function () {
        if ($('.order-amount>span').html()) {
            var sd = $('#start-date').val();
            var ed = $('#end-date').val();
            var params = {
                'sd': sd,
                'ed': ed,
                'house_id': houseId
            };
            $.ajax({
                url: '/api/1.0/orders',
                type: 'post',
                contentType: 'application/json',
                data: JSON.stringify(params),
                headers: {'X-CSRFToken': getCookie('csrf_token')},
                success: function (response) {
                    if (response.errno === '0') {
                        location.href = 'orders.html'
                    } else if (response.errno === '4101') {
                        location.href = 'login.html'
                    } else {
                        alert(response.errmsg)
                    }

                }
            })
        }
    })
});
