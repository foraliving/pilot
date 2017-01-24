$(document).ready(function () {
    //method to validate the T9 Form
    $(document).on('click', '#assign-volunteer-id', function (e) {
        var modal = $("#createInterview").validate({
            onkeyup: false,
            focusout: false,
            focusInvalid: false,
            submitHandler: function (form) {
                assignVolounteer();
            },
            errorClass: "my-error-class",
            errorPlacement: function (error, element) {
                if (element.attr("name") == "options")
                    error.appendTo('#errors');
                else
                    error.insertAfter(element);
            },
            rules: {
                classname: {
                    required: {
                        depends: function (element) {
                            return ($("#classname").val() == 0);
                        }
                    },
                },
                assignment: {
                    required: true
                    ,
                },
                options: {
                    required: true
                }
            },
            messages: {
                classname: {
                    required: "The Class Name is required"
                },
                options: {
                    required: "Select an Student or Group"
                },
                assignment: {
                    required: "The Assignment is required"
                }
            }
        });
    });

    //function to assign a volunteer in one interview
    function assignVolounteer() {
        var class_id = $("#classname").val();
        var volunteer_id = $('#volunteer_id').val();
        var assignment = $('#assignment').val();
        var option = $('input[name=options]:checked').val();
        var result = option.charAt(0);
        var new_option = option.substr(1);
        $.ajax({
            type: "POST",
            url: "/foraliving/teacher/interview-volunteer/create/",
            data: {'assignment': assignment, 'result': result, 'new_option': new_option, 'volunteer_id': volunteer_id},
        }).done(function (data) {
            window.location.href = '/foraliving/teacher/class/?class=' + class_id + "&assignment=" + assignment;
        });

    }

    //method to detect the changes in the class select
    $("#classname").change(function () {
        var class_id = $("#classname").val();
        var url = "/foraliving/get-assignment/" + class_id + "/";
        $.ajax({
            method: "GET",
            url: url,
            contentType: "application/json"
        }).done(function (data) {
            $("#assignment").html("");
            $("#assignment").selectpicker('refresh');


            $.each(data.results, function (id, data) {
                var opt = $('<option />');
                opt.val(data.id);
                opt.text(data.title);
                $('#assignment').append(opt);
            });

            var result = $('#result');
            result.html('');
            var result = $('#groups');
            result.html('');

            var assignment_id = $("#assignment").val();
            $("#assignment").selectpicker('refresh');
        });
        return false;
    });

    //method to detect the changes in the assignment select
    $("#assignment").change(function () {
        var assignment_id = $("#assignment").val();
        $.ajax({
            method: "GET",
            url: "/foraliving/get/student-list/" + assignment_id,
            contentType: "application/json"
        }).done(function (data) {

            if (data != "") {
                result.append('<h4 style="text-align: center";> Students </h4>')
            }

            $.each(data, function (id, data) {
                variable = "";
                variable = '<label><input type="radio" name="options" value="a' +
                    data.pk + '" /> ' + data.fields.first_name + " " + data.fields.last_name + '</label>';
                result.append(variable);
                result.append("</br>")
            });
        });

        var result = $('#groups');
        result.html('');

        //method to generate the group and student list
        $.ajax({
            method: "GET",
            url: "/foraliving/get/student-group/" + assignment_id,
            contentType: "application/json"
        }).done(function (data) {


            if (data != "") {
                result.append('<h4 style="text-align: center";> Groups </h4>')
            }

            $.each(data, function (id, data) {
                variable = "";
                variable = '<label><input type="radio" name="options" value="b' +
                    data.pk + '" /> ' + data.fields.name + '</label>';
                result.append(variable);
                result.append("</br>")
            });
        });
        return false;
    });
});