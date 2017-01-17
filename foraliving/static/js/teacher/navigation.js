$(document).ready(function () {
    var user_table = $("#data-table").DataTable({
        'destroy': true,
        "paging": false,
    });

    var assignment_id = $("#assignment_hidden").val();
    var class_id = $("#class_hidden").val();
    if (class_id != null) {
        $('#classname').val(class_id);
        $('#classname').selectpicker('refresh');
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
            $('#options').val(assignment_id);
            $("#options").selectpicker('refresh');
        });
    }


    getClass(assignment_id, class_id);


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
            });

            return false;
        } else if ($("#company").val() == 0) {

        }
    });

    $("#use_group").change(function () {
        if ($('#use_group').is(':checked')) {
            $("#group_name").hide();
            $('#group').selectpicker('show');
        } else {
            $("#group_name").show();
            $('#group').selectpicker('hide');
        }
    });

    $('html').on('click', '#add_to_group', function (e) {
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
                url: "/foraliving/groups/",
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
            });
        });
        e.preventDefault();
        $("#group_name").hide();
        $("#use_group").prop("checked", true);
        $('input[name=group_name]').val("");
        $('#group').selectpicker('show');
        $('#add_group').modal();
        $('input[name=data]').val(selected);
    });

    $("#add_group").on("shown.bs.modal", function () {
        //will be executed everytime #item_modal is shown
        var formID = $('#addGroup');
        $(this).hide().show(); //hide first and then show here
    });

    $('#add_group').on('hidden.bs.modal', function () {
        var formID = $('#addGroup');
        formID.validate().resetForm();
    })


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

    function sendGroup() {
        var selected = [];
        $('.checkboxes input:checked').each(function () {
            selected.push($(this).attr('value'));
        });
        var group = $('#group').val();
        var group_name = $('input[name=group_name]').val()
        $.ajax({
            type: "POST",
            url: "/foraliving/assign_group/",
            data: {'selected[]': selected, 'group': group, 'group_name': group_name},
        }).done(function (data) {
            $('#add_group').modal('toggle');
            var assignment_id = $("#options").val();
            var class_id = $("#classname").val();
            getClass(assignment_id, class_id);
        });
    }


    $("#options").change(function () {
        if ($("#options").val() != "A0") {
            if ($("#options").val() == "A1") {

            }
            else if ($("#options").val() == "B2") {

            }
            else {
                var assignment_id = $("#options").val();
                var class_id = $("#classname").val();
                getClass(assignment_id, class_id);

            }
        }
        else if ($("#company").val() == 0) {

        }
    });


    function getAssignment() {
        var assignment_id = $("#options").val();

        $.ajax({
            method: "GET",
            url: "/foraliving/get-student/" + assignment_id + "/",
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
                    "render": function (data, type, full, meta) {
                        return '<div> </div>';
                    }
                }, {
                    "targets": 1,
                    "render": function (data, type, full, meta) {
                        if (full[4] != null) {
                            return "<div>" + full[1] + "<a href=''> (" + full[4] + ")</a></div>";
                        }
                        else {
                            return "<div><a href=''> (" + full[1] + ")</a></div>";
                        }
                    }
                }, {
                    "targets": 3,
                    "render": function (data, type, full, meta) {
                        return full[2];
                    }
                }, {
                    "targets": 4,
                    "render": function (data, type, full, meta) {
                        return full[3];
                    }
                }, {
                    "targets": 2,
                    "render": function (data, type, full, meta) {
                        return "<div> <a href='/foraliving/volunteer/profile/" + full[5] + "/0'>" + full[6] + " " + full[7] + "</a> <i class='fa fa-btn fa-close' style='margin-left: 10px;' title='Delete'></i>" + "</a>" + "</div>";
                    }
                }
                ]
            });
        });
    }


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
                            return "<div>" + full[1] + "<a href=''> (" + full[8] + ")</a></div>";
                        }
                        else {
                            return "<div><a href=''> " + full[1] + "</a></div>";
                        }
                    }
                }, {
                    "targets": 3,
                    "render": function (data, type, full, meta) {
                        return full[2];
                    }
                }, {
                    "targets": 4,
                    "render": function (data, type, full, meta) {
                        return full[3];
                    }
                }, {
                    "targets": 2,
                    "render": function (data, type, full, meta) {
                        if (full[4] != null) {
                            return "<div> <a href='/foraliving/volunteer/profile/" + full[4] + "/0'>" + full[5] + " " + full[6] + "</a> <i class='fa fa-btn fa-close' style='margin-left: 10px;' title='Delete'></i></div>";
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