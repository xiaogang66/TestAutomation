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
                    }]
            }
    );
}


//添加用例至用例集
function add() {
	var suitId = $('#suitId').val();
	var rows = $('#exampleTable').bootstrapTable('getSelections'); //返回所有选择的行，当没有选择的记录时，返回一个空数组
	if (rows.length == 0) {
		layer.msg("请选择要添加的数据");
		return;
	}
	var ids = new Array();
		$.each(rows, function(i, row) {
			ids[i] = row['id'];
		});
		$.ajax({
			type : 'POST',
			traditional:true,			//不加这个,ajax会将结果后边加个[]
			data : {
				'caseIds' : ids,
				'suitId': suitId
			},
			url :'/interface/suitCaseAdd',
			success : function(r) {
				if (r.code == 0) {
					var index = parent.layer.getFrameIndex(window.name);
                	parent.layer.close(index);
                	parent.layer.msg('添加成功');
					parent.reLoad();
				} else {
					layer.msg('添加失败');
				}
			}
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
        $('#jstree').jstree().open_all();  //展开所有节点
    });
}


function search() {
    $("#exampleTable").bootstrapTable('refresh',{pageNumber:1,moduleId:choseModuleId});
}
