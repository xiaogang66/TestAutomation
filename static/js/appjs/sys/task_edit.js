//默认触发校验
$().ready(function () {
    validateRule();
});

//校验通过后提交表单请求
$.validator.setDefaults({
    submitHandler: function () {
        update();
    }
});

//修改任务
function update() {
    $.ajax({
        cache: true,
        type: "POST",
        url: "/sys/taskEdit",
        data: $('#signupForm').serialize(),
        async: false,
        error: function (request) {
            parent.layer.alert("新增失败");
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
            task_no:{
                required: true,
            },
            task_name: {
                required: true,
            },
            task_partern: {
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
            task_no: {
                required: icon + "请输入任务编号",
            },
			task_name: {
                required: icon + "请输入任务名称",
            },
            task_partern: {
                required: icon + "请输入任务定时表达式",
            },
        }
    })
}

//关闭弹窗
$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});


//根据任务类型变更对应用例集选项
function changeSuit(suit_type){
    $.ajax({
        url : "/sys/taskSuitList",
        type : "post",
        data : {
            'suit_type' : suit_type
        },
        success : function(r) {
            suits = r.suits;
            console.log(suits)
            $('#suit_id').empty();
            for(var i=0;i<suits.length;i++){
                $('#suit_id').append('<option value="'+suits[i].id+'">'+suits[i].suit_name+'</option>')
            }
        }
    });
}