function showTips(msg, code) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
    if(code === "0000"){
        $('#fb-form')[0].reset();
    }
}

function postForm() {
    let opt = {}
    opt['keyword'] = $("[name='keyword']").val()
    opt['asin'] = $("[name='asin']").val()
    let page_size = $("[name='page_size']").val()
    opt['page_size'] = page_size?page_size:0
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