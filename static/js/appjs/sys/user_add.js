$().ready(function () {
    $("#usersource").trigger('change');
    validateRule();
});

$.validator.setDefaults({
    submitHandler: function () {
        save();
    }
});

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
                remote: {
                    url: "/sys/userAccountIsExit",
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
                remote: icon + "账号已经存在"
            },
            password: {
                required: icon + "请输入您的密码",
                minlength: icon + "密码必须6个字符以上"
            },
        }
    })
}

var openDept = function () {
    var usersource = $("#usersource").val();
    if (!usersource) {
        layer.msg("请先选择用户来源");
        return false;
    }
    if (usersource == 0) {
        layer.open({
            type: 2,
            title: "选择机构",
            area: ['800px', '520px'],
            content: "/system/sysDept/treeView/" + usersource
        })
    } else if (usersource == 1) {
        layer.open({
            type: 2,
            title: "选择供应商",
            area: ['800px', '520px'],
            content: "/sys/user/toSupplierList"
        })
    }

};

$('#usersource').on('change', function () {
    $('#todeptcode').val('');
    $('#todeptName').val('');
});

function loadDept(deptId, deptName, subHqCode) {
    $("#todeptcode").val(deptId);
    $("#subHqCode").val(subHqCode);
    $("#todeptName").val(deptId + "_" + deptName).valid();

    $.ajax({
        url: "/sys/role/list",
        type: "get",
        data: {
            userSource: $('#usersource').val(),
            userRoleCode: '',
            subHqCode: "'"+subHqCode+"'"
        },
        success: function (r) {
            var html = '';
            r.forEach(function (value, index) {
                html += "<label class=\"checkbox-inline\">\n" +
                    " <input name=\"role\" type=\"checkbox\" value=\"" + value.userRoleCode + "\"/>" + value.userRoleName +
                    "</label>";
            });
            $('#roles').html(html);
        }
    });
};

$("#cancel").on("click", function () {
	alert('关闭弹框');
    parent.closeLayer();
});
