$(function() {
    /* Post Ajax */
    var options = {
        success: getSuccess,
        dataType: "JSON",
        data: {'last_time':time },
        error: ajaxError,
        type : "POST",
        beforeSubmit : beforeSubmit
    }

    function beforeSubmit(arr, form, options) {
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