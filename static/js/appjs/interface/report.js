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
    var execute_person=$("#execute_person").val();
	var start_time=$("#start_time").val();
	var end_time=$("#end_time").val();
    var query_params={
        suit_name:suit_name,
		execute_person:execute_person,
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
			url : "/interface/reportList", // 服务器数据的加载地址
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
						field : 'execute_person',
						title : '执行人'
					},
					{
						field : 'start_time',
						title : '执行开始时间'
					},
					{
						field : 'end_time',
						title : '执行结束时间'
					},
					{
						field : 'ececute_status',
						title : '执行状态',
						formatter: function (value, row, index) {
							if(row.ececute_status==1){
								return  "未开始"
							}else if(row.ececute_status==2){
								return  "执行中"
							}else if(row.ececute_status==3){
								return  "执行结束"
							}
                        },
					},
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-primary btn-sm '+s_edit_h+'" href="#" mce_href="#" title="详情" onclick="detail(\'' + row.id + '\')">报告</a> ';
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

function detail(id) {
	layer.open({
		type : 2,
		title : '测试报告详情',
		maxmin : true,
		shadeClose : true, // 点击遮罩关闭层
		area : [ '100%', '100%' ],
		content : '/interface/reportDetailPage?id='+id // iframe的url
	});
}

