var prefix = "/sys/user";
var layerIdx = 0;

$(function () {
    initDatePlugin();
    $("#usersource").trigger('change');
});

function initDatePlugin() {
    var timeConf = {
        language: "zh-CN",
        autoclose: true,
        clearBtn: true,
        format: "yyyymmdd"
    };
    $("#startTime").datepicker(timeConf);
    $("#endTime").datepicker(timeConf);
    $("#validTime").datepicker(timeConf);
}

$("#usersource").on('change', function () {
    let todeptcode = '';
    var usersource = $("#usersource").val();
    $('#jstree').data('jstree', false).empty();
    $('#jstree').unbind();
    if (usersource == 0) {
        getTreeData(prefix + "/deptTee");
    } else if (usersource == 1) {
        getTreeData("/system/supplier/tree");
    }
    load(todeptcode);
});

$('#myModal').on('show.bs.modal', function () {
    $("#validTime").val('');
    var rows = $('#exampleTable').bootstrapTable('getSelections');
    if (rows.length == 0) {
        layer.msg("请选择要设置的职员");
        return false;
    }
});

function submitValidTime() {
    if (!$("#validTime").val()) {
        layer.msg("请选择有效时间");
        return false;
    }
    var rows = $('#exampleTable').bootstrapTable('getSelections'); // 返回所有选择的行，当没有选择的记录时，返回一个空数组
    var ids = new Array();
    $.each(rows, function (i, row) {
        ids[i] = row['employeecode'];
    });
    $.ajax({
        type: 'POST',
        data: {
            "ids": ids,
            "validTime": $("#validTime").val()
        },
        url: prefix + '/batchUpdateValidTime',
        success: function (r) {
            if (r.code == 0) {
                layer.msg(r.msg);
                reLoad();
                $("#myModal").modal('hide');
            } else {
                layer.msg(r.msg);
            }
        }
    });
}

function load(todeptcode) {
    $('#exampleTable')
        .bootstrapTable(
            {
                method: 'get', // 服务器数据的请求方式 get or post
                url: prefix + "/list", // 服务器数据的加载地址
                iconSize: 'outline',
                toolbar: '#exampleToolbar',
                striped: true, // 设置为true会有隔行变色效果
                dataType: "json", // 服务器返回的数据类型
                pagination: true, // 设置为true会在底部显示分页条
                singleSelect: false, // 设置为true将禁止多选
                pageSize: 10, // 如果设置了分页，每页数据条数
                pageNumber: 1, // 如果设置了分布，首页页码
                showColumns: false, // 是否显示内容下拉框（选择显示的列）
                sidePagination: "server", // 设置在哪里进行分页，可选值为"client" 或者
                undefinedText: '',
                queryParams: function (params) {
                    var condition1 = $("#startTime").val() && $("#endTime").val();
                    var condition2 = !$("#startTime").val() && !$("#endTime").val();
                    if (condition1 || condition2) {
                        if ($("#startTime").val() > $("#endTime").val()) {
                            layer.msg("结束时间不能小于开始时间");
                            return false;
                        } else {
                            return {
                                limit: params.limit,
                                offset: params.offset,
                                name: $('#searchName').val(),
                                todeptcode: todeptcode,
                                deptCode: $("#deptCode").val(),
                                usersource: $("#usersource").val(),
                                startTime: $("#startTime").val(),
                                endTime: $("#endTime").val()
                            };
                        }
                    } else {
                        layer.msg("开始日期、结束日期必须同时选择或同时缺省");
                        return false;
                    }
                },
                columns: [
                    {
                        checkbox: true
                    },
                    {
                        field: 'employeecode',
                        title: '编码',
                        align: 'center',
                    },
                    {
                        field: 'employeename',
                        title: '名称',
                        align: 'center',
                    },
                    // {
                    //     field: 'cardid',
                    //     title: '身份证号码',
                    //     align: 'center',
                    // },
                    // {
                    //     field: 'telephone',
                    //     title: '电话',
                    //     align: 'center',
                    // },
                    // {
                    //     field: 'email',
                    //     title: '邮箱',
                    //     align: 'center',
                    // },
                    // {
                    //     field: 'address',
                    //     title: '地址',
                    //     align: 'center',
                    // },
                    {
                        field: 'maturedate',
                        title: '有效时间',
                        align: 'center',
                    },
                    {
                        field: 'isused',
                        title: '状态',
                        align: 'center',
                        formatter: function (value, row, index) {
                            if (value == '0') {
                                return '<span class="label label-danger">禁用</span>';
                            } else if (value == '1') {
                                return '<span class="label label-primary">正常</span>';
                            }
                        }
                    },
                    {
                        field: 'todeptcode',
                        title: '所属组织编码',
                        align: 'center',
                    },
                    {
                        field: 'todeptname',
                        title: '所属组织名称',
                        align: 'center',
                    },
                    {
                        title: '操作',
                        field: 'id',
                        align: 'center',
                        formatter: function (value, row, index) {
                            var e = '<a  class="btn btn-primary btn-sm ' + s_edit_h + '" href="#" mce_href="#" title="编辑" onclick="edit(\''
                                + row.employeecode
                                + '\')">编辑</i></a> ';
                            var d = '<a class="btn btn-warning btn-sm ' + s_remove_h + '" href="#" title="删除"  mce_href="#" onclick="remove(\''
                                + row.employeecode
                                + '\')">删除</a> ';
                            var f = '<a class="btn btn-success btn-sm ' + s_resetPwd_h + '" href="#" title="重置密码"  mce_href="#" onclick="resetPwd(\''
                                + row.employeecode
                                + '\')">重置密码</a> ';
                            var g = '<a class="btn btn-success btn-sm ' + s_allocation_h + '" href="#"  mce_href="#" onclick=\'allocation('
                                + JSON.stringify(row)
                                + ')\'>分管</a> ';
                            return e + d + f + g;
                        }
                    }]
            });
}

