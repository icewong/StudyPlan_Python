/*! liu_hui */

function changeResultIcon(caseid,use_ico)
{
    var testcase=$(".testcase#"+caseid);
    var icon=testcase.children("span.fa");
    if (icon.length!=0) {testcase.children("span.fa").remove();}
    testcase.prepend('<span class="fa '+use_ico+'" aria-hidden="true"/>');
    if (use_ico=="fa-times"){$("#addNewBug").show();}
    else{$("#addNewBug").hide();}
}

function updateResult(button,state){
    $("#waiting").show();
    var caseid=$(".testcaseDetail").attr("caseid");
    var use_ico;
    if (state==0){use_ico="fa-check";}
    else if(state==1){use_ico="fa-times";}
    else if(state==2){use_ico="fa-exclamation";}
    else {return;}
    $.post('/testcase/Instances/case/'+caseid+'/', {
        testresult:state},
        function(data,textStatus){
        if( data=='updated' ){
            changeResultIcon(caseid,use_ico);
             $("#waiting").hide();
            }
    });
}
function dlgFormSubmit(event){
    $("#waiting").show();
    var bug_dlg_id=$(this).parent().parent().parent().parent('.failDlg').attr('id');
    var bugid=bug_dlg_id.match(/\d+/);
        $.ajax({url:window.location.pathname+'bug/'+bugid,
            type:'POST',
            async:false,
            data:$(this).serialize()+'&testresult=1',
            success: function(data,statue){
                $("#waiting").hide();
                if( data!='updated' ){
                    $("#"+bug_dlg_id+" .dlg_error_info").html(data);
                }
                else{
                    $("#"+bug_dlg_id).modal('hide');
                    $("#"+bug_dlg_id+" .dlg_error_info").html("");
                }
            },
            error:function(jqXHR,textStatus){
                $("#waiting").hide();
                $("#"+bug_dlg_id+" .dlg_error_info").html(data);
            }
        });

        return false;
}

function commentFormSubmit(event){
    $("#waiting").show();
    var caseid=$(".testcaseDetail").attr("caseid");
    $.ajax({
        url:'/testcase/Instances/case/'+caseid+'/',
        type:'POST',
        async:false,
        data:$(this).serialize(),
        success: function (data, textStatus) {
            $("form#form_comment button").attr('disabled','disabled');
            $("#waiting").hide();
        },
        error:function(jqXHR,textStatus){
            $("#waiting").hide();
            $("#baseErrorInfo").html(jqXHR.responseText);
        }
    });
    return false;
}

function deleteBug(dlg_id){
    $("#waiting").show();
    var caseid=$(".testcaseDetail").attr("caseid");
    $.ajax({
        url:"/testcase/Instances/del-bug/"+caseid+"/",
        type:'POST',
        async:false,
        data:"deleteBug="+dlg_id,
        success: function (data, textStatus) {
            $(".comb-del").has("a[related_dlg_id="+dlg_id+"]").remove();
            $("#"+dlg_id).remove();
            $("#waiting").hide();
        },
        error:function(jqXHR,textStatus){
            $("#waiting").hide();
            showPromptDlg(jqXHR.responseText);
        }
    });
    hidePrmoptDlg();
}

function boundDeleteBug(){
    var realted_item=$(this).prev('a');
    var delete_dlg_id=realted_item.attr("related_dlg_id");
    var delete_text=realted_item.text();
    showWarningDlg("Are you sure to delete <b>"+delete_text+"</b>?","deleteBug('"+delete_dlg_id+"')");
}

function reloadInfo(hideAddBug){
    $("#failbtn").click(function(){updateResult(this,1);});
    $("#successbtn").click(function(){updateResult(this,0);});
    $("#ngbtn").click(function(){updateResult(this,2);});

    $("#detail .failDlg form").submit(dlgFormSubmit);
    if (hideAddBug){ $("#addNewBug").hide();}

    $("form#form_comment").submit(commentFormSubmit);
    $("form#form_comment textarea").keyup(function(){
        var related_btn = $("form#form_comment button");
        if (related_btn.attr('disabled')!=undefined)
        { related_btn.removeAttr('disabled'); }

    });

    $("#dd_bugs i").each(function(){$(this).click(boundDeleteBug);});
}

