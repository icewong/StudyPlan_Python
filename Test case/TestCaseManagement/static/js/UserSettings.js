/*! liu_hui */

function checkPasswordMatch() {
    var password = $("#newpwd").val();
    var confirmPassword = $("#confirmpwd").val();

    if (password != confirmPassword)
        $("#pwdErr").html("The passwords do not match!");
    else $("#pwdErr").html("&nbsp");
}

$(document).ready(function () {
    $("#confirmpwd").keyup(checkPasswordMatch);

    $("form").submit(function (event) {
        $.ajax({
            url: window.location.pathname,
            type: 'POST',
            async:false,
            data: $(this).serialize(),
            success: function (data, textStatus) {
                $("#contentArea").html(data);
            },
            error: function (jqXHR, textStatus) {
                $("#pwdErr").html(jqXHR.responseText);
            }
        });

        return false;
    });

});


