let json, pageSize = 30
$(function () {
    $('.setPageDiv').change(function () {
        doPagination(parseInt($(this).val()))
    })
    getList({})
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
        }
    })
}

function structureHtml(html, data, i) {
    let level = $("#user_level").html()
    let asin = data[i].asin.substr(0,10)
    html += '<tr class="gradeX">';
    html += '<td><img style="width: 6rem;height: 6rem;cursor:pointer;" src="'+data[i].img+'" onclick="openAmzPage(\''+asin+'\')" class="tpl-table-line-img" alt=""></td>'
    if(level === "1"){
        html += '<td>' + checkObj(data[i].nickname) + '</td>'
    }
    html += '<td>' + checkObj(data[i].name) + '</td>'
    html += '<td>' + checkObj(data[i].keyword) + '</td>'
    html += '<td>' + checkObj(data[i].asin.replaceAll("|"," ")) + '</td>'
    html += '<td>' + checkObj(data[i].price) + '</td>'
    html += '<td>' + checkObj(data[i].brand) + '</td>'
    html += '<td>' + checkObj(data[i].store) + '</td>'
    html += '<td style="text-align: center">' + data[i].num+'/'+checkObj(data[i].total_order) +'</td>'
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

function getOrderData(dataList,asin,img){
    $("#order_img").attr("src",img)
    $("#order_asin").html(" — "+asin)
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
            html += '<td><div class="tpl-switch"><input type="checkbox" data-id="' + data.id + '" class="ios-switch bigswitch tpl-switch-btn"'+(data.state===1?' checked':'')+'><div class="tpl-switch-btn-view" style="margin: 0"><div></div></div></div></td>'
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
    updateBtnInit()
}

function submitOpt() {
    let keyword = $('#keyword').val();
    let asin = $('#asin').val();
    let opt = {};
    if (keyword) {
        opt['keyword'] = keyword;
    }
    if (asin) {
        opt['asin'] = asin;
    }
    getList(opt);
}

function checkedChange() {
    $("input[type='checkbox']").on("change", function () {
        let id = $(this).data("id")
        if (id) {
            let opt = {"state":$(this).is(":checked")?1:0,"id":id}
            $.ajax({
                type: "post",
                url: "updateOrderState",
                dataType: "json",
                charset: "utf-8",
                contentType: "application/json",
                data: JSON.stringify(opt),
                success: function (d) {
                    alert(d.msg)
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