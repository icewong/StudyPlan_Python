/*! liu_hui */

function removeUser(obj){
    var userid=$(obj).parent().attr("userid");
    $(obj).parent().remove();
    $(".dropdown-menu li[userid="+userid+"]").removeClass("joined");
}

$(document).ready(function(){

    $(".user i").click(function(){
        removeUser(this);
    });

    $(".user").each(function(){
        var related_li=$(this).siblings(".borderDropdown").children("ul").children("li[userid="+$(this).attr("userid")+"]");
        related_li.addClass("joined");
        $(this).prepend(related_li.children("a").text());
    });

    $(".borderDropdown .dropdown-menu li:not(.joined) a").click(function(){
        if ( $(this).parent("li:not(.joined)").length!=0 ){
            var text='<div class="user" userid="'+$(this).parent().attr("userid")+'">'+$(this).text()+'<i class="glyphicon glyphicon-remove" onclick="removeUser(this)"></i></div>';
            $(this).parents('.borderDropdown').before(text);
            $(this).parent().addClass('joined');
        }
    });


    function formatUploadData(formData){
        var principals=$("#principalList .user");
        for(var i=0; i<principals.length; i++){
            formData.append("principals",principals[i].getAttribute('userid'));
        }
        var members=$("#memberList .user");
        for(var i=0; i<members.length; i++){
            formData.append("members",members[i].getAttribute('userid'));
        }
    }

    $("form").submit(function(){
        var formData = new FormData();
        var token=$("input[name=csrfmiddlewaretoken]");
        formData.append("csrfmiddlewaretoken", token.val());
        var name=$("input[name=project_name]");
        if (name.length==1){ formData.append("project_name", name.val()); }
        var file=$("input[name=docfile]");
        if (file.length==1){ formData.append("docfile",file[0].files[0]); }
        formatUploadData(formData);
        $.ajax({
            url:window.location.pathname,
            type:'POST',
            async:false,
            data:formData,
            processData: false,
            contentType:false,
            success: function (data, textStatus) {
                window.location.href="/testcase/Project/";
            },
            error:function(jqXHR,textStatus){
                $("#errorInfo").html(jqXHR.responseText);
            }
        });

        return false;
    });

});
