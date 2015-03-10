$(function() {
    
    /* Post Ajax */
    console.log("stuffs happening");
    var base_url = "/api/friendrequest";
    var jsonData = {
            "query": "friendrequest",
            "author": {
                "id":$("#author-uuid").val(),
                "host":$("#author-host").val(),
                "displayname":$("#author-dn").val()
            },
            "friend":{
                "id": $("#friend-uuid").val(),
                "host": $("friend-host").val(),
                "displayname": $("#friend-dn").val(),
                "url": $("#friend-url").val()
            }
        };

    var form_options = {
        success: requestSuccess,
        dataType: "json",
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        error: ajaxError,
        type : "POST",
        data : JSON.stringify(jsonData),
        beforeSubmit : beforeSubmit
    }
    
    $('#friendrequestform').ajaxForm(form_options);

    function beforeSubmit(arr, form, options) {
        console.log("setting url")
        console.log($("#author-from").val()  + " wtf is this " + $("#author-to").val())
        options["url"] = base_url;
      
        console.log(options["data"])
        console.log(options["url"]);
    }

    function ajaxError(xhr, errmsg, err) {
        var response;

        console.log("we errored out yo");
        console.log(xhr.responseText)

    }
    
    function requestSuccess(response, status, xhr, form) {
        console.log("friend request sent!");
  
    };

});

function clicker() {
    // Cheap little hack to make the heart the button
    // to submit the form, can't just say
    // onclick=submit() in the html because then it
    // doesn't run the ajax above.
    //$("#friendrequestform").submit();

    // Even cheaper hack... not using submit at all just f ucking ajaxing it 
    // outta control. Actually this might not be ah ack this might be what we want
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
    // THIS NEEDS TO BE RESOLVED, just a quick hack
    // to at least get it working... basically
    // JSON when stringifying everything is adding
    // backslashes so I'm fucking removing them fuck that
    // it was making the IDs not match up
    var myJSONString = JSON.stringify(jsonData);
    var regex = new RegExp("/", 'g');
    var myEscapedJSONString = myJSONString.replace(regex,"");
    console.log(myEscapedJSONString);
    $.ajax({
        success: requestSuccess,
        dataType: "json",
        clearForm : false,
        contentType: "application/json; charset=utf-8",
        //error: ajaxError,
        type : "POST",
        url : base_url,
        data : myEscapedJSONString,
        beforeSubmit : beforeSubmit
    }).done(function (data) {
         console.log("Response "+ data);
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
  
    };
}
