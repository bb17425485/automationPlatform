let json;
let pageSize = 30;
$(function () {
    $('.setPageDiv').change(function () {
        doPagination(parseInt($(this).val()))
    })
    getList({})
})

function getList(opt) {
    $.ajax({
        type: "post",
        url: "getGroupData",
        dataType: "json",
        charset: "utf-8",
        contentType: "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            let html = "";
            json = d;
            let data = json.list;
            let for_num = pageSize;
            if(data.length < pageSize){
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
    html += '<tr class="gradeX">';
    html += '<td>' + data[i].name + '</td>'
    html += '<td>' + data[i].admins + '</td>'
    html += '<td>' + data[i].nums + '</td>'
    if (data[i].type === 0) {
        html += '<td>公开</td>'
    } else if (data[i].type === 1) {
        html += '<td>非公开</td>'
    } else {
        html += '<td>未知</td>'
    }
    html += '<td>' + new Date(data[i].add_time).Format("yyyy-MM-dd hh:mm:ss") + '</td>'
    html += '<tr/>'
    return html;
}

function goPage(){
    let index = $('#go_page').val() - 1, showNum = pageSize, dataL = json.list.length, data = json.list, html = "";
    for (let i = showNum * index; i < showNum * index + showNum; i++) {
        if (i < dataL) {
            html = structureHtml(html, data, i)
        }
    }
    $('#list-tbody').html(html)
}

function submitOpt() {
    let type = $('#group_type').val();
    let name = $('#group_name').val();
    let bigNum = $('#big_num').val();
    let smallNum = $('#small_num').val();
    let opt = {};
    if (type !== "none") {
        opt['type'] = type;
    }
    if (name) {
        opt['name'] = name;
    }
    if (bigNum) {
        opt['bigNum'] = bigNum;
    }
    if (smallNum) {
        opt['smallNum'] = smallNum;
    }
    getList(opt);
}

Date.prototype.Format = function (fmt) {
    let o = {
        "M+": this.getMonth() + 1, //月份
        "d+": this.getDate(), //日
        "h+": this.getHours(), //小时
        "m+": this.getMinutes(), //分
        "s+": this.getSeconds(), //秒
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度
        "S": this.getMilliseconds() //毫秒
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (let k in o) {
        if (new RegExp("(" + k + ")").test(fmt)) {
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
        }
    }
    return fmt;
}