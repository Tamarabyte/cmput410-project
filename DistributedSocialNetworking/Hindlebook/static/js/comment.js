$(function() {
    $(document).ready(function (){
        $(".add_comment_button").click(showCommentForm);
    });

    var base_comment_url = "/post/";
    var commentPostUUID;

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
        options["url"] = base_comment_url + $("#comment-form").data("postUUID") +"/create/" + $("#comment-uuid").val();
        console.log(options["url"]);
    }

    function commentSuccess(response, status, xhr, form) {
        console.log("Form was valid!");
        console.log(response["comment"]);
        var postUUID = $("#comment-form").data("postUUID");
        $('#comment-form').html(response["form"]);
        $('#comment-form').clearForm();
        $('#' + postUUID).before(response["comment"]);
        $("#comment_form_html").hide();
        $(".add_comment_button").show();
    }

    function ajaxErrorComment(xhr, errmsg, err) {
        var response;
        console.log(xhr.status + ": " + xhr.responseText);
        response = JSON.parse(xhr.responseText);
        $('#comment-form').html(response["form"]);
    }

    function showCommentForm(event) {
        var data = $(this).attr("data-postUUID");
        console.log(data);

        $(".add_comment_button").show();
        $(this).hide();
        $("#comment_form_html").hide();
        $("#"+ data ).after($("#comment_form_html"))
        $("#comment_form_html").show();
        $("#comment-form").data("postUUID", data);
        console.log($("#comment-form").data("postUUID"));
    };

});