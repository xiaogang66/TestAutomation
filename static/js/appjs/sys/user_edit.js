var original_account = $("#account").val();

$(function() {
	validateRule();
});

$.validator.setDefaults({
	submitHandler : function() {
		update();
	}
});


function update() {
	$.ajax({
		cache : true,
		type : "POST",
		url : "/sys/userEdit",
		data : $('#signupForm').serialize(), // 你的formid
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
                rangelength: [1, 20]
            },
            account: {
                required: true,
                minlength: 3,
                remote: {
                    url: "/sys/userAccountIsExist",
                    type: "post",
                    dataType: "json",
                    data: {
                        'account': function () {
                            return $("#account").val();
                        },
                        'original_account':original_account
                    }
                }
            },
            password: {
                minlength: 3
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
                minlength: icon + "密码必须3个字符及以上",
                required: icon + "请输入账号",
                remote: icon + "账号已经存在",
            },
            password: {
                minlength: icon + "密码必须3个字符及以上",
            },
        }
    });
}


$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});