let json, pageSize = 30,level
$(function () {
    $('.setPageDiv').change(function () {
        doPagination(parseInt($(this).val()))
    })
    getList({})
    level = $("#user_level").html()
})

function getList(opt) {
    $.ajax({
        type: "post",
        url: "getReviewData",
        dataType: "json",
        charset: "utf-8",
        contentType: "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            let html = "";
            json = d;
            let data = json.list;
            let for_num = pageSize;
            $("#total_num").html("总计"+data.length+"条,每页"+pageSize+"条")
            if (data.length < pageSize) {
                for_num = data.length;
                $('.searchPage').hide();
            }
            for (let i = 0; i < for_num; i++) {
                html = structureHtml(html, data, i)
            }
            $('#list-tbody').html(html)
            doPagination()
            checkedChange()
        }
    });
}

function showTips(msg,reload) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
    if(reload){
        getList()
    }
}

function doPagination() {
    let showNum = pageSize;
    let dataL = json.list.length;
    let data = json.list;
    let pageNum = Math.ceil(dataL / showNum);
    $('.allPage').html(pageNum);
    $('#Pagination').pagination(pageNum, {
        num_edge_entries: 1, //边缘页数
        num_display_entries: 4, //主体页数
        items_per_page: 1, //每页显示1项
        prev_text: "上一页",
        next_text: "下一页",
        callback: function (index) {
            let html = "";
            for (let i = showNum * index; i < showNum * index + showNum; i++) {
                if (i < dataL) {
                    html = structureHtml(html, data, i)
                }
            }
            $('#list-tbody').html(html)
            checkedChange()
        }
    })
}

function structureHtml(html, data, i) {
    let asin = data[i].asin.substr(0,10)
    html += '<tr class="gradeX">';
    html += '<td><img style="width: 6rem;height: 6rem;cursor:pointer;" src="'+(data[i].img?data[i].img:'')+'" onclick="openAmzPage(\''+asin+'\')" class="tpl-table-line-img" alt=""></td>'
    if(level === "1"){
        html += '<td>' + checkObj(data[i].nickname) + '</td>'
        let checked = ""
        if(data[i].status===1){
            checked = " checked"
        }
        html += '<td><div class="tpl-switch">' +
            '<input type="checkbox" style="margin-left: -2.5rem" data-id="' + data[i].id + '" class="ios-switch bigswitch tpl-switch-btn"'+checked+'>' +
            '<div class="tpl-switch-btn-view" style="margin: 0 auto"><div></div></div></div></td>'
        html += '<td><input type="text" onblur="discountChange(this)" data-id="' + data[i].id + '" style="font-size: 14px;width: 4rem;color: #838FA1;line-height: 1.6;text-align: center" value="'+checkObj(data[i].discount)+'"></td>'
    }
    html += '<td>' + checkObj(data[i].name) + '</td>'
    html += '<td>' + checkObj(data[i].keyword) + '</td>'
    html += '<td>' + checkObj(data[i].asin_str) + '</td>'
    html += '<td>' + checkObj(data[i].price) + '</td>'
    // html += '<td>' + checkObj(data[i].brand) + '</td>'
    html += '<td>' + checkObj(data[i].store) + '</td>'
    html += '<td style="text-align: center"><span style="color: red">' + data[i].done_num+'</span>/'+data[i].num+'/'+checkObj(data[i].total_order) +'<br>结/单/总</td>'
    html += '<td>' + checkObj(data[i].add_time_str) + '</td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation" onclick="showDetail(' + data[i].id + ',\''+asin+'\',\''+data[i].img+'\')"><i class="am-icon-bar-chart-o"></i> 进度</a></div></td>'
    html += '<tr/>'
    return html;
}

function showDetail(id,asin,img){
    let opt = {"task_id": id};
    $.ajax({
        type: "post",
        url: "getOrderData",
        dataType: "json",
        charset: "utf-8",
        contentType: "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            let dataList = d.list;
            getOrderData(dataList,asin,img)
        }
    });
    $("#order_modal").modal('open')
}

