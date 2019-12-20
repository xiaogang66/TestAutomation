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
        url: "/sys/moduleAdd",
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
            module_number:{
                required: true,
                remote: {
                    url: "/sys/moduleNumberIsExit",
                    type: "post",
                    dataType: "json",
                    data: {
                        module_number: function () {
                            return $("#module_number").val();
                        }
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
                remote: icon + "模块编号已经存在"
            },
			module_name: {
                required: icon + "请输入模块名",
            },
        }
    })
}

//关闭弹窗
$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});
