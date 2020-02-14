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
    var query_params={
    	suit_record_id: $("#suit_record_id").val(),
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
			url : "/interface/reportDetail", // 服务器数据的加载地址
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
						field : 'module_name',
						title : '模块名'
					},
					{
						field : 'case_no',
						title : '用例编号',
					},
					{
						field : 'case_name',
						title : '用例名称'
					},
					{
						field : 'case_description',
						title : '用例描述'
					},
					{
						field : 'builder',
						title : '创建人'
					},
					{
						field : 'url',
						title : '请求URL'
					},
					// {
					// 	field : 'request_method',
					// 	title : '请求方式',
					// 	formatter: function (value, row, index) {
					// 		if(row.request_method==1){
					// 			return  "GET"
					// 		}else if(row.request_method==2){
					// 			return  "POST"
					// 		}
                    //     },
					// },
					// {
					// 	field : 'request_param',
					// 	title : '请求参数'
					// },
					// {
					// 	field : 'exp_result',
					// 	title : '预期结果'
					// },
					// {
					// 	field : 'asset_type',
					// 	title : '断言类型',
					// 	formatter: function (value, row, index) {
					// 		if(row.asset_type==1){
					// 			return  "相等"
					// 		}else if(row.asset_type==2){
					// 			return  "包含"
					// 		}else if(row.asset_type==3){
					// 			return  "正则"
					// 		}
                    //     }
					// },
					// {
					// 	field : 'asset_partern',
					// 	title : '断言表达式'
					// },
					{
						field : 'status_code',
						title : '状态码'
					},
					// {
					// 	field : 'real_result',
					// 	title : '实际结果'
					// },
					{
						field : 'start_time',
						title : '执行开始时间'
					},
					{
						field : 'end_time',
						title : '执行结束时间'
					},
					{
						field : 'period',
						title : '耗时(ms)'
					},
					{
						field : 'pass_flag',
						title : '是否通过',
						formatter: function (value, row, index) {
							if(row.pass_flag==1){
								return  "通过"
							}else if(row.pass_flag==2){
								return  "未通过"
							}else if(row.pass_flag==3){
								return  "异常"
							}else{
								return  "未知"
							}
                        }
					},
					{
						field : 'exception_msg',
						title : '异常信息'
					},
					]
		});
});



function reLoad() {
	$('#exampleTable').bootstrapTable('refresh');
}