function reloadInstanceCases(){
    var tested = $("#project_detail").attr('tested');
    if (tested.length>0){
        items=tested.split(';');
        for (i in items){
            var datas=items[i].split(',');
            if (datas[1]=='0'){$(".testcase#"+datas[0]).prepend('<span class="fa fa-check" aria-hidden="true"/>');}
            else if (datas[1]=='1'){$(".testcase#"+datas[0]).prepend('<span class="fa fa-times" aria-hidden="true"/>');}
            else if (datas[1]=='2'){$(".testcase#"+datas[0]).prepend('<span class="fa fa-exclamation" aria-hidden="true"/>');}
        }
    }

    $(".testcase").click(function(){
        $(".testcase.selected").removeClass("selected");
        $(this).addClass("selected");
        var hideAddbug=($(this).has(".fa-times").length==0);
        var htmlobj=$.ajax({url:'/testcase/Instances/case/'+this.id+'/',async:false});
        $("#detail").html(htmlobj.responseText);
            reloadInfo(hideAddbug);
        });

    $('#project_detail').treed();
}

$(document).ready(function(){

    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    function csrfSafeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));}
    $.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        async : false
    });

    reloadInstanceCases();

    $("#fail_dlg_NewFailDlg form").submit(function(event){
            $("#waiting").show();
            var caseid=$(".testcase.selected")[0].id;
            $.ajax({
                url:"/testcase/Instances/new-bug/"+caseid + "/",
                type:'POST',
                async:false,
                data:$(this).serialize() + '&testresult=1',
                success:function (data, statue) {
                    var res_item = $(data);
                    var newid = res_item.attr("id");
                    var jiraNumber = res_item.find('form #id_jira_number')[0].value;
                    var text = '<div class="comb-del"><a related_dlg_id="'+newid+'" onclick="dlgShow('+"'"+newid+"')"+'">JIRA number:'+jiraNumber+'</a><i class="glyphicon glyphicon-remove"></i></div>';
                    $("#addNewBug").before(text);
                    $("#detail").append(data);
                    $("#detail .failDlg form").submit(dlgFormSubmit);
                    $("#waiting").hide();

                    $("#fail_dlg_NewFailDlg").modal('hide');
                    $("#fail_dlg_NewFailDlg .dlg_error_info").html("");
                    $("#fail_dlg_NewFailDlg form")[0].reset();
                },
                error:function(jqXHR,textStatus){
                    $("#waiting").hide();
                    $("#fail_dlg_NewFailDlg .dlg_error_info").html(jqXHR.responseText);
                }
            });

            return false;
    });

    $("#search_div .panel-heading").click(function(){
        $(this).find("span").toggleClass("glyphicon-menu-up glyphicon-menu-down");
        $("#search_div .panel-body").toggle();
    });

    function check_all_search_status(bcheck){
        $("#checkbox_pass")[0].checked=bcheck;
        $("#checkbox_fail")[0].checked=bcheck;
        $("#checkbox_na")[0].checked=bcheck;
        $("#checkbox_none")[0].checked=bcheck;
    }
    $("#radio_search_all").change(function(){
        if (this.checked)
            check_all_search_status(false);
    });

    function check_search_status(){
        var search_all=$("#radio_search_all")[0];
        if (search_all.checked){
            search_all.checked=false;
        }
        var search_condition=$("#radio_search_condition")[0];
        if (!search_condition.checked){
            search_condition.checked=true;
        }
    }
    $("#checkbox_pass").change(check_search_status);
    $("#checkbox_fail").change(check_search_status);
    $("#checkbox_na").change(check_search_status);
    $("#checkbox_none").change(check_search_status);


    $("#id_form_search").submit(function(){
        $("#waiting").show();
        $.ajax({
            url:window.location.pathname+'search/',
            type:'POST',
            async:false,
            data:$(this).serialize(),
            success: function (data, textStatus) {
                $("#div_project_detail").html(data);
                $("#detail").html('<div  id="warnning_info">Please select a test case to test.</div>');
                reloadInstanceCases();
                $("#waiting").hide();
            },
            error:function(jqXHR,textStatus){
                $("#div_project_detail").html(jqXHR.responseText);
            }
        });

        return false;
    });
});
