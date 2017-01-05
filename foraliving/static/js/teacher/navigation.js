$(document).ready(function () {
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
                opt.val("A0");
                opt.text("Select an option");
                $('#options').append(opt);
                var opt = $('<option />');
                opt.val("A1");
                opt.text("New Assignment");
                $('#options').append(opt);
                var opt = $('<option />');
                opt.val("B2");
                opt.text("Delete Class");
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


    $("#options").change(function () {
        if ($("#options").val() != "A0") {
            if ($("#options").val() == "A1") {

            }
            else if ($("#options").val() == "B2") {

            }
            else {
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
                        'data': data_s,
                        select: {
                            style: 'multi'
                        },
                        "columnDefs": [{
                            "targets": 0,
                            'checkboxes': {
                                'selectRow': true
                            }
                        }, {
                            "targets": 1,
                            "render": function (data, type, full, meta) {
                                return "<div>" + full[1] + "<a href=''> (" + full[4] + ")</a></div>";
                            }
                        }, {
                            "targets": 4,
                            "render": function (data, type, full, meta) {
                                return full[5];
                            }
                        }
                        ]
                    });
                });

            }
        }
        else if ($("#company").val() == 0) {

        }
    })
    ;
})
;