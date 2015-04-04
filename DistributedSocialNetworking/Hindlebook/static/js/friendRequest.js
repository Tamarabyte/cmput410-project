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


    var myJSONString = JSON.stringify(jsonData);
    $.ajax({
        success: requestSuccess,
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myJSONString,
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

function friend(uuid, is_pending) {
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
    console.log("friendID: " + $("#friend-uuid-" + uuid).val())
    console.log("Friendhost: " + $("#friend-host-" + uuid).val())
    console.log("trying to friend request lol")

    var myJSONString = JSON.stringify(jsonData);
    console.log("2");
    $.ajax({
        success: requestSuccess,
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myJSONString,
        beforeSubmit : beforeSubmit
    });

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
                var requests = parseInt($("#notifications-badge").text()) - is_pending;
                $("#notifications-badge").text(requests + "");
            }
        }
        
        
        
        
        icon.toggleClass("icon-favourite-3 icon-broken-heart");
        $(".friend-link").blur();
    };
}
