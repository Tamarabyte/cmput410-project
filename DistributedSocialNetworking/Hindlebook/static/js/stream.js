$(function() {
    /* Post Ajax */
    var base_url = "";
    var time = "";

    var options = {
        success: getSuccess,
        dataType: "JSON",
        data: {'last_time':time },
        error: ajaxError,
        type : "POST",
        beforeSubmit : beforeSubmit
    }

    function beforeSubmit(arr, form, options) {
        console.log(options["url"]);
        // options["url"] = base_url + $("#guid").val();
        console.log(options["url"]);
    }

    function getSuccess(response, status, xhr, form) {
        console.log(response);
        $.each(response['posts'], function(count, post){
             $('#stream').prepend(post["post"]);
             $('.add_comment_button[data-postGUID="' + post["created_guid"] +'"]').click(showCommentForm);
        });
        $.each(response['comments'], function(count, comment){
            $('#' + comment['postGUID']).before(comment['comment']);
        });
        time = response['time'];
    }

    function ajaxError(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText);
        }

    /* End Post Ajax */
    function showCommentForm(event) {
        var data = $(this).attr("data-postGUID");
        console.log(data);

        $(".add_comment_button").show();
        $(this).hide();
        $("#comment_form_html").hide();
        $("#"+ data ).after($("#comment_form_html"))
        $("#comment_form_html").show();
        $("#comment-form").data("postGUID", data);
        console.log($("#comment-form").data("postGUID"));
    };
    $.ajax({
            success: getSuccess,
            dataType: "JSON",
            data: {'last_time': time},
            error: ajaxError,
            type : "POST",
            beforeSubmit : beforeSubmit
        });

    setInterval(function() {
        $.ajax({
            success: getSuccess,
            dataType: "JSON",
            data: {'last_time': time},
            error: ajaxError,
            type : "POST",
            beforeSubmit : beforeSubmit});
    }, 2000);

});