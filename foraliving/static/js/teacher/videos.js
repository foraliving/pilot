$(document).ready(function () {
    $(function () {
        $('.status').bootstrapToggle();
    })
    $("#classname").change(function () {
        class_id = $("#classname").val();
        location.href = "/foraliving/teacher/videos/?class=" + class_id
    });
    $(".status").change(function () {
        var video_id = $(this).attr('id');
        var status = $(this).prop('checked');
        var flag_id = (status) ? 0 : 1;
        var url = "/foraliving/video/update/" + video_id + "/" + flag_id + "/";
        $.ajax({
            method: "GET",
            url: url,
            async: true,
            contentType: "application/json"
        }).done(function (data) {
        });
    });
});