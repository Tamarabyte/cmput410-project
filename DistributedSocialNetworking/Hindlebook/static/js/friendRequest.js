function follow(uuid) {
    var icon = $("#follow-icon-" + uuid);
    var base_url = "/api/follow";
    if (isFollowing)
        base_url = "/api/unfollow";

    var friend = {
                "id": $("#friend-uuid-"+ uuid).val(),
                "host": $("#friend-host-"+ uuid).val(),
                "displayname": $("#friend-dn-"+ uuid).val(),
                "url": $("#friend-url-"+ uuid).val()
            };
    var author = {
                "id": userUUID,
                "host": userHost,
                "displayname": userDN
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

        if (removeIfUnfriend) {
            $("#following-"+uuid).hide();
        }
        else {
            if (isFollowing) {
                isFollowing = 0
            }
            else {
                isFollowing = 1
            }
            icon.toggleClass("icon-eye-3 icon-eye-4");
            $(".follow-link").blur();
        }
    };

}

function friend(uuid) {
    var icon = $("#friend-icon-" + uuid);
    var base_url = "/api/friendrequest";
    if (isFriend)
        base_url = "/api/unfriend";
        
    var friend = {
                "id": $("#friend-uuid-" + uuid).val(),
                "host": $("#friend-host-" + uuid).val(),
                "displayname": $("#friend-dn-" + uuid).val(),
                "url": $("#friend-url-"+ uuid).val()
            };
    var author = {
                "id": userUUID,
                "host": userHost,
                "displayname": userDN
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
        console.log(xhr.responseText)

    }
    
    function requestSuccess(response, status, xhr, form) {
        console.log("friend request sent!");
        // On request success we succesfully followed this person...
        // Time to change icon look and functionality.
        if (removeIfUnfriend) {
            $("#friend-"+uuid).hide();
        }
        else {
            if (isFriend) {
                isFriend = 0
            }
            else {
                isFriend = 1
            }
        }
        icon.toggleClass("icon-favourite-3 icon-broken-heart");
        $(".friend-link").blur();
    };
}
