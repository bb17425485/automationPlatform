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
        url: "getUserData",
        dataType: "json",
        charset: "utf-8",
        contentType: "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            let html = "";
            json = d;
            let data = json.list;
            let for_num = pageSize;
            if (data.length < pageSize) {
                for_num = data.length;
                $('.searchPage').hide();
            }
            for (let i = 0; i < for_num; i++) {
                html = structureHtml(html, data, i)
            }
            $('#list-tbody').html(html).trigger("create")
            selectOnChange()
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
            $('#list-tbody').html(html).trigger("create")
            selectOnChange()
        }
    })
}

function structureHtml(html, data, i) {
    html += '<tr class="gradeX">';
    html += '<td>' + data[i].id + '</td>'
    html += '<td>' + data[i].account + '</td>'
    html += '<td>' + data[i].nickname + '</td>'
    if (data[i].level === 1) {
        html += '<td>管理员</td>'
    } else if (data[i].level === 2) {
        html += '<td>平台用户</td>'
    }
    html += '<td><select class="state_select" style="font-size: 1.5rem" data-id="' + data[i].id + '" data-am-selected="{btnSize: \'sm\'}"><option value="none">选择状态</option>'
    if (data[i].state === 1) {
        html += '<option value="1" selected>正常</option><option value="2">待审核</option><option value="3">停用</option>'
    } else if (data[i].state === 2) {
        html += '<option value="1">正常</option><option value="2" selected>待审核</option><option value="3">停用</option>'
    } else if (data[i].state === 3) {
        html += '<option value="1">正常</option><option value="2">待审核</option><option value="3" selected>停用</option>'
    }
    html += '</select></div></div></td>'
    html += '<td>' + data[i].reg_time + '</td>'
    html += '<td>' + data[i].login_time + '</td>'
    html += '<tr/>'
    return html;
}

function selectOnChange() {
    $('.state_select').on("change", function () {
        let id = $(this).data("id")
        if (id) {
            let opt = {"state":$(this).find(':selected').val(),"id":id}
            $.ajax({
                type: "post",
                url: "updateUser",
                dataType: "json",
                charset: "utf-8",
                contentType: "application/json",
                data: JSON.stringify(opt),
                success: function (d) {
                    showTips(d.msg)
                }
            });
        }
    })
}

function showTips(msg) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
    getList()
}

function goPage() {
    let index = $('#go_page').val() - 1, showNum = pageSize, dataL = json.list.length, data = json.list, html = "";
    for (let i = showNum * index; i < showNum * index + showNum; i++) {
        if (i < dataL) {
            html = structureHtml(html, data, i)
        }
    }
    $('#list-tbody').html(html).trigger("create")
    selectOnChange()
}

function addUser() {
    $(".am-modal-prompt-input").val("")
    $('#user_prompt').modal({
        relatedTarget: this,
        onConfirm: function (e) {
            if(!e.data[0]){
                showTips("帐号不能为空")
            }else if(!e.data[1]){
                showTips("昵称不能为空")
            }else if(!e.data[2]){
                showTips("密码不能为空")
            }else{
                let level = $("#add_user_level").val()
                let opt = {"account":e.data[0],"nickname":e.data[1],"password":e.data[2],"level":level}
                $.ajax({
                    type: "post",
                    url: "addUser",
                    dataType: "json",
                    charset: "utf-8",
                    contentType: "application/json",
                    data: JSON.stringify(opt),
                    success: function (d) {
                        showTips(d.msg)
                        getList()
                    }
                });
            }
        }
    });
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