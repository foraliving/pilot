$(document).ready(function () {


    $('html').on('click', '.delete_group', function (e) {
        ;
        var group_id = e.target.id;
        $('#delete-modal').modal();
        $('.confirm-delete-modal', '#delete-modal').attr('id', 'group_id-' + group_id);
        $('#myModalLabelDelete').text("Are you sure you want to remove this group?")
        e.preventDefault();
    });

    $('body').on('click', 'button.confirm-delete-modal', function (e) {
        var id = e.target.id.split('-')[1];
        var class_id = $("#classname").val();
        var assignment = $("#assignment").val();
        $.ajax({
            type: "POST",
            url: "/foraliving/group/delete/",
            data: {'group_id': id},
        }).done(function (data) {
            $("#delete-modal").modal("hide");
            window.location.href = '/foraliving/teacher/class/?class=' + class_id + "&assignment=" + assignment;

        });
    });

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