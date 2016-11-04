$(document).ready(function () {
    $('#question2').hide();
    $("input[name='question1']").change(function (event) {
        if ($("input[name='question1']:checked").val() == 2) {
            alert("For the time being, the option is not available");
            $('#question2').hide();
        }
        else {
            $('#question2').show();
        }
    });

    $("input[name='question2']").change(function (event) {
        if ($("input[name='question2']:checked").val() == 1) {
            alert("For the option, the option is not available");
        }
        else {
            $('#question2').show();
        }
    });

    $('html').on('click', '#next', function (e) {
        e.preventDefault();
        if ($("input[name='question2']:checked").val() == 2 || $("input[name='question2']:checked").val() == 3){
            window.location.href = '/foraliving/setup/';
        }
        else {
            alert ("Please, select one option valid")
        }
    });


});
