let json;
let pageSize = 10;
$(function () {
    $('.setPageDiv').change(function () {
        doPagination(parseInt($(this).val()))
    })
    getList({})
})

function getList(opt) {
    $.ajax({
        type: "post",
        url: "getFbData",
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
    html += '<td>' + data[i].group_id + '</td>'
    html += '<td>' + data[i].keyword + '</td>'
    html += '<td>' + data[i].nums + '</td>'
    html += '<td>' + data[i].share_num + '</td>'
    html += '<td>' + data[i].done_num + '</td>'
    if (data[i].state === "working") {
        html += '<td class="am-warning">进行中</td>'
    } else if (data[i].state === "finish") {
        html += '<td class="am-success">已完成</td>'
    } else {
        html += '<td>未知</td>'
    }
    html += '<td>' + new Date(data[i].add_time).Format("yyyy-MM-dd hh:mm:ss") + '</td>'
    if (data[i].finish_time) {
        html += '<td>' + new Date(data[i].finish_time).Format("yyyy-MM-dd hh:mm:ss") + '</td>'
    } else {
        html += '<td>无</td>'
    }
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
    let state = $('#state').val();
    let keyword = $('#keyword').val();
    let group_id = $('#group_id').val();
    console.log(keyword)
    let opt = {};
    if (state !== "none") {
        opt['state'] = state;
    }
    if (keyword) {
        opt['keyword'] = keyword;
    }
    if (group_id) {
        opt['group_id'] = group_id;
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