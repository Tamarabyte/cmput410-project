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
        options["url"] = base_url + $("#guid").val();
        console.log(options["url"]);
    }

    function postSuccess(response, status, xhr, form) {
        console.log("Form was valid!");
        $('#post-form').html(response["form"]);
        $('#post-form').clearForm();
        $("#id_visibility").val("PUBLIC")
        $("#id_content_type").val("text/plain")
        $('#stream').prepend(response["post"]);
        $('.add_comment_button[data-postGUID="' + response["created_guid"] +'"]').click(showCommentForm);
        time = response['time'];
        magicSuggest();
    }

    function ajaxError(xhr, errmsg, err) {
        var response;
        console.log(xhr.status + ": " + xhr.responseText);
        response = JSON.parse(xhr.responseText);
        $('#post-form').html(response["form"]);
        magicSuggest();
    }
    
});