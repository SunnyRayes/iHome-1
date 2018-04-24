function hrefBack() {
    history.go(-1);
}

// 解析提取url中的查询字符串参数
function decodeQuery() {
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function (result, item) {
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function () {
    // 获取详情页面要展示的房屋编号
    var queryData = decodeQuery();
    var houseId = queryData["id"];

    // TODO: 获取该房屋的详细信息
    $.get('/api/1.0/house/' + houseId, function (response) {
        if (response.errno === '0') {
            var swiper_slide = template('house-image-tmpl', {
                img_urls: response.data.img_urls,
                price: response.data.price
            });
            $('.swiper-container').html(swiper_slide);
            swiper();
            $('.detail-con').html(template('house-detail-tmpl', {house: response.data}))
        }
        else {
            alert(response.errmsg)
        }

    });

    function swiper() {
        var mySwiper = new Swiper('.swiper-container', {
            loop: true,
            autoplay: 2000,
            autoplayDisableOnInteraction: false,
            pagination: '.swiper-pagination',
            paginationType: 'fraction'
        });
    }

    // TODO: 数据加载完毕后,需要设置幻灯片对象，开启幻灯片滚动

});