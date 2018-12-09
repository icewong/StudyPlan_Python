/*! liu_hui */

function removeVersion(btn){
    $(btn).parent().remove();
}

$(document).ready(function(){
    function change_sub(id){
        htmlobj=$.ajax({url:"/testcase/Instances/add/"+id,async:false});
        var case_detail=$("#testcase-detail");
        case_detail.html(htmlobj.responseText);
        case_detail.ready(function(){
            if (case_detail.is('[sel]')){
                var sel_items=new Array();
                sel_items=case_detail.attr('sel').split(",");
                for(i=0;i<sel_items.length;i++)
                {
                    $(".testcase[id="+sel_items[i]+"] i.glyphicon-unchecked").click();
                }
            }
        });
    }

    var select_testcase=$("select[name=testcase_choice]");
    select_testcase.change(function(){
    if ( this.value!="") {change_sub(this.value); }
    });

    if(select_testcase[0].value!=""){
        change_sub(select_testcase[0].value); }

    $("#btn-add-ver").click(function(){
        var system=$("#ver-system");
        var version=$("#ver-version");
        var ver_info=$("#added-version");
        if ( system.val().length==0) {
            $("#errorInfo").html('Please enter "System" information!');
            system.focus();
        }
        else if ( version.val().length==0 ){
            $("#errorInfo").html('Please enter "Version" information!');
            version.focus();
        }
        else{
            ver_info.append('<div class="version-item"><b class="ver-system">'+system.val()+
                '</b><i>'+version.val()+'</i><i class="glyphicon glyphicon-remove" onclick="removeVersion(this)"></i></div>');
            system.val("");
            version.val("");
        }
    });

    $("form").submit(function(event){
        var ver_info=$("#added-version");
        if ( ver_info.children("div").length==0 ){
            $("#errorInfo").html("Please add at least a Version information!");
            return false;
        }

        var testcase='&testcases=';
        $(".testcase").has('i.glyphicon-check').each(function(){
            testcase+= this.id+",";
        });

        var formData=$(this).serialize()+testcase;
        $("#added-version").children("div").each(function(){
            var ver_info=$(this).children("b").text()+"@:@"+$(this).children("i").text();
            formData+='&versionInfo='+ver_info;
        });


        $.ajax({
            url:window.location.pathname,
            type:'POST',
            async:false,
            data:formData,
            success: function (data, textStatus) {
                window.location.href="/testcase/Instances";
            },
            error:function(jqXHR,textStatus){
                $("#errorInfo").html(jqXHR.responseText);
            }
        });

        return false;
    });

});


