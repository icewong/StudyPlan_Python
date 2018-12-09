/*! liu_hui */

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
        var htmlobj=$.ajax({url:'/testcase/Instances/case/'+this.id,async:false});
        $("#detail").html(htmlobj.responseText);
            reloadInfo(hideAddbug);
        });

    $('#project_detail').treed();
}



function showEditDlg(){
    var item=$(this).parent().parent();
    var form=$("#dlg_from_id_NewFailDlg");
    form.children("dl").attr('bug_id',item.attr("id"));
    form.find('input[name=jira_number]').val(item.children(".number").text());
    form.find('select[name=system]').val(item.children(".system").attr("data"));
    form.find('select[name=status]').val(item.children(".status").attr("data"));
    form.find('input[name=occurance_probability]').val(item.children(".probility").text());
    form.find('textarea[name=description]').val(item.children(".content").text());
    dlgShow('fail_dlg_NewFailDlg');
}
function saveEditDlgData(){
    var form=$("#dlg_from_id_NewFailDlg");
    var bug_id=form.children("dl").attr('bug_id');
    var item=$("tr#"+bug_id);
    item.children(".number").text(form.find('input[name=jira_number]').val());
    var system_item=item.children(".system")
    system_item.attr("data",form.find('select[name=system]').val());
    system_item.each(translateSystem);
    var status_item=item.children(".status");
    status_item.attr("data",form.find('select[name=status]').val());
    status_item.each(translateStatus);
    item.children(".probility").text(form.find('input[name=occurance_probability]').val());
    item.children(".content").text(form.find('textarea[name=description]').val());
}

function translateSystem(){
    var idf=$(this).attr("data");
    if(idf==1){ $(this).text('iOS'); }
    else if(idf==2){ $(this).text('Android'); }
    else { $(this).text('Unknown'); }
}
function translateStatus(){
    var idf=$(this).attr("data");
    if(idf==1){ $(this).text('Opening'); }
    else if(idf==2){ $(this).text('Closed'); }
    else if(idf==3){ $(this).text('Pending'); }
    else { $(this).text('Unknown'); }
}

function deleteBug(dlg_id){
    $("#waiting").show();
    var caseid=$(".testcaseDetail").attr("caseid");
    $.ajax({
        url:"/testcase/Bugs/delete/",
        type:'POST',
        async:false,
        data:"deleteBug="+dlg_id,
        success: function (data, textStatus) {
            $("tr#"+dlg_id).remove();
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
    var realted_item=$(this).parent().parent();;
    var delete_dlg_id=realted_item.attr("id");
    var delete_text=realted_item.children(".number").text();
    showWarningDlg("Are you sure to delete <b>"+delete_text+"</b>?","deleteBug('"+delete_dlg_id+"')");
}

function reloadBugs(){
    $("td .glyphicon-cog").each(function(){
        $(this).click(showEditDlg);
    });
    $("td .delete").each(function(){
        $(this).click(boundDeleteBug);
    });
    $("td.system").each(translateSystem);
    $("td.status").each(translateStatus);
}

$(document).ready(function(){
    ajaxBoundCsrf();

    reloadBugs();

    $("#dlg_from_id_NewFailDlg").submit(function(event){
        $("#waiting").show();
        var bugid=$(this).children("dl").attr('bug_id');
        $.ajax({url:window.location.pathname+bugid+"/",
            type:'POST',
            async:false,
            data:$(this).serialize()+'&testresult=1',
            success: function(data,statue){
                $("#waiting").hide();
                saveEditDlgData();
                dlgHide("fail_dlg_NewFailDlg");
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

    $("#id_form_search").submit(function(){
        $("#waiting").show();
        $.ajax({
            url:window.location.pathname+'search/',
            type:'POST',
            async:false,
            data:$(this).serialize(),
            success: function (data, textStatus) {
                $("#div_bugs").html(data);
                reloadBugs();
                $("#waiting").hide();
            },
            error:function(jqXHR,textStatus){
                $("#waiting").hide();
                showPromptDlg(jqXHR.responseText);
            }
        });

        return false;
    });
});
