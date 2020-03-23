$(document).ready(function() {
    $("#result").hide();
     
});
    $(function() {
        $('#proglang').bind('focusout',function(){
            $.getJSON('/check_email_jquery',{
            proglang: $('input[name="proglang"]').val()
            }, function(data) {
            $("#result").text(data.result);

            if (data.result === 'you can register with this email address') {
                $("#result").show();
                $("#result").removeClass('alert alert-info').removeClass('alert alert-warning').removeClass('alert alert-danger').addClass('alert alert-success');
            }

            if (data.result === 'it seem this email alredy in use please follow th link ') {
                $("#result").show();
                $("#result").removeClass('alert alert-info').removeClass('alert alert-success').addClass('alert alert-danger');
            }

            if (data.result === 'please enter correct email address') {
                $("#result").show();
                $("#result").removeClass('alert alert-info').removeClass('alert alert-danger').addClass('alert alert-warning');
            }



            });
            return false;
            });
            });


    $(function() {
        $('#pinid').bind('focusout',function(){
            $.getJSON('/check_tagid',{
            pinid: $('input[name="pinid"]').val(),
            tagid: $('input[name="tagid"]').val()

            }, function(data) {

            $("#result").text(data.result);

            if (data.result === 'Your card information is incorrect !') {
                $("#result").show();
                $("#result").removeClass('alert alert-success').addClass('alert alert-danger');
            }
            if (data.result === 'Your card information is correct now') {
                $("#result").show();
                $("#result").removeClass('alert alert-danger').addclass('alert alert-success');
            }

            });
            return false;
            });
            });



