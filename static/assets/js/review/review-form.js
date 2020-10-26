function showTips(msg, code) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
    if(code === "0000"){
        $("[name='keyword']").val("")
        $("[name='asin']").val("")
        $("[name='img']").val("")
    }
}

function postForm() {
    let keyword = $("[name='keyword']").val().trim()
    let kw_page = $("[name='kw_page']").val().trim()
    let name = $("[name='name']").val().trim()
    let user_id = $("[name='user_id']").val()
    let price = $("[name='price']").val().trim()
    let brand = $("[name='brand']").val().trim()
    let store = $("[name='store']").val().trim()
    let days_order = $("[name='days_order']").val().trim()
    let total_order = $("[name='total_order']").val().trim()
    let asin = $("[name='asin']").val().trim()
    let img = $("[name='img']").val().trim()
    let note = $("[name='note']").val().trim()
    if (!keyword){
        showTips("关键词不能为空")
        return false
    }
    if (!name){
        showTips("产品简写不能为空")
        return false
    }
    if (!kw_page){
        showTips("关键词页数不能为空")
        return false
    }
    if (!price){
        showTips("价格不能为空")
        return false
    }
    if (!brand){
        showTips("品牌名不能为空")
        return false
    }
    if (!store){
        showTips("店铺名不能为空")
        return false
    }
    if (!days_order){
        showTips("总单数不能为空")
        return false
    }
    if (!total_order){
        showTips("总单数不能为空")
        return false
    }
    if (!asin){
        showTips("ASIN不能为空")
        return false
    }
    if (!img){
        showTips("主图链接不能为空")
        return false
    }
    let opt = {"keyword":keyword,"kw_page":kw_page,"user_id":user_id,"price":price,"brand":brand,"store":store,
        "total_order":total_order,"asin":asin,"img":img,"days_order":days_order,"note":note,"name":name}
    $.ajax({
        type: "post",
        url: "reviewForm",
        dataType: "json",
        charset : "utf-8",
        contentType : "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            showTips(d.message,d.code);
        }
    });
}