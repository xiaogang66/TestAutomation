//默认加载列表
$(function() {
	    $('#exampleTable').bootstrapTable(
            {
                method: 'get', // 服务器数据的请求方式 get or post
                url: "/interface/suitCaseList", // 服务器数据的加载地址
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
						suitId : $('#suitId').val(),
						case_no : $('#case_no').val(),
						case_name : $('#case_name').val()
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
                    }]
            }
    );
});


function remove() {
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
		console.log(ids)
		$.ajax({
			type : 'POST',
			traditional:true,			//不加这个,ajax会将结果后边加个[]
			data : {
				'caseIds' : ids,
				'suitId': $('#suitId').val()
			},
			url :'/interface/suitCaseDelete',
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


function add() {
	suitId = $('#suitId').val()
    layer.open({
        type: 2,
        title: '添加用例',
        maxmin: true,
        shadeClose: false, // 点击遮罩关闭层
        area: ['100%', '100%'],
        content: '/interface/suitCaseAddPage?suitId='+suitId
    });
}


function reLoad() {
	$('#exampleTable').bootstrapTable('refresh');
}

function search(){
	$("#exampleTable").bootstrapTable('refresh',{pageNumber:1});
}