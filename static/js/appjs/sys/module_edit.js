var original_number = $("#module_number").val()

$(function() {
	validateRule();
});

$.validator.setDefaults({
	submitHandler : function() {
		update();
	}
});


function update() {
	var user = $('#signupForm').serialize();
	$.ajax({
		cache : true,
		type : "POST",
		url : "/sys/moduleEdit",
		data : user, // 你的formid
		async : false,
		error : function(request) {
			alert("Connection error");
		},
		success : function(r) {
			if (r.code == 0) {
				parent.layer.msg('修改成功');
				parent.reLoadTree();
				var index = parent.layer.getFrameIndex(window.name); // 获取窗口索引
				parent.layer.close(index);
			} else {
				parent.layer.msg('修改失败');
			}
		}
	});
}

function validateRule() {
    var icon = "<i class='fa fa-times-circle'></i> ";
    $("#signupForm").validate({
        rules: {
			module_number: {
                required: true,
				remote: {
                    url: "/sys/moduleNumberIsExist",
                    type: "post",
                    dataType: "json",
                    data: {
                        'module_number': function () {
                            return $("#module_number").val();
                        },
                        'original_number':original_number
                    }
                }
            },
            module_name: {
                required: true,
            },
        },
        errorPlacement: function (error, element) {
            if (element.is(":radio") || element.is(":checkbox")) {
                error.appendTo(element.parent().parent());
            } else {
                error.appendTo(element.parent());
            }
        },
        messages: {
			module_number: {
                required: icon + "请输入模块编码",
				remote: icon + "模块编码已经存在",
            },
			module_name: {
                required: icon + "请输入模块名",
            },
        }
    })
}


$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});