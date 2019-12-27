var choseModuleId = "";

$(function() {
    //展示树状菜单
	getTreeData("/sys/moduleTree");
	//查询节点用例列表
	loadCase()

	//树点击事件
	$('#jstree').on("changed.jstree", function (e, data) {
		if (data.selected == -1) {
			choseModuleId = "";
		} else {
			choseModuleId = data.selected[0] == "" || data.selected[0] == '0' ? '' : data.selected[0];
			search();
		}
	});
});


function loadCase() {
    $('#exampleTable').bootstrapTable(
            {
                method: 'get', // 服务器数据的请求方式 get or post
                url: "/interface/caseList", // 服务器数据的加载地址
                striped : true, // 设置为true会有隔行变色效果
                dataType : "json", // 服务器返回的数据类型
                pagination : true, // 设置为true会在底部显示分页条
                // queryParamsType : "limit",
                // //设置为limit则会发送符合RESTFull格式的参数
                singleSelect : false, // 设置为true将禁止多选
                iconSize : 'outline',
                toolbar : '#exampleToolbar',
                // contentType : "application/x-www-form-urlencoded",
                // //发送到服务器的数据编码类型
                pageSize : 10, // 如果设置了分页，每页数据条数
                pageNumber : 1, // 如果设置了分布，首页页码
                //search : true, // 是否显示搜索框
                //showColumns : true, // 是否显示内容下拉框（选择显示的列）
                sidePagination : "server", // 设置在哪里进行分页，可选值为"client" 或者
                undefinedText: '',
                queryParams: function (params) {
                    return {
                        //说明：传入后台的参数包括offset开始索引，limit步长，sort排序列，order：desc或者,以及所有列的键值对
						size: params.limit,                         //页面大小
						page: (params.offset / params.limit) + 1,   //页码
						run_flag : $('#run_flag').val(),
						builder : $('#builder').val(),
						case_name : $('#case_name').val(),
						case_no : $('#case_no').val(),
						moduleId : choseModuleId
                    };
                },
                columns: [{
						checkbox : true
					},
                    {
                        field: 'case_no',
						title: '用例编号',
                        align: 'center',
                    },
                    {
                        field: 'case_name',
                        title: '用例名称',
                        align: 'center',
                    },
                    {
                        field: 'case_description',
                        title: '用例描述',
                        align: 'center',
                    },
                    {
                        field: 'url',
                        title: '请求地址',
                        align: 'center',
                    },
                    {
                        field: 'request_method',
                        title: '请求方式',
                        align: 'center',
                    },
                    {
                        field: 'request_param',
                        title: '请求参数',
                        align: 'center',
                    },
                    {
                        field: 'run_flag',
                        title: '运行标志',
                        align: 'center',
                        formatter: function (value, row, index) {
                        	//保留两位小数显示
                            // return (value-0).toFixed(2).replace(/(\d)(?=(\d{3})+\.)/g, '$1,');
							if(row.run_flag==1){
								return  "启用"
							}else if(row.run_flag==0){
								return  "禁用"
							}
                        },
                    },
					{
                        field: 'builder',
                        title: '创建人',
                        align: 'center',
                    },
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-warning btn-sm '+s_edit_h+'" href="#" mce_href="#" title="编辑" onclick="edit(\''
									+ row.id
									+ '\')">编辑</a> ';
							var d = '<a class="btn btn-danger btn-sm '+s_remove_h+'" href="#" title="删除"  mce_href="#" onclick="remove(\''
									+ row.id
									+ '\')">删除</a> ';
							var f = '<a class="btn btn-primary btn-sm '+s_executee_h+'" href="#" title="执行"  mce_href="#" onclick="execute(\''
									+ row.id
									+ '\')">执行</a> ';
							return e + d + f;
						}
					}]
            }
    );
}


//添加用例
function add() {
	if(!choseModuleId){
		layer.alert("请选择模块节点");
		return;
	}
	layer.open({
		type : 2,
		title : '添加用例',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '80%', '90%' ],
		content : '/interface/caseAddPage?moduleId='+choseModuleId
	});
}


//编辑用例
function edit(id) {
	layer.open({
		type : 2,
		title : '编辑用例',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '80%', '90%' ],
		content : '/interface/caseEditPage?id='+ id
	});
}


//删除用例
function remove(id) {
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : "/interface/caseDelete",
			type : "post",
			data :{'id':id} ,
			success : function(r) {
				if (r.code === 0) {
					layer.msg("删除成功");
					search();
				} else {
					layer.msg("删除失败");
				}
			}
		});
	})
}


//执行用例
function execute(id){
		$.ajax({
			url : "/interface/caseExecute",
			type : "post",
			data :{'id':id} ,
			success : function(r) {
				if (r.code === 0) {
					layer.msg("用例执行通过");
				} else if(r.code === 1){
					layer.msg("用例执行未通过，实际结果为："+r.msg);
				} else{
					layer.msg("用例执行出现异常："+r.msg);
				}
			}
		});
}


function batchRemove() {
	var rows = $('#exampleTable').bootstrapTable('getSelections'); //返回所有选择的行，当没有选择的记录时，返回一个空数组
	if (rows.length == 0) {
		layer.msg("请选择要删除的数据");
		return;
	}
	layer.confirm("确认要删除选中的" + rows.length + "条数据吗?", {
		btn : [ '确定', '取消' ]
	}, function() {
		var ids = new Array();
		$.each(rows, function(i, row) {
			ids[i] = row['id'];
		});
		$.ajax({
			type : 'POST',
			traditional:true,			//不加这个,ajax会将结果后边加个[]
			data : {
				'ids' : ids
			},
			url :'/interface/caseBatchDelete',
			success : function(r) {
				if (r.code == 0) {
					layer.msg('删除成功');
					search();
				} else {
					layer.msg('删除失败');
				}
			}
		});
	}, function() {});
}


function getTreeData(requestUrl) {
    $('#jstree').jstree({
        'core': {
            'data': {
                "url": "/sys/moduleTree",
                "dataType": "json" // needed only if you do not supply JSON headers
            },
            "themes": {
                "dots": true,               // no connecting dots between dots
                "responsive": false        //无响应
            },
            'multiple': false,              //设置其为没有多选
            'check_callback': true,          //设置其true.可以进行文本的修改。
        },
        'types': {                         //这里就是图片的显示格式
            "default": {
                "icon": "fa fa-folder tree-item-icon-color icon-lg"
            },
            "file": {
                "icon": "fa fa-file tree-item-icon-color icon-lg"
            }
        },
        // "plugins": ["types", "contextmenu", "search", "wholerow", "sort"]
    }).on('loaded.jstree', function (e, data) {
        $('#jstree').jstree().open_all();  //展开所有节点
    });
}


function search() {
    $("#exampleTable").bootstrapTable('refresh',{pageNumber:1,moduleId:choseModuleId});
}
