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
        url: "/web/elementAdd",
        data: $('#signupForm').serialize(),
        async: false,
        error: function (request) {
            parent.layer.alert("Connection error");
        },
        success: function (data) {
            if (data.code == 0) {
                parent.layer.msg("新增成功");
                parent.search();
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
                required: icon + "请输入元素名称",
            },
            locate_partern: {
                required: icon + "请输入定位表达式",
            },
        }
    })
}

//关闭弹窗
$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});
