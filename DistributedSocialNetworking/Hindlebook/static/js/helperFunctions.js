
    function setUpAjaxForm(form, formOptions) {
        if (form == undefined || form.length === 0) { console.log("Form does not exist."); return; }
        if (form.length > 1) { console.log("Multiple forms with same ID."); return; }

        if (!('dataType' in formOptions)) { formOptions['dataType'] = "json"; }

        if (!('success' in formOptions)) { formOptions['success'] = ajaxSuccessLog; }
        if (!('error' in formOptions)) { formOptions['error'] = ajaxErrorLog; }
        if (!('beforeSubmit' in formOptions)) { formOptions['beforeSubmit'] = beforeSubmit; }

        form.ajaxForm(formOptions);
    }

    function ajaxSuccessLog(response, status, xhr, form) {
        console.log("Form was valid!");
        console.log(response);
        console.log(xhr.status + ":" + xhr.responseText);
    }

    function ajaxErrorLog(xhr, errmsg, err) {
        console.log(xhr.status + ": " + xhr.responseText);
    }

    function beforeSubmit(arr, $form, options) {
        console.log($form);
        console.log(JSON.stringify(arr));
    }

