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
		url : "/sys/userEdit",
		data : user, // 你的formid
		async : false,
		error : function(request) {
			alert("Connection error");
		},
		success : function(r) {
			if (r.code == 0) {
				parent.layer.msg('修改成功');
				parent.reLoad();
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
            user_name: {
                required: true,
				rangelength: [1,20]
            },
            account: {
                required: true
            },
            password: {
                required: true,
                minlength: 6
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
			user_name: {
                required: icon + "请输入您的姓名",
                rangelength: icon + "姓名长度范围为1-20个字符",
            },
            account: {
                required: icon + "请输入账号",
            },
            password: {
                required: icon + "请输入您的密码",
                minlength: icon + "密码必须6个字符以上"
            },
        }
    })
}