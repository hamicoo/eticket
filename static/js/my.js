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
                $("#result").removeClass('alert info').removeClass('alert warning').removeClass('alert alert').addClass('alert success');
            }

            if (data.result === 'it seem this email alredy in use please follow th link ') {
                $("#result").show();
                $("#result").removeClass('alert info').removeClass('alert success').addClass('alert alert');
            }

            if (data.result === 'please enter correct email address') {
                $("#result").show();
                $("#result").removeClass('alert info').removeClass('alert alert').addClass('alert warning');
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

            if (data.result === 'False') {
                $("#result").show();
                $("#result").text('Your card information is incorrect !')
                $("#result").removeClass('alert success').addClass('alert warning');
            }
            if (data.result === 'True') {
                $("#result").show();
                $("#result").text('Your card information is correct now')
                $("#result").removeClass('alert info').removeClass('alert warning').removeClass('alert alert').addClass('alert success');
            }

            });
            return false;
            });
            });



