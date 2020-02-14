//默认触发校验
$(function () {
    //去除默认的tab换行，使textarea中支持tab键
    $("textarea").on('keydown',function(e){
        if(e.keyCode == 9){
            e.preventDefault();
            var indent = '    ';
            var start = this.selectionStart;
            var end = this.selectionEnd;
            var selected = window.getSelection().toString();
            selected = indent + selected.replace(/\n/g,'\n'+indent);
            this.value = this.value.substring(0,start) + selected + this.value.substring(end);
            this.setSelectionRange(start+indent.length,start+selected.length);
        }
    });
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
        url: "/web/caseAdd",
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
                parent.layer.msg("新增失败："+r.msg)
            }
        }
    });
}

//表单校验配置
function validateRule() {
    var icon = "<i class='fa fa-times-circle'></i> ";
    $("#signupForm").validate({
        rules: {
            case_no:{
                required: true,
                remote: {
                    url: "/web/caseNoIsExist",
                    type: "post",
                    dataType: "json",
                    data: {
                        case_no: function () {
                            return $("#case_no").val();
                        }
                    }
                }
            },
            case_name: {
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
            case_no: {
                required: icon + "请输入用例编号",
                remote: icon + "用例编号已经存在"
            },
			case_name: {
                required: icon + "请输入用例名",
            },
        }
    })
}

//关闭弹窗
$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});

