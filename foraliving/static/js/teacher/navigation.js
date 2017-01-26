$(document).ready(function () {
    //definition initial of the datatable
    var user_table = $("#data-table").DataTable({
        'destroy': true,
        "paging": false,
    });

    var assignment_id = $("#assignment_hidden").val();
    var class_id = $("#class_hidden").val();
    if (class_id != 'None') {
        //Verify if exist a class sent how parameter
        $('#classname').val(class_id);
        $('#classname').selectpicker('refresh');
        var url = "/foraliving/get-assignment/" + class_id + "/";
        $.ajax({
            method: "GET",
            url: url,
            contentType: "application/json"
        }).done(function (data) {
            // reload the assignment options
            $("#options").html("");
            $("#options").selectpicker('refresh');

            $("#options").html("");
            var opt = $('<option />');
            opt.val("B2");
            opt.text("Delete Class");
            $('#options').append(opt);

            $('#options').append(opt);
            var opt = $('<option />');
            opt.val("A1");
            opt.text("New Assignment");
            $('#options').append(opt);

            $.each(data.results, function (id, data) {
                var opt = $('<option />');
                opt.val(data.id);
                opt.text(data.title);
                $('#options').append(opt);
            });
            $("#options").selectpicker('refresh');
            $('#options').val(assignment_id);
            $("#options").selectpicker('refresh');

            //get the student in relation with the assignment and ckass
            getClass(assignment_id, class_id);
        });
    }

    //method to verify if the teacher select other class
    $("#classname").change(function () {
        if ($("#classname").val() != 0) {
            var class_id = $("#classname").val();
            var url = "/foraliving/get-assignment/" + class_id + "/";
            $.ajax({
                method: "GET",
                url: url,
                contentType: "application/json"
            }).done(function (data) {
                $("#options").html("");
                $("#options").selectpicker('refresh');

                $("#options").html("");
                var opt = $('<option />');
                opt.val("B2");
                opt.text("Delete Class");
                $('#options').append(opt);

                $('#options').append(opt);
                var opt = $('<option />');
                opt.val("A1");
                opt.text("New Assignment");
                $('#options').append(opt);

                $.each(data.results, function (id, data) {
                    var opt = $('<option />');
                    opt.val(data.id);
                    opt.text(data.title);
                    $('#options').append(opt);
                });
                $("#options").selectpicker('refresh');
                $('#data-table').dataTable().fnClearTable();
            });

            return false;
        } else if ($("#company").val() == 0) {

        }
    });

    //verify if the teacher change the option to "user an existing group"
    $("#use_group").change(function () {
        if ($('#use_group').is(':checked')) {
            $("#group_name").hide();
            $('#group').selectpicker('show');
        } else {
            $("#group_name").show();
            $('#group').selectpicker('hide');
        }
    });

    //method to make the ajax call that get the student list that the teacher want to assign
    $('html').on('click', '#add_to_group', function (e) {
        class_id = $("#classname").val();
        assignment_id = $("#options").val();
        if (assignment_id != "") {

            var selected = [];
            $('.checkboxes input:checked').each(function () {
                selected.push($(this).attr('value'));
            });

            $.ajax({
                type: "POST",
                url: "/foraliving/list-student-group/",
                data: {'selected[]': selected},
            }).done(function (data) {
                $("#students_name > tbody").html("");
                $.each(data, function (id, data) {
                    $('#students_name').append('<tr><td>' + data.fields.first_name + ' ' + data.fields.last_name + '</td></tr>')
                });
                $.ajax({
                    type: "GET",
                    url: "/foraliving/groups/?class_id=" + class_id,
                }).done(function (data) {
                    $("#group").html("");
                    $("#group").selectpicker('refresh');

                    $.each(data, function (id, data) {
                        var opt = $('<option />');
                        opt.val(data.pk);
                        opt.text(data.fields.name);
                        $('#group').append(opt);
                    });
                    $("#group").selectpicker('refresh');

                    e.preventDefault();
                    $("#group_name").hide();
                    $("#use_group").prop("checked", true);
                    $('input[name=group_name]').val("");
                    $('#group').selectpicker('show');
                    $('#add_group').modal();
                    $('input[name=data]').val(selected);
                });
            });
        }
    });

    $("#add_group").on("shown.bs.modal", function () {
        //will be executed everytime #item_modal is shown
        var formID = $('#addGroup');
        $(this).hide().show(); //hide first and then show here
    });

    $('#add_group').on('hidden.bs.modal', function () {
        var formID = $('#addGroup');
        //reset the form when the modal is open
        formID.validate().resetForm();
    })


    //method to verify the unique group
    $.validator.addMethod("uniqueGroup", function () {
        var group = $("input[name=group_name]").val();
        var valid = false
        $.ajax({
            type: "GET",
            async: false,
            url: "/foraliving/unique-group/",
            data: "group=" + group,
            dataType: "json",
            async: false,
            success: function (response) {
                valid = !response;
            }
        });
        return valid;


    }, "This group name is already taken! Try another.");


    //method to validate the group form
    $(document).on('click', '#save_group', function (e) {
        var modal = $("#addGroup").validate({
            onkeyup: false,
            focusout: false,
            focusInvalid: false,
            submitHandler: function (form) {
                sendGroup();
            },
            errorClass: "my-error-class",
            rules: {
                group: {
                    required: {
                        depends: function (element) {
                            return $("#use_group").is(":checked");
                        }
                    },
                },
                group_name: {
                    required: {
                        depends: function (element) {
                            return $("#use_group").is(":not(:checked)");
                        }
                    },
                    uniqueGroup: true
                },
                data: {
                    required: true
                }
            },
            messages: {
                group_name: {
                    required: "The Group name is required"
                },
                data: {
                    required: "The student list is required"
                }
            }
        });
    });

    //method to assign students to group
    function sendGroup() {
        var selected = [];
        $('.checkboxes input:checked').each(function () {
            selected.push($(this).attr('value'));
        });
        var class_id = $("#classname").val();
        var group = $('#group').val();
        var group_name = $('input[name=group_name]').val()
        if (selected != null) {
            $.ajax({
                type: "POST",
                url: "/foraliving/assign_group/",
                data: {'selected[]': selected, 'group': group, 'group_name': group_name, 'class_id': class_id},
            }).done(function (data) {
                $('#add_group').modal('toggle');
                var assignment_id = $("#options").val();
                getClass(assignment_id, class_id);
            });
        }
    }

    //method to delete a volunteer
    $(document).on('click', '.delete-volunteer', function (e) {
        var interview_id = e.target.id;
        $('#delete-modal').modal();
        $('.confirm-delete-modal', '#delete-modal').attr('id', 'interview-' + interview_id);
        $('#myModalLabelDelete').text("Are you sure you want to remove this volunteer?")
        e.preventDefault();
    });


    $('body').on('click', 'button.confirm-delete-modal', function (e) {
        var option = e.target.id.split('-')[0];
        var id = e.target.id.split('-')[1];
        var class_id = $("#classname").val();
        var assignment_id = $("#options").val();

        if (option == "interview") {
            $.ajax({
                type: "POST",
                url: "/foraliving/interview/delete/",
                data: {'interview_id': interview_id},
            }).done(function (data) {
                $("#delete-modal").modal("hide");
                getClass(assignment_id, class_id);
            });
        }
        else if (option == "class") {
            $.ajax({
                type: "POST",
                url: "/foraliving/class/delete/",
                data: {'class_id': class_id},
            }).done(function (data) {
                $("#delete-modal").modal("hide");
                window.location.href = '/foraliving/teacher/class/';
            });
        }
    });

    //method to verify the changes in the assignment select
    $("#options").change(function () {
        if ($("#options").val() == "A1") {

        }
        else if ($("#options").val() == "B2") {
            var class_id = $("#classname").val();
            $('#delete-modal').modal();
            $('.confirm-delete-modal', '#delete-modal').attr('id', 'class-' + class_id);
            $('#myModalLabelDelete').text("Are you sure you want to remove this class?")

        }
        else {
            var assignment_id = $("#options").val();
            var class_id = $("#classname").val();
            getClass(assignment_id, class_id);

        }
    });

    //method to display the stuents in relation with the class and assignment
    function getClass(assignment_id, class_id) {
        var url = "/foraliving/student-list/" + class_id + "/" + assignment_id + "/";
        $.ajax({
            method: "GET",
            url: url,
            contentType: "application/json"
        }).done(function (data) {
            var data_s = data.results;

            $('#data-table').dataTable().fnClearTable();
            var user_table = $("#data-table").DataTable({
                'destroy': true,
                "paging": false,
                'data': data_s,
                "columnDefs": [{
                    "targets": 0,
                    "searchable": false,
                    "orderable": false,
                    "className": 'dt-body-center',
                    "render": function (data, type, full, meta) {
                        if (full[8] == null || (full[8] == full[1] && full[4] == "Add")) {
                            return '<div class="checkboxes"><input type="checkbox" name="student" value="' + full[0] + '"></div>';
                        }
                        else {
                            return '<div> </div>';
                        }
                    }
                }, {
                    "targets": 1,
                    "render": function (data, type, full, meta) {
                        if (full[8] != null && full[8] != full[1]) {
                            return "<div>" + full[1] + "<a href='/foraliving/teacher/group/" + class_id + "/" + assignment_id + "/" + full[9] + "/'>  (" + full[8] + ")</a></div>";
                        }
                        if (full[9] == null) {
                            return "<div>" + full[1] + "</div>";
                        }
                        else {
                            return "<div><a href='/foraliving/teacher/group/" + class_id + "/" + assignment_id + "/" + full[9] + "/'> " + full[1] + "</a></div>";
                        }
                    }
                }, {
                    "targets": 4,
                    "render": function (data, type, full, meta) {
                        return full[2];
                    }
                }, {
                    "targets": 2,
                    "render": function (data, type, full, meta) {
                        if (full[11] == 0 && full[12] == 0) {
                            return "<div style='color:black;'>" + full[11] + "</div>"
                        }
                        else if (full[11] == 0 && full[12] != 0) {
                            return "<div style='color:#99c64c; font-weight: 600;'>" + full[12] + "</div>"
                        }
                        else {
                            return "<div style='color:red; font-weight: 600;'>" + full[11] + "</div>"
                        }
                    }
                }, {
                    "targets": 5,
                    "render": function (data, type, full, meta) {
                        return full[3];
                    }
                }, {
                    "targets": 3,
                    "render": function (data, type, full, meta) {
                        if (full[4] != null && (full[12] == 0 && full[11] == 0)) {
                            return "<div> <a href='/foraliving/volunteer/profile/" + full[4] + "/0'>" + full[5] +
                                " " + full[6] + "</a> <i class='fa fa-btn fa-close delete-volunteer' id=' " + full[10] + "'" +
                                " style='margin-left: 10px;' title='Delete'></i></div>";
                        }
                        else if (full[4] != null) {
                            return "<div> <a href='/foraliving/volunteer/profile/" + full[4] + "/0'>" + full[5] +
                                " " + full[6] + "</a></div>";
                        }
                        else {
                            return "<a href='/foraliving/teacher/volunteer/assign/" + full[0] + "/" + assignment_id + "/'> Add </a>";
                        }
                    }
                }
                ]
            });
        });
    }
});