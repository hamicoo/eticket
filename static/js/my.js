$(document).ready(function() {
    $("#result").hide();
     
});
    $(function() {
        $('#proglang').bind('focusout',function(){
            $.getJSON('/check_email_jquery',{
            proglang: $('input[name="proglang"]').val()
            }, function(data) {
            $("#result").text(data.result);

            if (data.result === '1') {
                Toastify({
                text: "it's good ! you can register with this email address",
                    duration: 5000,
                    //destination: "https://github.com/apvarun/toastify-js",
                    newWindow: true,
                close: true,
                gravity: "top", // `top` or `bottom`
                position: 'center', // `left`, `center` or `right`
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                // onClick: function(){} // Callback after click
                }).showToast();
            }

            if (data.result === '0')
            {
                Toastify({
                    text: "it seem this email alredy in use please,if it belongs to you click link",
                    duration: 8000,
                    destination: "/login",
                    newWindow: true,
                    close: true,
                    gravity: "top", // `top` or `bottom`
                    position: 'center', // `left`, `center` or `right`
                    backgroundColor: "linear-gradient(to right, #eb5149, #fc190f)",
                    stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                    // onClick: function(){} // Callback after click
                     }).showToast();
            }

            if (data.result === '2') {

                    Toastify({
                    text: "incoorect Email Address",
                    duration: 8000,
                    destination: "/login",
                    newWindow: true,
                    close: true,
                    gravity: "top", // `top` or `bottom`
                    position: 'center', // `left`, `center` or `right`
                    backgroundColor: "linear-gradient(to right, #fca50f, #ffa100)",
                    stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                    // onClick: function(){} // Callback after click
                     }).showToast();





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
                Toastify({
                    text: "Your Card Information is Incorrect",
                    duration: 6000,
                    //destination: "/login",
                    newWindow: true,
                    close: true,
                    gravity: "top", // `top` or `bottom`
                    position: 'center', // `left`, `center` or `right`
                    backgroundColor: "linear-gradient(to right, #fca50f, #ffa100)",
                    stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                    // onClick: function(){} // Callback after click
                     }).showToast();
            }
            if (data.result === 'True') {
                Toastify({
                text: "Your Card Infromation Is Correct !",
                    duration: 5000,
                    //destination: "https://github.com/apvarun/toastify-js",
                    newWindow: true,
                close: true,
                gravity: "top", // `top` or `bottom`
                position: 'center', // `left`, `center` or `right`
                backgroundColor: "linear-gradient(to right, #00b09b, #96c93d)",
                stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                // onClick: function(){} // Callback after click
                }).showToast();
            }



            });
            return false;
            });
            });




     $(document).ready(function() {
       $('#mybutt').click(function(){

           var name = $('#name').val();
           var family = $('#family').val();
           var proglang = $('#proglang').val();
           var nationalid = $('#nationalid').val();
           var birthdate = $('#birthdate').val();
           var male = $('#male').val();
           var female = $('#female').val();
           var mobile = $('#mobile').val();
           var password = $('#password').val();
           var address = $('#address').val();
           var city = $('#city').val();
           var pinid = $('#pinid').val();
           var tagid = $('#tagid').val();
           var sex= $('input[name="sex"]:checked').val();

           $.ajax({
           url: "/processNewRegisterUser",
           type: "get",
           data: {
               name: name
               , family:family
               ,proglang:proglang
                ,nationalid:nationalid
               ,birthdate:birthdate
               ,sex:sex,
               mobile:mobile
               ,password:password
               ,address:address,
               city:city
               ,pinid:pinid
               ,tagid:tagid
           },
           success: function(response) {

               if (response.code === '1'){
                var delay = 2500;
                setTimeout(function() {
                 window.location = "/confirm";
                 return true;
                 }, delay);
               }




                Toastify({
                text: response.message,
                    duration: 5000,
                    //destination: "https://github.com/apvarun/toastify-js",
                newWindow: true,
                close: true,
                gravity: "top", // `top` or `bottom`
                position: 'center', // `left`, `center` or `right`
                backgroundColor: response.noticetype ,
                stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                // onClick: function(){} // Callback after click
                }).showToast();


          },
          error: function(xhr) {
            Toastify({
                text: 'Error calling service please try again later',
                    duration: 5000,
                    //destination: "https://github.com/apvarun/toastify-js",
                    newWindow: true,
                close: true,
                gravity: "top", // `top` or `bottom`
                position: 'center', // `left`, `center` or `right`
                backgroundColor: "linear-gradient(to right, #eb5149, #fc190f)",
                stopOnFocus: true
                    //  ,  Prevents dismissing of toast on hover
                // onClick: function(){} // Callback after click
                }).showToast();
         }
         });
       });
    });





