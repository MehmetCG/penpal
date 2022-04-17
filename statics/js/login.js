$(document).ready(function(){

    window.showLogin = function showLogin(){
        $("#signup-page").hide();
        $("#login-page").show();      
    }
    window.showSignup = function showSignup(){
        $("#login-page").hide();
        $("#signup-page").show();    
    }

    function show_notification(type, element_id, error_message){
        document.getElementById(element_id).insertAdjacentHTML(
            "afterbegin",
            "<div class='alert alert-"+type+" alert-dismissable'>"
            +"<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>"
            +error_message+"</div>"
        )
    }

    $("#signup-form").submit(function(e){
        e.preventDefault();
        var email = $("#signup-email").val();
        var username = $("#signup-username").val();
        var password1 = $("#signup-password1").val();
        var password2 = $("#signup-password2").val();

        if (password1 != password2){
            show_notification("danger", "signup-form", "Passwords do not match!");
        }else{
            var data = JSON.stringify({
                "email": email,
                "username": username,
                "password": password1
            });
            $.ajax({         
                url: "/api/user_create/",
                data: data,
                type: "post",
                contentType: "application/json",
                dataType: "json",
                headers: { "X-CSRFToken":"{{csrf_token}}"},           
                success: function (data) {
                    $('#signup-form')[0].reset();
                    showLogin();
                    show_notification("success", "login-form", 
                    "Your account has been created successfully!");
                },
                error: function(response) {                          
                    show_notification("danger", "signup-form", response.responseText)
               }
            });         
        }
    });
});