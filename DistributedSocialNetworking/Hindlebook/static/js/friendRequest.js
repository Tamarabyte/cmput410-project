function follow() {
    var base_url = "/api/follow";
    var friend = {
                "id": $("#friend-uuid").val(),
                "host": $("friend-host").val(),
                "displayname": $("#friend-dn").val(),
                "url": $("#friend-url").val()
            };
    var author = {
                "id":$("#author-uuid").val(),
                "host":$("#author-host").val(),
                "displayname":$("#author-dn").val()
            };
   

    var jsonData = {
            "query": "friendrequest",
            "author": author,
            "friend": friend
        };

    console.log("trying to follow lol")

    // THIS NEEDS TO BE RESOLVED, just a quick hack
    // to at least get it working... basically
    // JSON when stringifying everything is adding
    // backslashes so I'm fucking removing them fuck that
    // it was making the IDs not match up
    var myJSONString = JSON.stringify(jsonData);
    var regex = new RegExp("/", 'g');
    var myEscapedJSONString = myJSONString.replace(regex,"");
    $.ajax({
        success: requestSuccess,
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myEscapedJSONString,
        beforeSubmit : beforeSubmit
    })

    function beforeSubmit(arr, form, options) {
        console.log("setting url");
        options["url"] = base_url;
        console.log(options["data"]);
        console.log(options["url"]);
    }

    function ajaxError(xhr, errmsg, err) {
        var response;

        console.log("we errored out yo");
        console.log(xhr.responseText)

    }
    
    function requestSuccess(response, status, xhr, form) {
        console.log("follow request sent!");
        isFollowing = 1;
        // On request success we succesfully followed this person...
        // Time to change icon look and functionality.
        $("#follow-icon").toggleClass("icon-screenshot icon-tl-undo");
        $("#follow-icon").attr("onclick","unfollow()");
  
    };
}

function unfollow() {
    var base_url = "/api/unfollow";
    var friend = {
                "id": $("#friend-uuid").val(),
                "host": $("friend-host").val(),
                "displayname": $("#friend-dn").val(),
                "url": $("#friend-url").val()
            };
    var author = {
                "id":$("#author-uuid").val(),
                "host":$("#author-host").val(),
                "displayname":$("#author-dn").val()
            };
   

    var jsonData = {
            "query": "friendrequest",
            "author": author,
            "friend": friend
        };


    // THIS NEEDS TO BE RESOLVED, just a quick hack
    // to at least get it working... basically
    // JSON when stringifying everything is adding
    // backslashes so I'm fucking removing them fuck that
    // it was making the IDs not match up
    var myJSONString = JSON.stringify(jsonData);
    var regex = new RegExp("/", 'g');
    var myEscapedJSONString = myJSONString.replace(regex,"");
    $.ajax({
        success: requestSuccess,
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myEscapedJSONString,
        beforeSubmit : beforeSubmit
    })

    function beforeSubmit(arr, form, options) {
        console.log("setting url");
        options["url"] = base_url;
        console.log(options["data"]);
        console.log(options["url"]);
    }

    function ajaxError(xhr, errmsg, err) {
        var response;

        console.log("we errored out yo");
        console.log(xhr.responseText)

    }
    function requestSuccess(response, status, xhr, form) {
        console.log("in unfollow")
        isFollowing = 0;
        $("#follow-icon").toggleClass("icon-screenshot icon-tl-undo");
        $("#follow-icon").attr("onclick","follow()");
  
    };

}

function friend() {
    var base_url = "/api/friendrequest";
    var friend = {
                "id": $("#friend-uuid").val(),
                "host": $("friend-host").val(),
                "displayname": $("#friend-dn").val(),
                "url": $("#friend-url").val()
            };
    var author = {
                "id":$("#author-uuid").val(),
                "host":$("#author-host").val(),
                "displayname":$("#author-dn").val()
            };
   

    var jsonData = {
            "query": "friendrequest",
            "author": author,
            "friend": friend
        };

    console.log("trying to friend request lol")

    // THIS NEEDS TO BE RESOLVED, just a quick hack
    // to at least get it working... basically
    // JSON when stringifying everything is adding
    // backslashes so I'm fucking removing them fuck that
    // it was making the IDs not match up
    var myJSONString = JSON.stringify(jsonData);
    var regex = new RegExp("/", 'g');
    var myEscapedJSONString = myJSONString.replace(regex,"");
    $.ajax({
        success: requestSuccess,
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myEscapedJSONString,
        beforeSubmit : beforeSubmit
    })

    function beforeSubmit(arr, form, options) {
        console.log("setting url");
        options["url"] = base_url;
        console.log(options["data"]);
        console.log(options["url"]);
    }

    function ajaxError(xhr, errmsg, err) {
        var response;

        console.log("we errored out yo");
        console.log(xhr.responseText)

    }
    
    function requestSuccess(response, status, xhr, form) {
        console.log("friend request sent!");
        // On request success we succesfully followed this person...
        // Time to change icon look and functionality.
        if (isFollowing == 0) {
            follow();
        }
        $("#friend-icon").toggleClass("icon-favourite-3 icon-broken-heart");
        $("#friend-icon").attr("onclick","unfriend()");
        if (authorHost != "localhost") {
            console.log("wtf")
            $.ajax({
                clearForm : false,
                contentType: "application/json; charset=utf-8",
                //error: ajaxError,
                type : "POST",
                url : authorHost + "/api/friendrequest",
                data : myEscapedJSONString,
                success : function(returnHtml) {
                    console.log("Succesfully sent friend reuqest to host: " + authorHost)
                }
            })
        }
    };
}

function unfriend() {
    var base_url = "/api/unfriend";
    var friend = {
                "id": $("#friend-uuid").val(),
                "host": $("friend-host").val(),
                "displayname": $("#friend-dn").val(),
                "url": $("#friend-url").val()
            };
    var author = {
                "id":$("#author-uuid").val(),
                "host":$("#author-host").val(),
                "displayname":$("#author-dn").val()
            };
   

    var jsonData = {
            "query": "friendrequest",
            "author": author,
            "friend": friend
        };


    // THIS NEEDS TO BE RESOLVED, just a quick hack
    // to at least get it working... basically
    // JSON when stringifying everything is adding
    // backslashes so I'm fucking removing them fuck that
    // it was making the IDs not match up
    var myJSONString = JSON.stringify(jsonData);
    var regex = new RegExp("/", 'g');
    var myEscapedJSONString = myJSONString.replace(regex,"");
    $.ajax({
        success: requestSuccess,
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myEscapedJSONString,
        beforeSubmit : beforeSubmit
    })

    function beforeSubmit(arr, form, options) {
        console.log("setting url");
        options["url"] = base_url;
        console.log(options["data"]);
        console.log(options["url"]);
    }

    function ajaxError(xhr, errmsg, err) {
        var response;

        console.log("we errored out yo");
        console.log(xhr.responseText)

    }
    function requestSuccess(response, status, xhr, form) {
        console.log("Succesfully Unfriended")
        $("#friend-icon").toggleClass("icon-favourite-3 icon-broken-heart");
        $("#friend-icon").attr("onclick","friend()");
  
    };

}

