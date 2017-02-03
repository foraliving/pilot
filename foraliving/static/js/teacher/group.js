$(document).ready(function () {

    $('html').on('click', '.delete_group', function (e) {
        ;
        var group_id = e.target.id;
        $('#delete-modal').modal();
        $('.confirm-delete-modal', '#delete-modal').attr('id', 'group_id-' + group_id);
        $('#myModalLabelDelete').text("Are you sure you want to remove this group?")
        e.preventDefault();
    });


    $('html').on('click', '.edit-group', function (e) {
        var group_id = e.target.id;
        $('.update_group', '#edit_group').attr('id', 'group_id-' + group_id);
        var result = [];
        $.ajax({
            type: "POST",
            url: "/foraliving/group/members/",
            data: {'group_id': group_id},
        }).done(function (data) {
            $("#students_name > tbody").html("");
            $.each(data, function (id, data) {
                var opt = $('<option />');
                opt.val(data.pk);
                opt.text(data.fields.first_name + ' ' + data.fields.last_name);
                $('#pre-selected-options').append(opt);
                result.push(data.pk.toString());
            });
            $('input[name=group_name]').val($("#group_name").text());

            var class_id = $("#classname").val();
            $.ajax({
                type: "POST",
                url: "/foraliving/class/members/",
                data: {'class_id': class_id, 'group_id': group_id},
            }).done(function (data) {
                $.each(data, function (id, data) {
                    var opt = $('<option />');
                    opt.val(data.pk);
                    opt.text(data.fields.first_name + ' ' + data.fields.last_name);
                    $('#pre-selected-options').append(opt);
                });
                $('#pre-selected-options').multiSelect({
                    selectableHeader: "<div class='custom-header'>Student's Class</div>",
                    selectionHeader: "<div class='custom-header'>Student's Group</div>",
                });
                $('input[name=group_name]').val($("#group_name").text());

                result.forEach(function (element) {
                    $('#pre-selected-options').multiSelect('select', String(element));
                });
                $('#edit_group').modal();
            });
        });

    });

    $.validator.addMethod("uniqueGroup", function () {
        var group = $("input[name=group_name]").val().trim();
        var group_id = $('input[name=group_name]').attr('id');
        var valid = false
        $.ajax({
            type: "GET",
            async: false,
            url: "/foraliving/unique-group-edit/",
            data: "group=" + group + "&group_id=" + group_id,
            dataType: "json",
            async: false,
            success: function (response) {
                valid = !response;
            }
        });
        return valid;


    }, "This group name is already taken! Try another.");


    $(document).on('click', '.update_group', function (e) {
        var modal = $("#editGroup").validate({
            onkeyup: false,
            focusout: false,
            focusInvalid: false,
            submitHandler: function (form) {
                event.preventDefault();
                updateGroup();
            },
            errorClass: "my-error-class",
            rules: {
                group_name: {
                    required: true,
                    uniqueGroup: true
                }
            },
            messages: {
                group_name: {
                    required: "The Group name is required"
                }
            }
        });
    });

    function updateGroup() {
        var group_id = $('input[name=group_name]').attr('id');
        var group_name = $('input[name=group_name]').val().trim();;
        var students = $('#pre-selected-options').val();
        $.ajax({
            type: "POST",
            url: "/foraliving/assign_group/edit/",
            data: {'group_name': group_name, 'students[]': students, 'group_id' : group_id},
        }).done(function (data) {
            $('#edit_group').modal("hide");
            location.reload();
        });


    }


    $('body').on('click', 'button.confirm-delete-modal', function (e) {
        var id = e.target.id.split('-')[1];
        var class_id = $("#classname").val();
        var assignment = $("#assignment").val();
        $.ajax({
            type: "POST",
            url: "/foraliving/group/update/",
            data: {'group_name': id},
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
})
;