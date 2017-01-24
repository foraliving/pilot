$(document).ready(function () {
    $("#classname").change(function () {
        class_id = $("#classname").val();
        location.href = "/foraliving/teacher/videos/?class=" + class_id
    });
});