var prefix = "/system/sysDept";
var choseSubhqcode = "";
var choseSubhqname = "";
var choseSubhqType = "";
$(function() {

	getTreeData("/sys/moduleTree");
	// loadTree2();
	load();
	//树点击事件
	$('#jstree').on("changed.jstree", function (e, data) {
		var opt = {};
		if (data.selected == -1) {
			choseSubhqcode = "";
			choseSubhqname = "";
			choseSubhqType= "";
		} else {
			choseSubhqcode = data.selected[0] == "" || data.selected[0] == '0' ? '' : data.selected[0];
			choseSubhqname = data.instance.get_node(data.selected[0]).state.nodeName;
			choseSubhqType = data.instance.get_node(data.selected[0]).state.nodeType;
		}
		opt = {
			query: {
				subhqcode: choseSubhqcode
			}
		};
		$('#exampleTable').bootstrapTable('refresh', opt);
	});
});

function load() {
	$('#exampleTable').bootstrapTable(
			{
				type : "GET", // 请求数据的ajax类型
				url : '/sys/listWithPage', // 请求数据的ajax的url
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
					return {
						limit: params.limit,
						offset: params.offset,
						nodekey: $('#nodeKey').val(),
						subhqcode: choseSubhqcode
					};
				},
				columns : [{
						title : '部门编码',
						field : 'nodecode',
						align : 'center',
						valign : 'center'
					},
					{
						title : '部门名称',
						field : 'nodename',
						align : 'center'
					},
					{
						title : "部门类型",
						field : "nodetypename",
						align : "center"
					},
					{
						title : "负责人",
						field : "deptleader",
						align : "center"
					},
					{
						title : "联系电话",
						field : "phonenum",
						align : "center"
					},
					{
						title : "经营面积",
						field : "area",
						align : "center"
					},
					{
						title : "员工人数",
						field : "employeecount",
						align : "center"
					},
					{
						title : "状态",
						field : "statename",
						align : "center"
					},
					{
						title : "更新时间",
						field : "lastmodifydate",
						align : "center"
					},
					{
						title : '操作',
						field : 'nodecode',
						align : 'center',
                        valign : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-primary btn-sm ' + s_edit_h + '" href="#" mce_href="#" title="编辑" onclick="edit(\''
								+ value
								+ '\')">编辑</a> ';
							var d = '<a class="btn btn-warning btn-sm '+s_remove_h+'" href="#" title="删除"  mce_href="#" onclick="remove(\''
								+ value
								+ '\')">删除</a> ';
							return e + d;
						}
					} ]
			});
}
function reLoad() {
	$('#exampleTable').bootstrapTable('refresh');
}
//添加分总部下部门
function add() {
	if(!choseSubhqcode){
		layer.alert("请选择父级模块");
		return;
	}
	layer.open({
		type : 2,
		title : '添加部门',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '80%', '90%' ],
		content : prefix + '/toAdd?subhqcode=' + choseSubhqcode + '&subhqname=' + choseSubhqname
	});
}
//添加一级菜单
function addSub() {
	layer.open({
		type : 2,
		title : '添加模块',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '80%', '90%' ],
		content : '/sys/moduleAddPage'
	});
}

//编辑一级菜单
function editSub() {
	if(!choseSubhqcode){
		layer.alert("请选择父级模块");
		return;
	}
	layer.open({
		type : 2,
		title : '编辑模块',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '80%', '90%' ],
		content : '/sys/moduleEditPage?id='+ choseSubhqcode
	});
}


function edit(nodecode) {
	layer.open({
		type : 2,
		title : '编辑部门',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [  '80%', '90%'],
		content : prefix + '/edit/' + nodecode
	});
}

function getTreeData(requestUrl) {
	$('#jstree').jstree({
		'core' : {
		  'data' : {
			"url" : "/sys/moduleTree",
			"dataType" : "json" // needed only if you do not supply JSON headers
		  }
		},
		"plugins": ["search"]
	});

	$('#jstree').jstree().open_all();

	// $.ajax({
	// 	type: "GET",
	// 	url: requestUrl,
	// 	success: function (tree) {
	// 		loadTree(tree);
	// 	}
	// });
}

function loadTree(tree) {
	$('#jstree').jstree({
		'core': {
			'data': tree
		},
		"plugins": ["search"]
	});

	$('#jstree').jstree().open_all();
}

function loadTree2() {
	$('#jstree').jstree({
		'core': {
			'data':{
				url:"/sys/moduleTree",
				dataFilter:function(data){
					console.log(data)
					return data;
				}
			}
		},
		strings:{
			'Loading....':'正在加载....'
		}
	});
	$('#jstree').jstree().open_all();
}

function reLoadTree(){
	$.ajax({
		type: "GET",
		url: prefix + '/userDeptTree',
		success: function (tree) {
			$('#jstree').jstree(true).settings.core.data=tree;
			$('#jstree').jstree(true).refresh()
		}
	});
}

function remove(nodeCode) {
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : prefix + "/remove/" + nodeCode,
			type : "post",
			success : function(r) {
				if (r.code === 0) {
					layer.msg("删除成功");
					reLoad();
				} else {
					layer.msg(r.msg);
				}
			}
		});
	})

}