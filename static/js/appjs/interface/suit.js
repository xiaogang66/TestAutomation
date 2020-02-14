//初始化查询条件的日期插件
function initDatePlugin() {
    var timeConf = {
        language: "zh-CN",			//时间语言
        autoclose: true,				//选择日期后自动关闭
        clearBtn: true,				//清除按钮
		// todayBtn:true,				//今日按钮
        format: "yyyy-mm-dd",		//时间格式
		// startDate: "2017年1月1日",	//最小时间
		// endDate: "9017年1月1日"	//最大时间
    };
    $("#start_time").datepicker(timeConf);
    $("#end_time").datepicker(timeConf);
}


//获取查询条件值，以及带上分页条件
var queryParams = function (params) {
    var suit_name=$("#suit_name").val();
    var builder=$("#builder").val();
	var start_time=$("#start_time").val();
	var end_time=$("#end_time").val();
    var query_params={
        suit_name:suit_name,
		builder:builder,
		start_time:start_time,
		end_time:end_time,
		size: params.limit,                         //页面大小
		page: (params.offset / params.limit) + 1,   //页码
    }
    return  query_params
};

//默认加载列表
$(function() {
	initDatePlugin();
	$('#exampleTable').bootstrapTable(
		{
			method : 'get', // 服务器数据的请求方式 get or post
			url : "/interface/suitList", // 服务器数据的加载地址
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
						field : 'id', // 列字段名
						title : 'ID' // 列标题
					},
					{
						field : 'suit_no',
						title : '用例集编号'
					},
					{
						field : 'suit_name',
						title : '用例集名称',
					},
					{
						field : 'suit_description',
						title : '用例集描述'
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
						field : 'modify_time',
						title : '修改时间'
					},
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-warning btn-sm '+s_edit_h+'" href="#" mce_href="#" title="编辑" onclick="edit(\'' + row.id + '\')">编辑</a> ';
							var d = '<a class="btn btn-danger btn-sm '+s_remove_h+'" href="#" title="删除"  mce_href="#" onclick="remove(\'' + row.id + '\')">删除</a> ';
							var f = '<a class="btn btn-primary btn-sm '+s_cases_h+'" href="#" title="用例维护"  mce_href="#" onclick="maintainCases(\'' + row.id + '\')">用例维护</a> ';
							var g = '<a class="btn btn-success btn-sm '+s_cases_h+'" href="#" title="执行"  mce_href="#" onclick="execute(\'' + row.id + '\')">执行</a> ';
							return e + d + f + g;
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
		title : '添加用例集',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/interface/suitAddPage'
	});
}

function remove(id) {
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : "/interface/suitDelete",
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
		title : '修改用例集',
		maxmin : true,
		shadeClose : true, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/interface/suitEditPage?id='+id // iframe的url
	});
}


function maintainCases(id){
	layer.open({
		type : 2,
		title : '用例维护',
		maxmin : true,
		shadeClose : true, // 点击遮罩关闭层
		area : [ '90%', '90%' ],
		content : '/interface/suitCaseListPage?suitId='+id // iframe的url
	});
}

function execute(id){
	layer.confirm('确定要执行该用例集？', {
		btn : [ '确定', '取消' ]
	}, function() {
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
        layer.msg("执行开始，请稍后查看报告！");
	});
}