function reLoad() {
    // if ($('#jstree').jstree(true).get_selected(true).length > 0) {
    //     var treeNode = $('#jstree').jstree(true).get_selected(true)[0];
    //     var dept_list = '';
    //     if ($('#jstree').jstree().is_parent(treeNode.id)) {
    //         if (!treeNode.children.length) {
    //             return;
    //         }
    //         $.each(treeNode.children, function (index, value) {
    //             dept_list += value + ","
    //         });
    //         dept_list = dept_list.slice(0, dept_list.length - 1);
    //     } else {
    //         dept_list = treeNode.id;
    //     }
    //     let opt = {
    //         query: {
    //             todeptcode: $("#deptCode").val(), usersource: $("#usersource").val(),
    //             pageNumber: 1
    //         }
    //     };
    //     $('#exampleTable').bootstrapTable('refreshOptions', {pageNumber: 1});
    //     $('#exampleTable').bootstrapTable('refresh', opt);
    // } else {
    // if ($('#jstree').jstree(true).get_selected(true).length > 0) {
    //     var treeNode = $('#jstree').jstree(true).get_selected(true)[0]
    // }
    let opt = {
        query: {
            todeptcode: '',
            usersource: $("#usersource").val(),
            deptCode: $("#deptCode").val(),
            pageNumber: 1
        }
    };
    $('#exampleTable').bootstrapTable('refresh', opt);

}

//添加用户
function add() {
    layerIdx = layer.open({
        type: 2,
        title: '增加用户',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['100%', '100%'],
		content:'useradd.html'
        //content: prefix + '/add'
    });
};

//删除用户
function remove(employeecode) {
    layer.confirm('确定要删除选中的记录？', {
        btn: ['确定', '取消']
    }, function () {
        $.ajax({
            url: "/sys/user/remove",
            type: "post",
            data: {
                'employeecode': employeecode
            },
            success: function (r) {
                if (r.code == 0) {
                    layer.msg(r.msg);
                    reLoad();
                } else {
                    layer.msg(r.msg);
                }
            }
        });
    })
}

