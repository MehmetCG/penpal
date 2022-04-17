
$(document).ready(function(){
    
    function showNotification(type, element_id, error_message){
        document.getElementById(element_id).insertAdjacentHTML(
            "afterbegin",
            "<div class='alert alert-"+type+" alert-dismissable'>"
            +"<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>"
            +error_message+"</div>"
        )
    }

    $("#profileForm").submit(function(e) {
        e.preventDefault();   
        var age = $("#age").val();
        var gender = $("#gender").val();
        var country = $("#country").val();
        var nativeLanguage = $("#nativeLanguage").val();
        var practisingLanguage = $("#practisingLanguage").val();
        var description = $("#description").val();
        var image = $("#image").val();
        var username = window.location.pathname.split('/')[2];

        var data = JSON.stringify({
            "age": age,
            "gender": gender,
            "country": country,
            "native_language": nativeLanguage,
            "practising_language": practisingLanguage,
            "description": description,
            "image": image
        });
        $.ajax({         
            url: "/api/profile_update/" + username +"/",
            data: data,
            type: "patch",
            dataType: "json",
            contentType: "application/json",
            headers: {"X-CSRFToken":$('input[name="csrfmiddlewaretoken"]').val()},           
            success: function (data) {
                showNotification(
                    "success", 
                    "profileForm", 
                    "Your profile has been updated successfully"
                )
            },
            error: function(response) {   
                showNotification("danger", "profileForm", response.responseText)
            }       
        });       
    });
});