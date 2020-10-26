let json, pageSize = 10, echarts_data = []
$(function () {
    $('.setPageDiv').change(function () {
        doPagination(parseInt($(this).val()))
    })
    getList({})
})

function getList(opt) {
    $.ajax({
        type: "post",
        url: "getTrackData",
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
            $('#list-tbody').html(html)
            updateBtnInit()
            doPagination()
        }
    });
}

function showTips(msg) {
    $('#tips_content').html(msg);
    $('#tips_modal').modal('toggle');
    getList()
}

function updateBtnInit() {
    $('#list-tbody').find('.cf_class').add('#doc-confirm-toggle').on('click', function () {
        $('#my_confirm').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                let $link = $(this.relatedTarget);
                let opt = {"state":$link.data('state'),"id":$link.data('id')}
                $.ajax({
                    type: "post",
                    url: "updateTrackState",
                    dataType: "json",
                    charset: "utf-8",
                    contentType: "application/json",
                    data: JSON.stringify(opt),
                    success: function (d) {
                        showTips(d.msg)
                    }
                });
            },
            onCancel: function () {
            }
        });
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
            updateBtnInit()
        }
    })
}

function structureHtml(html, data, i) {
    html += '<tr class="gradeX">';
    html += '<td><img style="width: 5rem" src="https://m.media-amazon.com/images/I/915Jnh4JIcL._AC_UL320_.jpg" class="tpl-table-line-img" alt=""></td>'
    html += '<td>' + data[i].keyword + '</td>'
    html += '<td>' + data[i].asin + '</td>'
    if (data[i].state === 1) {
        html += '<td class="am-success"><div class="tpl-table-black-operation"><a href="javascript:void(0);" data-id="' + data[i].pro_id + '" data-state="' + data[i].state + '" class="tpl-table-black-operation cf_class"><i class="am-icon-cog"></i> 进行中</a></div></td>'
    } else if (data[i].state === 0) {
        html += '<td class="am-warning"><div class="tpl-table-black-operation"><a href="javascript:void(0);" data-id="' + data[i].pro_id + '" data-state="' + data[i].state + '" class="tpl-table-black-operation-del cf_class"><i class="am-icon-cog"></i> 已停止</a></div></td>'
    } else {
        html += '<td>未知</td>'
    }
    html += '<td>' + data[i].rank + '</td>'
    html += '<td>' + data[i].review + '</td>'
    html += '<td>' + data[i].big_rank_txt + '</td>'
    html += '<td>' + data[i].update_time + '</td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation" onclick="showEcharts(' + data[i].pro_id + ',\'' + data[i].keyword + '\',\'' + data[i].asin + '\')"><i class="am-icon-bar-chart-o"></i> 详情</a></div></td>'
    html += '<tr/>'
    return html;
}

function showEcharts(id, keyword, asin) {
    let opt = {"pro_id": id};
    $.ajax({
        type: "post",
        url: "getDataByProId",
        dataType: "json",
        charset: "utf-8",
        contentType: "application/json",
        data: JSON.stringify(opt),
        success: function (d) {
            let html = "";
            let data = d.list;
            echarts_data = data
            getProData(data, keyword, asin)
            getCharts("rank")
        }
    });
    $("#charts_modal").modal('open')
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
    let state = $('#state').val();
    let keyword = $('#keyword').val();
    let asin = $('#asin').val();
    let opt = {};
    if (state !== "none") {
        opt['state'] = state;
    }
    if (keyword) {
        opt['keyword'] = keyword;
    }
    if (asin) {
        opt['asin'] = asin;
    }
    getList(opt);
}

function getProData(data, keyword, asin) {
    let pro_data = data[data.length - 1]
    $("#echarts_title").html(keyword + " - " + asin)
    let html = '<tr>'
    html += '<td onclick="getCharts(\'rank\')">' + pro_data['rank'] + ' (第' + pro_data['page_num'] + '页)' + '</td>'
    html += '<td onclick="getCharts(\'big_rank\')">' + pro_data['big_rank_txt'] + '</td>'
    html += '<td onclick="getCharts(\'review\')">' + pro_data['review'] + '</td>'
    html += '<td onclick="getCharts(\'price\')">' + pro_data['price'] + '</td>'
    html += '<td onclick="getCharts(\'star\')">' + pro_data['star'] + '</td>'
    html += '</tr><tr>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" onclick="getCharts(\'rank\')"><i class="am-icon-bar-chart-o"></i> 关键词趋势</a></div></td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" onclick="getCharts(\'big_rank\')"><i class="am-icon-bar-chart-o"></i> 大类趋势</a></div></td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" onclick="getCharts(\'review\')"><i class="am-icon-bar-chart-o"></i> 评论趋势</a></div></td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" onclick="getCharts(\'price\')"><i class="am-icon-bar-chart-o"></i> 价格趋势</a></div></td>'
    html += '<td><div class="tpl-table-black-operation">' +
        '<a href="javascript:void(0);" class="tpl-table-black-operation-del" onclick="getCharts(\'star\')"><i class="am-icon-bar-chart-o"></i> 星级趋势</a></div></td>'
    html += '</tr>'
    $('#echarts_tbody').html(html)
}

function getCharts(type) {
    let x_data = [], y_data = []
    let name = "", inverse = false
    if (type === "rank") {
        name = "关键词排名"
        inverse = true
    } else if (type === "big_rank") {
        name = "大类排名"
        inverse = true
    } else if (type === "review") {
        name = "评论数"
    } else if (type === "price") {
        name = "价格"
    } else if (type === "star") {
        name = "星级"
    }
    $.each(echarts_data, function (i, v) {
        x_data.push(v['update_time'])
        y_data.push(v[type])
    })
    let echartsA = echarts.init(document.getElementById('tpl_echarts'));
    let option = {
        title: {
            text: name,
            left: 'center'
        },
        tooltip: {
            trigger: 'axis'
        },
        grid: {
            top: '3%',
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            boundaryGap: false,
            data: x_data,
            axisLine: false
        }],
        yAxis: [{
            inverse: inverse,
            type: 'value',
            splitNumber: 4,
            min: 'dataMin',
            max: 'dataMax'
        }],
        textStyle: {
            color: '#838FA1'
        },
        series: [{
            name: name,
            type: 'line',
            data: y_data,
            itemStyle: {
                normal: {
                    color: '#1cabdb',
                    borderColor: '#1cabdb',
                    borderWidth: '2',
                    borderType: 'solid',
                    opacity: '1'
                },
                emphasis: {}
            }
        }]
    };
    echartsA.setOption(option);
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