function discountChange(obj){
    let id = $(obj).data("id")
        if (id) {
            let opt = {"discount":$(obj).val(),"id":id}
            $.ajax({
                type: "post",
                url: "updateTaskDiscount",
                dataType: "json",
                charset: "utf-8",
                contentType: "application/json",
                data: JSON.stringify(opt),
                success: function (d) {
                    if(d.code !== "0000"){
                        alert(d.msg)
                    }
                }
            });
        }
}

function getOrderData(dataList,asin,img){
    let titleHtml = ""
    if (img && img !== "null"){
        titleHtml += '<img style="width: 6rem;height: 6rem;cursor:pointer;" id="order_img" src="'+img+'" class="tpl-table-line-img" alt="">'
    }
    titleHtml += '<span style="line-height: 6rem">'+asin+'</span><a href="javascript: void(0)" class="am-close am-close-spin" data-am-modal-close>&times;</a>'
    $("#order_title").html(titleHtml)
    let html = ""
    if(dataList.length === 0){
        html = "<tr><td colspan='7' style='text-align: center;line-height: 20rem'>暂无订单数据</td>></tr>>"
    }else{
        $.each(dataList,function (index,data){
            html += '<tr>'
            html += '<td>'+(index+1)+'</td>'
            html += '<td>'+data.order_id+'</td>'
            html += '<td>'+data.channel+'</td>'
            html += '<td>'+data.order_time_str+'</td>'
            html += '<td><div class="tpl-table-black-operation">' +
                        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" ' +
                        'onclick="window.open(\'' + data.profile + '\')"><i class="am-icon-amazon"></i> 跳转</a></div></td>'
            if(data.review_url) {
                html += '<td><div class="tpl-table-black-operation">' +
                    '<a href="javascript:void(0);" class="tpl-table-black-operation-del" ' +
                    'onclick="window.open(\'' + data.review_url + '\')"><i class="am-icon-amazon"></i> 跳转</a></div></td>'
            }else{
                html += '<td>暂无</td>'
            }
            html += '<td><div class="tpl-switch"><input type="checkbox" data-id="' + data.id + '" class="ios-switch bigswitch tpl-switch-btn"'+(data.status===1?' checked':'')+(level === "1"?'':' disabled')+'><div class="tpl-switch-btn-view" style="margin: 0"><div></div></div></div></td>'
            html += '</tr>'
        })
    }
    $("#order_tbody").html(html)
    checkedChange()
}

function openAmzPage(asin){
    window.open("https://www.amazon.com/dp/"+asin)
}

function goPage() {
    let index = $('#go_page').val() - 1, showNum = pageSize, dataL = json.list.length, data = json.list, html = "";
    for (let i = showNum * index; i < showNum * index + showNum; i++) {
        if (i < dataL) {
            html = structureHtml(html, data, i)
        }
    }
    $('#list-tbody').html(html)
    checkedChange()
}

function submitOpt() {
    let keyword = $('#keyword').val();
    let asin = $('#asin').val();
    let user_id = $("#user_select").val()
    let opt = {};
    if (keyword) {
        opt['keyword'] = keyword;
    }
    if (asin) {
        opt['asin'] = asin;
    }
    if (user_id && user_id!=="0"){
        opt['user_id'] = user_id;
    }
    getList(opt);
}

function checkedChange() {
    $("#order_tbody").find("input[type='checkbox']").on("change", function () {
        let id = $(this).data("id")
        if (id) {
            let opt = {"status":$(this).is(":checked")?1:0,"id":id}
            $.ajax({
                type: "post",
                url: "updateOrderStatus",
                dataType: "json",
                charset: "utf-8",
                contentType: "application/json",
                data: JSON.stringify(opt),
                success: function (d) {
                    if(d.code !== "0000"){
                        alert(d.msg)
                    }
                }
            });
        }
    })
    $("#list-tbody").find("input[type='checkbox']").on("change", function () {
        let id = $(this).data("id")
        if (id) {
            let opt = {"status":$(this).is(":checked")?1:0,"id":id}
            $.ajax({
                type: "post",
                url: "updateTaskStatus",
                dataType: "json",
                charset: "utf-8",
                contentType: "application/json",
                data: JSON.stringify(opt),
                success: function (d) {
                    // showTips(d.msg)
                }
            });
        }
    })
}

function checkObj(obj){
    if(obj && obj!==""){
        return obj
    }else{
        return "--"
    }
}