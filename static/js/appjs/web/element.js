var choseModuleId = "";

//获取查询条件值，以及带上分页条件
var queryParams = function (params) {
    var element_name=$("#element_name").val();
	var locate_type=$("#locate_type").val();
    var query_params={
    	choseModuleId:choseModuleId,
        element_name:element_name,
        locate_type:locate_type,
		size: params.limit,                         //页面大小
		page: (params.offset / params.limit) + 1,   //页码
    }
    return  query_params
};

$(function() {
    //展示树状菜单
	getTreeData("/sys/moduleTree");
	//查询节点用例列表
	loadElement()

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


function loadElement() {
   $('#exampleTable').bootstrapTable(
		{
			method : 'get', // 服务器数据的请求方式 get or post
			url : "/web/elementList", // 服务器数据的加载地址
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
						title : '编号' // 列标题
					},
					{
						field : 'element_name',
						title : '元素名'
					},
					{
						field : 'description',
						title : '元素描述'
					},
					{
						field : 'locate_type',
						title : '定位方式',
						formatter: function (value, row, index) {
							if(row.locate_type==1){
								return  "by id"
							}else if(row.locate_type==2){
								return  "by name"
							}else if(row.locate_type==3){
								return  "by cssSelector"
							}else if(row.locate_type==4){
								return  "by xpath"
							}else if(row.locate_type==5){
								return  "by class"
							}else if(row.locate_type==6){
								return  "by tag"
							}else if(row.locate_type==7){
								return  "by linkText"
							}else if(row.locate_type==8){
								return  "by frame"
							}else if(row.locate_type==9){
								return  "by window"
							}
                        },
					},
					{
						field : 'locate_partern',
						title : '定位表达式'
					},
					{
						title : '操作',
						field : 'roleId',
						align : 'center',
						formatter : function(value, row, index) {
							var e = '<a class="btn btn-warning btn-sm '+s_edit_h+'" href="#" mce_href="#" title="编辑" onclick="edit(\'' + row.id + '\')">编辑</a> ';
							var d = '<a class="btn btn-danger btn-sm '+s_remove_h+'" href="#" title="删除"  mce_href="#" onclick="remove(\'' + row.id + '\')">删除</a> ';
							return e + d;
						}
					} ]
		});
}


function add() {
	if(!choseModuleId){
		layer.alert("请选择模块节点");
		return;
	}
	// iframe层
	layer.open({
		type : 2,
		title : '添加元素',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/web/elementAddPage?moduleId='+choseModuleId
	});
}

function remove(id) {
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : "/web/elementDelete",
			type : "post",
			data : {
				'id' : id
			},
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
function edit(id) {
	layer.open({
		type : 2,
		title : '修改元素',
		maxmin : true,
		shadeClose : true, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/web/elementEditPage?id='+id // iframe的url
	});
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
        //$('#jstree').jstree().open_all();  //展开所有节点
    });
}


function search() {
    $("#exampleTable").bootstrapTable('refresh',{pageNumber:1,choseModuleId:choseModuleId});
}
