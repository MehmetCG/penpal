
$(document).ready(function(){

    function showFilterResult(profiles) {
        $("#profiles").empty()
        
        if(profiles.length == 0){
            $("#profiles").append(
                "<div class='alert alert-warning alert-dismissable'>"
                +"<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>"
                +"Sorry! No result found :(</div>"
            )
        }else{
            window.scrollTo(0,0);
        
            for (i = 0; i<profiles.length; i++){
                profile = profiles[i]
                var status;
                var last_login;
                if (profile.is_online){
                    status = 'success">Online';
                    last_login = "";
                }else{
                    status = 'danger">Last Seen :';
                    last_login = profile.last_login
                }
                $("#profiles").append(
                    '<div class="container profile-page" id="profile-cards" >'
                    +'<div class="row"><div class="card profile-header">'
                    +'<div class="body"><div class="row"><div class="col-lg-4 col-md-4 col-12">'
                    +'<div class="profile-image float-md-right" style="text-align: center;" >'
                    +'<img src="'+profile.image+'" alt="" ><div><h4 class="m-t-0 m-b-0">'
                    +'<strong>'+profile.username+'</strong></h4>'+'<a href="/chat/'+profile.user+'">'
                    +'<button class="btn btn-primary btn-round btn-simple">Message</button></a>'
                    +'</div></div></div><div class="col-lg-8 col-md-8 col-12">'
                    +'<table class="table table-user-information"><tbody><tr><td>Status:</td>'
                    +'<td><small class="chat-alert-layout badge badge-'+status+'</small>'+' '+last_login+'</td></tr>'
                    +'<tr><td>Gender, Age:</td><td>'+profile.gender+', '+profile.age+'</td></tr>'
                    +'<tr><td>Country:</td><td>'+profile.country+'</td></tr>'
                    +'<td>Native Language:</td><td>'+profile.native_language+'</td></tr>'
                    +'<tr><td>Practising Language:</td><td>'+profile.practising_language+'</td></tr>'
                    +'<tr><td>Description:</td><td>'+profile.description
                    +'</td></tr></tbody></table></div></div></div></div></div></div>')
            }
        }
    }
    
    $("#filter").submit(function(e) {
        e.preventDefault();   
        var minAge = $("#minAge").val();
        var maxAge = $("#maxAge").val();
        var gender = $("#gender").val();
        var country = $("#country").val();
        var nativeLanguage = $("#nativeLanguage").val();
        var practisingLanguage = $("#practisingLanguage").val();

        var data = {
            "min_age": minAge,
            "max_age": maxAge,
            "gender": gender,
            "country": country,
            "native_language": nativeLanguage,
            "practising_language": practisingLanguage
        };
        
        $.ajax({         
            url: "/api/profile_list/",
            data: data,
            dataType: 'json',
            contentType: "application/json",
            headers: {"X-CSRFToken":'{{csrf_token}}'},           
            success: function (data) {
                showFilterResult(data)
                console.log(data)
            },
            error: function(response) {                          
                console.log(response.responseText)
            }       
        });       
    });
});