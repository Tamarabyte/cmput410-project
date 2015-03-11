$(function() {
    $(document).ready(function (){
        $(".add_comment_button").click(showCommentForm);
    });

    var base_comment_url = "/post/";
    var commentPostGUID;

    var comment_form_options = {
        success: commentSuccess,
        dataType: "json",
        error: ajaxErrorComment,
        clearForm : false,
        type : "PUT",
        beforeSubmit : beforeSubmitComment
    }

    $('#comment-form').ajaxForm(comment_form_options);

    function beforeSubmitComment(arr, form, options) {
        console.log(options["url"]);
        options["url"] = base_comment_url + $("#comment-form").data("postGUID") +"/create/" + $("#comment-guid").val();
        console.log(options["url"]);
    }

    function commentSuccess(response, status, xhr, form) {
        var postGUID = $("#comment-form").data("postGUID");
        $('#comment-form').html(response["form"]);
        $('#' + postGUID).before(response["comment"]);
        $("#comment_form_html").hide();
        $(".add_comment_button").show();
        time = response['time'];
    }

    function ajaxErrorComment(xhr, errmsg, err) {
        var response;
        console.log(xhr.status + ": " + xhr.responseText);
        response = JSON.parse(xhr.responseText);
        $('#comment-form').html(response["form"]);
    }
});