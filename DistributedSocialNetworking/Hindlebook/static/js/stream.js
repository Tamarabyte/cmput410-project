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
        $.each(response['posts'], function(count, post){
            // Generate posts
            $('#stream').prepend(post["post"]);
            $('.add_comment_button[data-postGUID="' + post["created_guid"] +'"]').click(showCommentForm);
        });
        $.each(response['comments'], function(count, comment){
            $('#' + comment['postGUID']).before(comment['comment']);
            $('#' + comment['postGUID']).before(genComment(comment.comment));
        });
        time = response['time'];
    }

    function genComment(comment) {
        return ''+
'<div class="row">'+
    '<div class="well comment-block">'+
        '<span class="comment-author">'+
            '<a href="'+ 'a place'/* author url */ +'">'+
            comment.author.displayname +
            '</a>'+
        '</span>'+
        '<span class="comment-date pull-right">'+ comment.pubDate +'</span>'+
        ': <span class="comment-comment">'+ comment.comment+'</span>'+
    '</div>'+
'</div>';
    }

    function ajaxError(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText);
    }

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