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
            // $('#' + comment['postGUID']).before(genComment(comment.comment));
        });
        time = response['time'];
    }

    function genComment(comment) { // This is now useless because we are caching other groups posts... I'll leave it here anyways though
        var time = new Date(comment.pubDate);
        return ''+
                '<div class="row">'+
                    '<div class="well comment-block">'+
                        '<span class="comment-author">'+
                            '<a href="'+ comment.author_url +'">'+
                            comment.author.displayname +
                            '</a>'+
                        '</span>'+
                        '<span class="comment-date pull-right">'+ time.toDateString() + ' '+ time.toLocaleTimeString() +'</span>'+
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