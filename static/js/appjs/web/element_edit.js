$(function() {
	validateRule();
});

$.validator.setDefaults({
	submitHandler : function() {
		update();
	}
});


function update() {
	var data = $('#signupForm').serialize();
	$.ajax({
		cache : true,
		type : "POST",
		url : "/web/elementEdit",
		data : data,
		async : false,
		error : function(request) {
			alert("Connection error");
		},
		success : function(r) {
			if (r.code == 0) {
				parent.layer.msg('修改成功');
				parent.search();
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
            element_name: {
                required: true,
            },
			locate_partern: {
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
			element_name: {
                required: icon + "请输入元素名",
            },
			locate_partern: {
                required: icon + " 请输入定位表达式",
            },
        }
    })
}


$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});