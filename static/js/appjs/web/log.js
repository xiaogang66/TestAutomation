//获取查询条件值，以及带上分页条件
var queryParams = function (params) {
    var log_name=$("#log_name").val();
    var query_params={
        log_name:log_name,
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
			url : "/web/logList", // 服务器数据的加载地址
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
			undefinedText: '',
			columns : [
					{ // 列配置项
						// 数据类型，详细参数配置参见文档http://bootstrap-table.wenzhixin.net.cn/zh-cn/documentation/
						// 列表中不显示复选框
						checkbox : false
					},
					{
						field : 'log_name',
						title : '文件名'
					},
					{
						field : 'log_size',
						title : '文件大小',
					},
					{
						field : 'build_time',
						title : '创建时间'
					},
					{
						field : 'modify_time',
						title : '修改时间'
					},
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-primary btn-sm '+s_edit_h+'" href="#" mce_href="#" title="详情" onclick="detail(\'' + row.log_name + '\')">详情</a> ';
							return e ;
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

function detail(log_name) {
	// iframe层
	layer.open({
		type : 2,
		title : '日志详情：'+log_name,
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '80%', '80%' ],
		content : '/web/logDetailPage?logName='+log_name
	});
}
