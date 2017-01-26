$(document).ready(function () {

    $(".status").change(function () {
        var video_id = $(this).val();
        if ($(this).is(':checked')) {
            var flag_id = 0;
            $(this).siblings('label').html('Approved');
            $(this).parent().removeClass('link').addClass('page-title');

        }
        else {
            flag_id = 1;
            $(this).siblings('label').html('Approve');
            $(this).parent().removeClass('page-title').addClass('link');

        }


        var url = "/foraliving/video/update/" + video_id + "/" + flag_id + "/"
        $.ajax({
            method: "GET",
            url: url,
            async: true,
            contentType: "application/json"
        }).done(function (data) {
            if (data == 0) {
            $(".alert-videos").hide();
            }
            else {
                $(".alert-videos").show();
                $(".alert-videos").text("You have " + data + " video(s) waiting to be approved")
            }

        });
    });
});