//编辑
function edit(employeecode) {
    layerIdx = layer.open({
        type: 2,
        title: '职员信息修改',
        maxmin: true,
        shadeClose: false,
        area: ['100%', '100%'],
        content: prefix + '/edit/' + employeecode
    });
}

//重置密码
function resetPwd(id) {
    layerIdx = layer.open({
        type: 2,
        title: '重置密码',
        maxmin: true,
        shadeClose: false,
        area: ['400px', '260px'],
        content: prefix + '/resetPwd/' + id
    });
}

// 分管权限
function allocation(user) {
    if (user.usersource == 0) {
        layerIdx = layer.open({
            type: 2,
            title: '分管',
            maxmin: true,
            shadeClose: false,
            area: ['100%', '100%'],
            content: prefix + '/allocation?employeeCode=' + user.employeecode + "&userSource=" + user.usersource
        });
    } else if (user.usersource == 1) {
        layerIdx = layer.open({
            type: 2,
            title: '供应商分管',
            maxmin: true,
            shadeClose: false,
            area: ['100%', '100%'],
            content: prefix + '/supplierAllocation?employeeCode=' + user.employeecode + "&supplierCode=" + user.todeptcode
        });
    }

}

function batchRemove() {
    var rows = $('#exampleTable').bootstrapTable('getSelections'); // 返回所有选择的行，当没有选择的记录时，返回一个空数组
    if (rows.length == 0) {
        layer.msg("请选择要删除的数据");
        return;
    }
    layer.confirm("确认要删除选中的" + rows.length + "条数据吗?", {
        btn: ['确定', '取消']
    }, function () {
        var ids = new Array();
        $.each(rows, function (i, row) {
            ids[i] = row['employeecode'];
        });
        $.ajax({
            type: 'POST',
            data: {
                "ids": ids
            },
            url: prefix + '/batchRemove',
            success: function (r) {
                if (r.code == 0) {
                    layer.msg(r.msg);
                    reLoad();
                } else {
                    layer.msg(r.msg);
                }
            }
        });
    }, function () {
    });
}

function getTreeData(requestUrl) {
    $.ajax({
        type: "GET",
        url: requestUrl,
        success: function (tree) {
            loadTree(tree);
        }
    });
}

function loadTree(tree) {
    $('#jstree').jstree({
        'core': {
            'data': tree
        },
        "plugins": ["search"]
    });
    $('#jstree').jstree().open_all();
    let opt = {
        query: {
            todeptcode: '', usersource: $("#usersource").val()
        }
    };
    $('#exampleTable').bootstrapTable('refresh', opt);
    $('#jstree').bind("changed.jstree", function (e, data) {
        initTreeEvent(data);
    });
}

function getDeptList(data) {
    var dept_list = "";
    if ($('#jstree').jstree().is_parent(data.node.id)) {
        if (!data.node.children.length) {
            return;
        }
        $.each(data.node.children, function (index, value) {
            dept_list += value + ","
        });
        dept_list = dept_list.slice(0, dept_list.length - 1);
    } else {
        dept_list = data.node.id;
    }
    return dept_list;
}

/**
 * 初始化树节点change事件
 * @param data
 */
function initTreeEvent(data) {
    console.log(data);
    var usersource = $("#usersource").val();
    var opt = {};
    var dept_list = getDeptList(data);
    if (data.selected == -1) {
        opt = {
            query: {
                todeptcode: '',
                usersource: usersource
            }
        };
    } else {
        if (usersource == 1) {
            opt = {
                query: {
                    deptCode: "",
                    todeptcode: data.node.id,
                    usersource: usersource,
                    nodeType: data.node.state.nodeType
                }
            }
        } else {
            opt = {
                query: {
                    deptCode: "",
                    todeptcode: data.node.id,
                    usersource: usersource
                }
            };
        }

    }
    $('#exampleTable').bootstrapTable('refresh', opt);
}

var closeLayer = function () {
    layer.close(layerIdx);
};