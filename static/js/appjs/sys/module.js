var choseModuleId = "";

$(function() {
    //展示树状菜单
	getTreeData("/sys/moduleTree");
	//展示对应节点详情
	loadDetail('');

	//树点击事件
	$('#jstree').on("changed.jstree", function (e, data) {
		var opt = {};
		if (data.selected == -1) {
			choseModuleId = "";
		} else {
			choseModuleId = data.selected[0] == "" || data.selected[0] == '0' ? '' : data.selected[0];
			// choseSubhqname = data.instance.get_node(data.selected[0]).state.nodeName;
			// choseSubhqType = data.instance.get_node(data.selected[0]).state.nodeType;
		}
		opt = {
			query: {
				id: choseModuleId
			}
		};
        loadDetail(choseModuleId);
	});
});


function clearDetail() {
    $('#id').val('');
    $('#module_number').val('');
    $('#module_name').val('');
    $('#module_type').val('');
    $('#module_desc').val('');
    $('#manager').val('');
    $('#builder').val('');
    $('#build_time').val('');
}


function loadDetail(id) {
    //根据id显示对应节点的详情
    if(id != undefined && id !=''){
        $.ajax({
			url : "/sys/getModuleById",
			type : "post",
            dataType:'json',
			data :{'id':id} ,
			success : function(r) {
				if (r.code === 0) {
					var module = r.data;
                    $('#id').val(module.id);
                    $('#module_number').val(module.module_number);
                    $('#module_name').val(module.module_name);
                    if(module.module_type==1){
                        $('#module_type').val('业务模块');
                    }else if(module.module_type==0){
                        $('#module_type').val('接口模块');
                    }
                    $('#module_desc').val(module.module_desc);
                    $('#manager').val(module.manager);
                    $('#builder').val(module.builder);
                    $('#build_time').val(module.build_time);
				} else {
					layer.msg('获取详情失败');
					clearDetail();
				}
			}
		});
    }else{
        clearDetail();
    }
}


//添加模块
function addSub() {
    if(!choseModuleId){
        choseModuleId = ''
    }
	layer.open({
		type : 2,
		title : '添加模块',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/sys/moduleAddPage?subId='+choseModuleId
	});
}


//编辑模块
function editSub() {
	if(!choseModuleId){
		layer.alert("请选择数据");
		return;
	}
	layer.open({
		type : 2,
		title : '编辑模块',
		maxmin : true,
		shadeClose : false, // 点击遮罩关闭层
		area : [ '70%', '70%' ],
		content : '/sys/moduleEditPage?id='+ choseModuleId
	});
}


//删除模块
function deleteSub() {
    if(!choseModuleId){
		layer.alert("请选择数据");
		return;
	}
	layer.confirm('确定要删除选中的记录？', {
		btn : [ '确定', '取消' ]
	}, function() {
		$.ajax({
			url : "/sys/moduleDelete",
			type : "post",
			data :{'id':choseModuleId} ,
			success : function(r) {
				if (r.code === 0) {
					layer.msg("删除成功");
					reLoadTree();
				} else {
					layer.msg(r.msg);
				}
			}
		});
	})
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


// 操作模块后刷新树网和详情
function reLoadTree(){
	$('#jstree').data('jstree', false).empty();		//清空树
	getTreeData("/sys/moduleTree");					//重新加载树
    loadDetail('');                                  //刷新右侧详情为空
}