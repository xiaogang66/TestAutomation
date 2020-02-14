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
    autoTextarea(document.getElementById("request_header"));
    autoTextarea(document.getElementById("request_cookie"));
    autoTextarea(document.getElementById("request_param"));
    autoTextarea(document.getElementById("assert_partern"));
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
        url: "/interface/caseAdd",
        data: $('#signupForm').serialize(),
        async: false,
        error: function (request) {
            parent.layer.alert("Connection error");
        },
        success: function (data) {
            if (data.code == 0) {
                parent.layer.msg("复制成功");
                parent.search();
                var index = parent.layer.getFrameIndex(window.name);
                parent.layer.close(index);
            } else {
                parent.layer.msg("复制失败："+r.msg)
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
                    url: "/interface/caseNoIsExist",
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
            url: {
                required: true,
            },
            assert_partern: {
                required: true,
            }
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
            url: {
                required: icon + "请输入请求url",
            },
            assert_partern: {
                required: icon + "请输入断言值",
            }
        }
    })
}

//关闭弹窗
$("#cancel").on("click", function () {
    var index = parent.layer.getFrameIndex(window.name);
    parent.layer.close(index);
});


function autoTextarea(elem, extra, maxHeight) {
    extra = extra || 0;
    var isFirefox = !!document.getBoxObjectFor || 'mozInnerScreenX' in window,
            isOpera = !!window.opera && !!window.opera.toString().indexOf('Opera'),
            addEvent = function(type, callback) {
                elem.addEventListener ?
                        elem.addEventListener(type, callback, false) :
                        elem.attachEvent('on' + type, callback);
            },
            getStyle = elem.currentStyle ? function(name) {
                var val = elem.currentStyle[name];
                if (name === 'height' && val.search(/px/i) !== 1) {
                    var rect = elem.getBoundingClientRect();
                    return rect.bottom - rect.top -
                            parseFloat(getStyle('paddingTop')) -
                            parseFloat(getStyle('paddingBottom')) + 'px';
                };
                return val;
            } : function(name) {
                return getComputedStyle(elem, null)[name];
            },
            minHeight = parseFloat(getStyle('height'));
    elem.style.resize = 'none';
    var change = function() {
        var scrollTop, height,
                padding = 0,
                style = elem.style;
        if (elem._length === elem.value.length) return;
        elem._length = elem.value.length;
        if (!isFirefox && !isOpera) {
            padding = parseInt(getStyle('paddingTop')) + parseInt(getStyle('paddingBottom'));
        };
        scrollTop = document.body.scrollTop || document.documentElement.scrollTop;
        elem.style.height = minHeight + 'px';
        if (elem.scrollHeight > minHeight) {
            if (maxHeight && elem.scrollHeight > maxHeight) {
                height = maxHeight - padding;
                style.overflowY = 'auto';
            } else {
                height = elem.scrollHeight - padding;
                style.overflowY = 'hidden';
            };
            style.height = height + extra + 'px';
            scrollTop += parseInt(style.height) - elem.currHeight;
            document.body.scrollTop = scrollTop;
            document.documentElement.scrollTop = scrollTop;
            elem.currHeight = parseInt(style.height);
        };
    };
    addEvent('propertychange', change);
    addEvent('input', change);
    addEvent('focus', change);
    change();
};