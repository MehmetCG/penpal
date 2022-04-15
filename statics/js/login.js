$(document).ready(function(){

    window.showLogin = function showLogin(){
        $("#signup-page").hide();
        $("#login-page").show();      
    }
    window.showSignup = function showSignup(){
        $("#login-page").hide();
        $("#signup-page").show();    
    }
    
});