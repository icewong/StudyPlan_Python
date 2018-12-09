/*! liu_hui */

function serializeChangedData(){
    var tokenName="csrfmiddlewaretoken";
    var result="";/*tokenName+'='+$("form input[name="+tokenName+"]").attr('value');*/
    $("form .changed").each(function(){
        result+="&"+$(this).attr("name")+"="+$(this).val();
    });

    return result;
}

function reload_sub_testcase()
{
    ajaxBoundCsrf();

    $("input").change(function(){
        $(this).addClass('changed');
    });
    $("textarea").change(function(){
        $(this).addClass('changed');
    });
    $("select").change(function(){
        $(this).addClass('changed');
    });
    $("form").submit(function(event){
        $("#waiting").show();
        $.ajax({
            url: window.location.pathname+"case/"+$(".testcase.selected").attr("id")+"/",
            type: 'POST',
            data: serializeChangedData(),
            success: function (data, textStatus) {
                $("form input.changed").each(function(){
                    $(this).removeClass('changed');  });
                $("#waiting").hide();
            },
            error: function (jqXHR, textStatus) {
                $("#waiting").hide();
            }
        });

        return false;
    });
}

function deleteTestcase(){
    var case_id=$(".testcase.selected").attr("id");
    $.ajax({
        url: window.location.pathname+"del-case/",
        type:'POST',
        async:false,
        data:"caseID="+case_id,
        success: function (data, textStatus) {
            $("#"+case_id).remove();
            $(".detail").html("<p>Please select a test case to see it's content.</p>");

            hidePrmoptDlg();
        },
        error:function(jqXHR,textStatus){
            hidePrmoptDlg();
            $("#baseErrorInfo").html(jqXHR.responseText);
        }
    });
}

function boundDeleteTestcase(){
    showWarningDlg("Are you sure to delete this test case?","deleteTestcase()");
}

function path_node_related_form_submit(method,fromData,success_fun){
    showWaitDlg();
    var selitem=$("li.selected");
    $.ajax({url: "/testcase/Project/path-node/"+selitem.attr("pathid")+"/",
        async:false,
        type: 'POST',
        data:fromData+";method="+method,
        success: success_fun,
        error:function(jqXHR,textStatus){
            hideWaitDlg();
            showPromptDlg(jqXHR.responseText);
        }
    });
}

function pathnode_click_bound(){
    var idf_active='active';
    if ( !$(this).hasClass(idf_active) ){
        var old_page=$("li[role=presentation].active");
        old_page.removeClass(idf_active);
        $("#"+old_page.attr("related")).hide();
        $(this).addClass(idf_active);
        $("#"+$(this).attr("related")).show();
    }
}

function reload_sub_path_node(){
    ajaxBoundCsrf();

    $("li[role=presentation]").click(pathnode_click_bound);
    $("#add_test_case_form").submit(function(){
        path_node_related_form_submit("ADD_TEST_CASE",$(this).serialize(),function(data, textStatus){
            var cur_item=null;
            if ( $("li.selected ul").length==0 ) {
                var cur_sel=$("li.selected");
                cur_sel.append("<ul/>");
                cur_item=cur_sel.children("ul").append(data);
                cur_sel.each(tree_add_toggle_button);
            }
            else{ cur_item=$("li.selected").children("ul").append(data); }
            cur_item.children(".testcase").last().click(testcase_click_bound);
            request_path_node_page($("li.selected b"));
            hideWaitDlg();});
            return false;
    });
    $("#add_path_node_form").submit(function(){
        path_node_related_form_submit(method="ADD_PATH_NODE",$(this).serialize(),function(data, textStatus){
            var cur_item=null;
            var cur_sel=$("li.selected");
            if ( $("li.selected ul").length==0 ) {
                cur_sel.append("<ul/>");
                cur_item=cur_sel.children("ul").append(data);
                cur_sel.each(tree_add_toggle_button);
            }
            else{
                cur_item=cur_sel.children("ul").append(data);
                if (cur_sel.children("i.glyphicon-plus").length!=0){
                    cur_item.children("li").last().toggle();
                }
            }
            cur_item.children(".path-node").last().children("b").first().click(path_node_click_bound);
            request_path_node_page($("li.selected b"));
            hideWaitDlg();});
        return false;
    });
    $("#delete_form").submit(function(){
        path_node_related_form_submit(method="DELETE",$(this).serialize(),function(data, textStatus){
            $("li.selected").remove();
            $(".detail").html("<p>Please select a test case to see it's content.</p>");
            hideWaitDlg();});
        return false;
    });
    $("#modify_form").submit(function(){
        path_node_related_form_submit(method="MODIFY",$(this).serialize(),function(data, textStatus){
            $("li.selected").children('b').text(data);
            hideWaitDlg();});
        return false;
    });
}

function testcase_click_bound(){
    showWaitDlg();
    $.ajax({url: window.location.pathname+"case/"+this.id+"/",
        async:false,
        type:'GET',
        success: function(data, textStatus) {
            $(".detail").html(data);
            reload_sub_testcase();
            hideWaitDlg();
        },
        error:function(jqXHR,textStatus){
            hideWaitDlg();
            showPromptDlg(jqXHR.responseText);
        }
    });

    $(".selected").removeClass("selected");
    $(this).addClass("selected");
}

function request_path_node_page(node){
    $.ajax({url: "/testcase/Project/path-node/"+$(node).parent().attr("pathid")+"/",
        type:"GET",
        async:false,
        success: function (data, textStatus) {
            $(".detail").html(data);
            reload_sub_path_node();
            hideWaitDlg();
        },
        error:function(jqXHR,textStatus){
            hideWaitDlg();
            showPromptDlg(jqXHR.responseText);
        }
    });
}

function path_node_click_bound(){
    showWaitDlg();
    request_path_node_page(this);
    $(".selected").removeClass("selected");
    $(this).parent().addClass("selected");
}
$(document).ready(function(){
    $(".testcase").click(testcase_click_bound);
    $(".path-node b").click(path_node_click_bound);

    $("#add_root_item").click(function(){
        $.ajax({url: window.location.pathname+"add-root/",
            type:"GET",
            async:false,
            success: function (data, textStatus) {
                $(".detail").html(data);
                $("#add_root_path_node_form").submit(function(){
                    showWaitDlg();
                    $.ajax({url: window.location.pathname+"add-root/",
                        async:false,
                        type: 'POST',
                        data:$(this).serialize(),
                        success: function(data, textStatus) {
                            $("#project_detail").append(data);
                            var new_path_node = $("#project_detail").children(".path-node").last().children("b").first();
                            new_path_node.click(path_node_click_bound);
                            new_path_node.click();
                        },
                        error:function(jqXHR,textStatus){
                            hideWaitDlg();
                            showPromptDlg(jqXHR.responseText);
                        }
                    });
                });
                hideWaitDlg();
            },
            error:function(jqXHR,textStatus){
                hideWaitDlg();
                showPromptDlg(jqXHR.responseText);
            }
        });
    })
});


