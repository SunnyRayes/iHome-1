//模态框居中的控制
function centerModals() {
    $('.modal').each(function (i) {   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top - 30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function () {
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);
    // TODO: 查询房东的订单
    $.get('/api/1.0/order?role=landlord', function (response) {
        if (response.errno === '0') {
            $('.orders-list').html(template('orders-list-tmpl', {orders: response.data}));
            // TODO: 查询成功之后需要设置接单和拒单的处理
            $(".order-accept").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-accept").attr("order-id", orderId);
            });
            $(".order-reject").on("click", function () {
                var orderId = $(this).parents("li").attr("order-id");
                $(".modal-reject").attr("order-id", orderId);
            });
        }
        else if (response.errno === '4101') {
            location.href = 'login.html'
        }
        else {
            alert(response.errmsg)
        }
    });

    $(".modal-accept").on('click', function (response) {
        var orderId = $(this).attr('order-id');
        console.log(orderId);
        $.ajax({
                url: '/api/1.0/order/status/' + orderId + '?action=accept',
                type: 'put',
                contentType: 'application/json',
                headers: {'X-CSRFToken': getCookie('csrf_token')},
                success: function (response) {
                    if (response.errno === '0') {
                        $('.orders-list>li[order-id=' + orderId + ']>div.order-content>div.order-text>ul li:eq(4)>span').text('待评价');
                        $('.orders-list>li[order-id=' + orderId + ']>div.order-title>div.order-operate').hide();
                        $('#accept-modal').modal('hide');
                    }
                    else if (response.errno === '4101') {
                        location.href = 'login.html'
                    }
                    else {
                        alert(response.errmsg)
                    }
                }
            }
        );

    });
    $('.modal-reject').on('click', function () {

        var orderId = $(this).attr('order-id');
        var reject_reason = $('#reject-reason').val();
        if (!reject_reason) {
            alert('请填写拒单理由');
            return;
        }
        $.ajax({
            url: '/api/1.0/order/status/' + orderId + '?action=reject',
            type: 'put',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({'reject_reason': reject_reason}),
            headers: {'X-CSRFToken': getCookie('csrf_token')},
            success: function (response) {
                if (response.errno === '0') {
                    $('ul.orders-list>li[order-id=' + orderId + ']>div.order-content>div.order-text>ul li:eq(4)>span').text('已拒单');
                    $('ul.orders-list>li[order-id=' + orderId + ']>div.order-title>div.order-operate').hide();
                    $('#reject-modal').modal('hide');
                }
                else if (response.errno === '4101') {
                    location.href = 'login.html';
                }
                else {
                    alert(response.errmsg)
                }
            }
        });
    })
});
