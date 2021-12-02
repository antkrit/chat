$("#create-chat-from").validate({
    rules: {
        name: {
            required: {
                depends: function() {
                    $(this).val($.trim($(this).val()));
                    return true;
                }
            },
            minlength: 3,
            maxlength: 200
        },
        description: {
            required: {
                depends: function() {
                    $(this).val($.trim($(this).val()));
                    return true;
                }
            },
            maxlength: 500
        }
    },
    messages: {
        name: {
            required: "Chat name field cannot be blank",
            minlength: "Minimum 3 characters",
            maxlength: "Maximum 200 characters"
        },
        description: {
            required: "Username field cannot be blank",
            maxlength: "Maximum 500 characters"
        }
    }
});

$("#enter-chat-form").validate({
    rules: {
        username: {
            required: {
                depends: function() {
                    $(this).val($.trim($(this).val()));
                    return true;
                }
            },
            maxlength: 50
        }
    },
    messages: {
        username: {
            required: "Username field cannot be blank",
            maxlength: "Maximum 50 characters"
        }
    }
});