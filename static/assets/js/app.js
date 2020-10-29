$(function () {
    autoLeftNav();
    $(window).resize(function () {
        autoLeftNav();
    });
})
// 风格切换
$('.tpl-skiner-toggle').on('click', function () {
    $('.tpl-skiner').toggleClass('active');
})

$('.tpl-skiner-content-bar').find('span').on('click', function () {
    $('body').attr('class', $(this).attr('data-color'))
    saveSelectColor.Color = $(this).attr('data-color');
    // 保存选择项
    storageSave(saveSelectColor);

})

// 侧边菜单开关
function autoLeftNav() {
    $('.tpl-header-switch-button').on('click', function () {
        if ($('.left-sidebar').is('.active')) {
            if ($(window).width() > 1024) {
                $('.tpl-content-wrapper').removeClass('active');
            }
            $('.left-sidebar').removeClass('active');
        } else {

            $('.left-sidebar').addClass('active');
            if ($(window).width() > 1024) {
                $('.tpl-content-wrapper').addClass('active');
            }
        }
    })

    if ($(window).width() < 1024) {
        $('.left-sidebar').addClass('active');
    } else {
        $('.left-sidebar').removeClass('active');
    }
}

// 侧边菜单
$('.sidebar-nav-sub-title').on('click', function () {
    $(this).siblings('.sidebar-nav-sub').slideToggle(80)
        .end()
        .find('.sidebar-nav-sub-ico').toggleClass('sidebar-nav-sub-ico-rotate');
})

function updatePassword() {
    $('#psw_prompt').modal({
        relatedTarget: this,
        onConfirm: function (e) {
            if (!e.data[0]) {
                showSysTips("原密码不能为空")
            } else if (!e.data[1]) {
                showSysTips("新密码不能为空")
            } else if (!e.data[2]) {
                showSysTips("确认密码不能为空")
            } else if (e.data[1] !== e.data[2]) {
                showSysTips("确认密码不一致")
            } else {
                let opt = {"old_psw": e.data[0], "new_psw": e.data[1]}
                $.ajax({
                    type: "post",
                    url: "/updatePassword",
                    dataType: "json",
                    charset: "utf-8",
                    contentType: "application/json",
                    data: JSON.stringify(opt),
                    success: function (d) {
                        showSysTips(d.msg)
                    }
                });
            }
        }
    });
}

function showSysTips(msg) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
}