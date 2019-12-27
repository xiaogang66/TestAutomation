//默认触发校验
$().ready(function () {
    validateRule();
});

//校验通过后提交表单请求
$.validator.setDefaults({
    submitHandler: function () {
        save();
    }
});

//提交表单请求
function save() {
    $.ajax({
        cache: true,
        type: "POST",
        url: "/sys/userAdd",
        data: $('#signupForm').serialize(),
        async: false,
        error: function (request) {
            parent.layer.alert("Connection error");
        },
        success: function (data) {
            if (data.code == 0) {
                parent.layer.msg("新增成功");
                parent.reLoad();
                var index = parent.layer.getFrameIndex(window.name);
                parent.layer.close(index);
            } else {
                parent.layer.msg("新增失败")
            }
        }
    });
}

//表单校验配置
function validateRule() {
    var icon = "<i class='fa fa-times-circle'></i> ";
    $("#signupForm").validate({
        rules: {
            user_name: {
                required: true,
				rangelength: [1,20]
            },
            account: {
                required: true,
                minlength: 3,
                remote: {
                    url: "/sys/userAccountIsExist",
                    type: "post",
                    dataType: "json",
                    data: {
                        account: function () {
                            return $("#account").val();
                        }
                    }
                }
            },
            password: {
                required: true,
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
                required: icon + "请输入账号",
                minlength: icon + "账号必须3个字符及以上",
                remote: icon + "账号已经存在"
            },
            password: {
                required: icon + "请输入您的密码",
                minlength: icon + "密码必须3个字符及以上"
            },
        }
    })
}

//关闭弹窗
$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});
