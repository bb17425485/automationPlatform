function showTips(msg, code) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
    if(code === "0000"){
        $('#fb-form')[0].reset();
    }
}

function postForm() {
    let opt = {}
    let groupList = [];
    $('input[name="group_id"]:checked').each(function(){
        groupList.push($(this).val());//向数组中添加元素
    })
    opt['group_id'] = groupList
    opt['keyword'] = $("[name='keyword']").val()
    opt['nums'] = $("[name='nums']").val()
    let share_num = $("[name='share_num']").val()
    opt['share_num'] = share_num?share_num:0
    $.ajax({
        type: "post",
        url: "form",
        dataType: "json",
        charset : "utf-8",
        contentType : "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            showTips(d.message,d.code);
        }
    });
}