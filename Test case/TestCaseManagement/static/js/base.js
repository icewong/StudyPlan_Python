
function showPromptDlg(text){
    $("#dlg_prompt .modal-body").html(text);
    $("#dlg_prompt #dlg_prompt_ok").attr("onclick","dlgHide('dlg_prompt')");
    $("#dlg_prompt #dlg_prompt_cancel").hide();
    dlgShow("dlg_prompt");
}
function showWarningDlg(text,click_action){
    $("#dlg_prompt .modal-body").html(text);
    $("#dlg_prompt #dlg_prompt_ok").attr("onclick",click_action);
    $("#dlg_prompt #dlg_prompt_cancel").show();
    dlgShow("dlg_prompt");
}

function hidePrmoptDlg(){
    dlgHide("dlg_prompt");
}


function dlgShow(id){
    $("#"+id).modal({backdrop: 'static'});
}
function dlgHide(id){
    $("#"+id).modal('hide');
}

function showWaitDlg(){
    $("#waiting").show();
}

function hideWaitDlg(){
    $("#waiting").hide();
}

function ajaxBoundCsrf(){
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
}

$(document).ready(function () {
    $('.user').hover(function () {
        $('#userMenu').addClass('show');
    });
    $('#userMenu').hover(function () {
    }, function () {
        var menu = $('#userMenu')[0];
        if (menu.classList.contains('show')) {
            menu.classList.remove('show');
        }
    });
});