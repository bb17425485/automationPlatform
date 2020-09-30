let json;
let pageSize = 5;
$(function () {
    $('.setPageDiv').change(function () {
        doPagination(parseInt($(this).val()))
    })

    getList({})
})

function fileUpload() {
    let fileObj = document.getElementById("fileUpload").files[0]; // js 获取文件对象
    let formFile = new FormData();
    formFile.append("file", fileObj); //加入文件对象

    $.ajax({
        url: "fileUpload",
        data: formFile,
        type: "Post",
        dataType: "json",
        cache: false,//上传文件无需缓存
        processData: false,//用于对data参数进行序列化处理 这里必须false
        contentType: false, //必须
        success: function (d) {
            if (d.code === "0000") {
                showTips("批量新增评论成功！")
                getList()
            } else {
                alert("新增失败！")
            }
        },
    })
}

function getList(opt) {
    $.ajax({
        type: "post",
        url: "getAccountData",
        dataType: "json",
        charset: "utf-8",
        contentType: "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            let html = "";
            json = d;
            let data = json.list;
            let dataL = Object.keys(json.list).length;
            let for_num = pageSize;
            if (dataL < pageSize) {
                for_num = dataL;
                $('.searchPage').hide();
            }
            let num = 0
            $.each(data,function (i,v){
                if (for_num > num && num >= 0){
                    html = structureHtml(html, v, i)
                }
                num += 1
            })
            $('#account_list').html(html)
            doPagination()
        }
    });
}

function doPagination() {
    let showNum = pageSize;
    let dataL = Object.keys(json.list).length;
    // let dataL = json.list.length;
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
            let num = 0
            $.each(data,function (i,v){
                if (showNum * index + showNum > num && num >= showNum * index){
                    html = structureHtml(html, v, i)
                }
                num += 1
            })

            // for (let i = showNum * index; i < showNum * index + showNum; i++) {
            //     if (i < dataL) {
            //         html = structureHtml(html, data, i)
            //     }
            // }
            $('#account_list').html(html)
        }
    })
}

function structureHtml(html, data, i) {
    if (i % 2 === 0) {
        html += '<tr class="even gradeC">';
    } else {
        html += '<tr class="gradeX">';
    }
    html += '<td>' + i + '</td>'
    html += '<td>' + data.pwd + '</td>'
    if(data['user-agent'].length > 0){
        html += '<td style="color: green">已生成</td>'
    }else{
        html += '<td style="color: red">未生成</td>'
    }
    if(data['cookies'].length > 0){
        html += '<td style="color: green">已生成</td>'
    }else{
        html += '<td style="color: red">未生成</td>'
    }
    html += '<td>未知</td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" onclick="deleteComment(' + i + ')"><i class="am-icon-trash"></i> 删除</a></div></td>'
    html += '<tr/>'
    return html;
}

function goPage(){
    let index = $('#go_page').val()-1
    let showNum = pageSize;
    let data = json.list;
    let html = "",num = 0;
    $.each(data,function (i,v){
        if (showNum * index + showNum > num && num >= showNum * index){
            html = structureHtml(html, v, i)
        }
        num += 1
    })
    $('#account_list').html(html)
}

function showTips(content) {
    $("#tips_content").html(content)
    $("#tips_modal").modal('toggle')
}

function addComment() {
    $('#my-prompt').modal({
        relatedTarget: this,
        onConfirm: function (e) {
            if (e.data === "") {
                alert("评论不能为空")
            } else {
                let opt = {}
                opt['content'] = e.data;
                $.ajax({
                    type: "post",
                    url: "addComment",
                    dataType: "json",
                    charset: "utf-8",
                    contentType: "application/json",
                    data: JSON.stringify(opt),
                    success: function (d) {
                        if (d.code === "0000") {
                            showTips("新增评论成功！")
                            getList()
                        } else {
                            alert("新增失败！")
                        }
                    }
                });
            }
        }
    });
}

function deleteComment(id) {
    let con = confirm("确认删除吗")
    let opt = {'id':id}
    if (con) {
        $.ajax({
            type: "post",
            url: "deleteComment",
            dataType: "json",
            charset: "utf-8",
            contentType: "application/json",
            data: JSON.stringify(opt),
            success: function (d) {
                if (d.code === "0000") {
                    showTips("评论删除成功！")
                    getList()
                } else {
                    alert("删除失败！")
                }
            }
        });
    } else {
        showTips("评论删除失败！")
    }
}

function submitOpt() {
    // let content = $('#content').val();
    // let opt = {"start":"1"}
    // if(content === "1"){
    //     opt = {"stop":"1"}
    //     $.ajax({
    //         type: "post",
    //         url: "stopThread",
    //         dataType: "json",
    //         charset: "utf-8",
    //         contentType: "application/json",
    //         data: JSON.stringify(opt),
    //         success: function (d) {
    //
    //         }
    //     });
    // }else{
    //     $.ajax({
    //         type: "post",
    //         url: "doThread",
    //         dataType: "json",
    //         charset: "utf-8",
    //         contentType: "application/json",
    //         data: JSON.stringify(opt),
    //         success: function (d) {
    //
    //         }
    //     });
    // }

    let content = $('#content').val();
    let opt = {};
    if (content) {
        opt['content'] = content;
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