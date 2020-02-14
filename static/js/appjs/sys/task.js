//获取查询条件值，以及带上分页条件
var queryParams = function (params) {
	var task_no=$("#task_no").val();
    var task_name=$("#task_name").val();
    var run_flag=$("#run_flag").val();
    var task_type=$("#task_type").val();
    var query_params={
    	task_no:task_no,
        task_name:task_name,
        run_flag:run_flag,
		task_type:task_type,
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
			url : "/sys/taskList", // 服务器数据的加载地址
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
						checkbox : true
					// 列表中显示复选框
					},
					{
						field : 'task_no', // 列字段名
						title : '任务编号' // 列标题
					},
					{
						field : 'task_name',
						title : '任务名称'
					},
					{
						field : 'task_type',
						title : '任务类型',
						formatter: function (value, row, index) {
							if(row.task_type==1){
								return  "接口任务"
							}else if(row.task_type==2){
								return  "UI任务"
							}
						}
					},
					{
						field : 'task_partern',
						title : '定时表达式'
					},
					{
						field : 'task_desc',
						title : '备注'
					},
					{
						field : 'run_flag',
						title : '启用标志',
						formatter: function (value, row, index) {
							if(row.run_flag==1){
								return  "启用"
							}else if(row.run_flag==0){
								return  "禁用"
							}
						}
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
						field : 'suit_name',
						title : '用例集名称'
					},
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-warning btn-sm '+s_edit_h+'" href="#" mce_href="#" title="编辑" onclick="edit(\'' + row.id + '\')">编辑</a> ';
							var d = '<a class="btn btn-danger btn-sm '+s_remove_h+'" href="#" title="删除"  mce_href="#" onclick="remove(\'' + row.id + '\')">删除</a> ';
							var f = '<a class="btn btn-success btn-sm '+s_execute_h+'" href="#" title="手动执行"  mce_href="#" onclick="execute(\'' + row.suit_id + '\',\'' + row.task_type + '\')">手动执行</a> ';
							return e + d + f;
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
		title : '添加任务',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/sys/taskAddPage'
		//content : prefix + '/add' // iframe的url
	});
}

function remove(id) {
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : "/sys/taskDelete",
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
		title : '用户修改',
		maxmin : true,
		shadeClose : true, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/sys/taskEditPage?id='+id // iframe的url
	});
}

//任务手动执行
function execute(id,task_type){
	layer.confirm('确定要执行该任务？', {
		btn : [ '确定', '取消' ]
	}, function() {
		if(task_type == '1'){
			$.ajax({
				url : "/interface/suitExecute",
				type : "post",
				data : {
					'suitId' : id
				},
				success : function(r) {
					if (r.code === 1) {
						layer.msg("执行异常...");
					}
				}
			});
		}else if(task_type == '2'){
			$.ajax({
				url : "/web/suitExecute",
				type : "post",
				data : {
					'suitId' : id
				},
				success : function(r) {
					if (r.code === 1) {
						layer.msg("执行异常...");
					}
				}
			});
		}
        layer.msg("执行开始，请稍后查看报告！");
	});
}