let json, pageSize = 50,level
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
        url: "getGroundingData",
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
    html += '<td><img style="width: 6rem;height:3rem;cursor:pointer;" src="'+(data[i].img?data[i].img:'')+'" onclick="openAmzPage(\''+asin+'\')" class="tpl-table-line-img" alt=""></td>'
    html += '<td>' + checkObj(data[i].nickname) + '</td>'
    html += '<td>' + checkObj(data[i].task_id) + '</td>'
    html += '<td>' + checkObj(data[i].asin) + '</td>'
    html += '<td>' + checkObj(data[i].price) + '</td>'
    html += '<td>' + checkObj(data[i].put_time_str) + '</td>'
    if(data[i].task_status === 0){
        html += '<td class="am-warning">已停止</td>'
    }else{
        html += '<td class="am-success">执行中</td>'
    }
    let checked = ""
    if(data[i].status===1){
        checked = " checked"
    }
    html += '<td><div class="tpl-switch">' +
        '<input type="checkbox" style="margin-left: -2.5rem" data-id="' + data[i].id + '" class="ios-switch bigswitch tpl-switch-btn"'+checked+'>' +
        '<div class="tpl-switch-btn-view" style="margin: 0 auto"><div></div></div></div></td>'
    html += '<tr/>'
    return html;
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
    let asin = $('#asin').val();
    let task_id = $('#task_id').val();
    let task_status = $('#task_status').val();
    let order_status = $('#order_status').val();
    let opt = {};
    if (asin) {
        opt['asin'] = asin;
    }
    if (task_id) {
        opt['task_id'] = task_id;
    }
    if (task_status && task_status !== "99") {
        opt['task_status'] = task_status;
    }
    if (order_status && order_status !== "99") {
        opt['order_status'] = order_status;
    }
    getList(opt);
}

function checkedChange() {
    $("input[type='checkbox']").on("change", function () {
        let id = $(this).data("id")
        if (id) {
            let opt = {"status":$(this).is(":checked")?1:0,"id":id}
            $.ajax({
                type: "post",
                url: "updateAsinStatus",
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
}

function checkObj(obj){
    if(obj && obj!==""){
        return obj
    }else{
        return "--"
    }
}