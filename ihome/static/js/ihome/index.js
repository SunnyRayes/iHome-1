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

function setStartDate() {
    var startDate = $("#start-date-input").val();
    if (startDate) {
        $(".search-btn").attr("start-date", startDate);
        $("#start-date-btn").html(startDate);
        $("#end-date").datepicker("destroy");
        $("#end-date-btn").html("离开日期");
        $("#end-date-input").val("");
        $(".search-btn").attr("end-date", "");
        $("#end-date").datepicker({
            language: "zh-CN",
            keyboardNavigation: false,
            startDate: startDate,
            format: "yyyy-mm-dd"
        });
        $("#end-date").on("changeDate", function () {
            $("#end-date-input").val(
                $(this).datepicker("getFormattedDate")
            );
        });
        $(".end-date").show();
    }
    $("#start-date-modal").modal("hide");
}

function setEndDate() {
    var endDate = $("#end-date-input").val();
    if (endDate) {
        $(".search-btn").attr("end-date", endDate);
        $("#end-date-btn").html(endDate);
    }
    $("#end-date-modal").modal("hide");
}

function goToSearchPage(th) {
    var url = "/search.html?";
    url += ("aid=" + $(th).attr("area-id"));
    url += "&";
    var areaName = $(th).attr("area-name");
    if (undefined == areaName) areaName = "";
    url += ("aname=" + areaName);
    url += "&";
    url += ("sd=" + $(th).attr("start-date"));
    url += "&";
    url += ("ed=" + $(th).attr("end-date"));
    location.href = url;
}

function swiper() {
    var mySwiper = new Swiper('.swiper-container', {
        loop: true,
        autoplay: 2000,
        autoplayDisableOnInteraction: false,
        pagination: '.swiper-pagination',
        paginationClickable: true
    });
}

$(document).ready(function () {
    // TODO: 检查用户的登录状态, 用户状态从session中获取，修改时最好改动一下session
    $.get('/api/1.0/sessions', function (response) {
            if (response.errno === '0') {
                $(".top-bar>.register-login").hide();
                $(".top-bar>.user-info").show();
                $(".top-bar>.user-info>a").text(response.data.name);
            }
            else {
                $(".top-bar>.user-info").hide();
                $(".top-bar>.register-login").show();
            }
        }
    );

    $.get('/api/1.0/house/index', function (response) {
        if (response.errno === '0') {
            $('.swiper-wrapper').html(template('swiper-houses-tmpl', {houses: response.house_list}));
            swiper();
        }
        else {
            alert(response.errmsg)
        }
    });

    // TODO: 数据设置完毕后,需要设置幻灯片对象，开启幻灯片滚动


    // TODO: 获取城区信息,获取完毕之后需要设置城区按钮点击之后相关操作
    $.get('/api/1.0/areas', function (response) {
        if (response.errno === '0') {
            $('.area-list').html(template('area-list-tmpl', {areas: response.data}));
            $('.area-list>a').click(function (event) {
                $('#area-btn').html($(this).html());
                $('.search-btn').attr('area-id', $(this).attr('area-id'));
                $('.search-btn').attr('area-name', $(this).text());
                $('#area-modal').modal('hide');
            });
        }
        else {
            alert(response.errmsg)
        }
    });


    //


    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);               //当窗口大小变化的时候
    $("#start-date").datepicker({
        language: "zh-CN",
        keyboardNavigation: false,
        startDate: "today",
        format: "yyyy-mm-dd"
    });
    $("#start-date").on("changeDate", function () {
        var date = $(this).datepicker("getFormattedDate");
        $("#start-date-input").val(date);
    });
});
