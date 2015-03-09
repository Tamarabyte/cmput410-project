$(function() {
    /* Post Ajax */
    var base_url = "/post/create/";

    var form_options = {
        success: postSuccess,
        dataType: "json",
        error: ajaxError,
        clearForm : false,
        type : "PUT",
        beforeSubmit : beforeSubmit
    }

    $('#post-form').ajaxForm(form_options);

    function beforeSubmit(arr, form, options) {
        console.log(options["url"]);
        options["url"] = base_url + $("#uuid").val();
        console.log(options["url"]);
    }

    function postSuccess(response, status, xhr, form) {
        console.log("Form was valid!");
        $('#post-form').html(response["form"]);
        $('#post-form').clearForm();
        $('#stream').prepend(response["post"]);
        $('.add_comment_button[data-postUUID="' + response["created_uuid"] +'"]').click(showCommentForm);
    }

    function ajaxError(xhr, errmsg, err) {
        var response;
        console.log(xhr.status + ": " + xhr.responseText);
        response = JSON.parse(xhr.responseText);
        $('#post-form').html(response["form"]);
    }

    /* End Post Ajax */
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