//获取查询条件值，以及带上分页条件
var queryParams = function (params) {
	var module_number=$("#module_number").val();
    var module_name=$("#module_name").val();
    var module_type=$("#module_type").val();
    var query_params={
        module_name:module_name,
        module_type:module_type,
		module_number:module_number,
		size: params.limit,                         //页面大小
		page: (params.offset / params.limit) + 1,   //页码
    }
    return  query_params
};

//默认加载列表
$(function() {
	$('#exampleTable').bootstrapTable(
		{
			method : 'get', // 服务器数据的请求方式 get or post
			url : "/sys/moduleList", // 服务器数据的加载地址
			striped : true, // 设置为true会有隔行变色效果
			cache:false,
			dataType : "json", // 服务器返回的数据类型
			pagination : true, // 设置为true会在底部显示分页条
			// queryParamsType : "limit",
			// //设置为limit则会发送符合RESTFull格式的参数
			singleSelect : false, // 设置为true将禁止多选
			iconSize : 'outline',
			toolbar : '#exampleToolbar',//添加工具栏按钮
			// contentType : "application/x-www-form-urlencoded",
			// //发送到服务器的数据编码类型
			pageNumber : 1, // 如果设置了分布，首页页码
			pageSize : 10, // 如果设置了分页，每页数据条数
			pageList: [10, 20, 50],        //可供选择的每页的行数（*）
			// search : true, // 是否显示搜索框
			// showColumns : true, // 是否显示内容下拉框（选择显示的列）
			sidePagination : "server", // 设置在哪里进行分页，可选值为"client" 或者"server"
			queryParams : queryParams,
			// //请求服务器数据时，你可以通过重写参数的方式添加一些额外的参数，例如 toolbar 中的参数 如果
			// queryParamsType = 'limit' ,返回参数必须包含
			// limit, offset, search, sort, order 否则, 需要包含:
			// pageSize, pageNumber, searchText, sortName,
			// sortOrder.
			// 返回false将会终止请求
			columns : [
					{ // 列配置项
						// 数据类型，详细参数配置参见文档http://bootstrap-table.wenzhixin.net.cn/zh-cn/documentation/
						checkbox : true
					// 列表中显示复选框
					},
					{
						field : 'id', // 列字段名
						title : '编号' // 列标题
					},
					{
						field : 'module_number',
						title : '模块编码'
					},
					{
						field : 'module_name',
						title : '模块名'
					},
					{
						field : 'module_type',
						title : '模块类型',
						formatter: function (value, row, index) {
							if(row.module_type==1){
								return  "业务模块"
							}else if(row.module_type==0){
								return  "接口模块"
							}
						}
					},
					{
						field : 'module_desc',
						title : '模块描述'
					},
					{
						field : 'manager',
						title : '负责人'
					},
					{
						field : 'builder',
						title : '创建人'
					},
					{
						field : 'build_time',
						title : '创建时间'
					},
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-primary btn-sm '+s_edit_h+'" href="#" mce_href="#" title="编辑" onclick="edit(\'' + row.id + '\')">编辑</a> ';
							var d = '<a class="btn btn-warning btn-sm '+s_remove_h+'" href="#" title="删除"  mce_href="#" onclick="remove(\'' + row.id + '\')">删除</a> ';
							return e + d;
						}
					} ]
		});
});



function reLoad() {
	$('#exampleTable').bootstrapTable('refresh');
}

function search() {
    $("#exampleTable").bootstrapTable('refresh',{pageNumber:1});
}

function add() {
	// iframe层
	layer.open({
		type : 2,
		title : '添加模块',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/sys/moduleAddPage'
		//content : prefix + '/add' // iframe的url
	});
}

function remove(id) {
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : "/sys/moduleDelete",
			type : "post",
			data : {
				'id' : id
			},
			success : function(r) {
				if (r.code === 0) {
					layer.msg("删除成功");
					reLoad();
				} else {
					layer.msg("删除失败");
				}
			}
		});
	})

}
function edit(id) {
	layer.open({
		type : 2,
		title : '模块修改',
		maxmin : true,
		shadeClose : true, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/sys/moduleEditPage?id='+id // iframe的url
	});
}

function batchRemove() {
	var rows = $('#exampleTable').bootstrapTable('getSelections'); //返回所有选择的行，当没有选择的记录时，返回一个空数组
	console.log(rows)
	if (rows.length == 0) {
		layer.msg("请选择要删除的数据");
		return;
	}
	layer.confirm("确认要删除选中的" + rows.length + "条数据吗?", {
		btn : [ '确定', '取消' ]
	}, function() {
		var ids = new Array();
		$.each(rows, function(i, row) {
			console.log(i)
			console.log(row['id'])
			ids[i] = row['id'];
		});
		console.log(ids);
		$.ajax({
			type : 'POST',
			traditional:true,			//不加这个,ajax会将结果后边加个[]
			data : {
				'ids' : ids
			},
			url :'/sys/moduleBatchDelete',
			success : function(r) {
				if (r.code == 0) {
					layer.msg('删除成功');
					reLoad();
				} else {
					layer.msg('删除失败');
				}
			}
		});
	}, function() {});
}