/*

Script  : Email Register Form
Version : 1.0
Author  : Surjith S M
URI     : http://themeforest.net/user/surjithctly

Copyright © All rights Reserved
Surjith S M / @surjithctly

*/

$(function() {

    "use strict";

    // Go to second Step
    $('#next-personal').on('click', function() {
        $('#js-product-info').addClass('slide-out-left');
        $('#js-personal-info').addClass('slide-in-right');
    });
    // back to first Step
    $('#prev-product-info').on('click', function() {
        $('#js-personal-info').removeClass('slide-in-right');
        $('#js-product-info').removeClass('slide-out-left');
    });


    /* ================================================
   jQuery Validate - Reset Defaults
   ================================================ */

    $.validator.setDefaults({
        highlight: function(element) {
            $(element).closest('.form-group').addClass('has-error');
        },
        unhighlight: function(element) {
            $(element).closest('.form-group').removeClass('has-error');
        },
        errorPlacement: function(error, element) {}
    });

    /* 
    VALIDATE
    -------- */

    $("#preorderform").submit(function(e) {
        e.preventDefault();
    }).validate({
        rules: {},
        submitHandler: function(form) {

            $(".js-preorder-btn").attr("disabled", true);

            /* 
            CHECK PAGE FOR REDIRECT (Thank you page)
            ---------------------------------------- */

            var redirect = $('#preorderform').data('redirect');
            var noredirect = false;
            if (redirect == 'none' || redirect == "" || redirect == null) {
                noredirect = true;
            }

            $(".js-preorder-btn").addClass('sending');

            var dataString = $(form).serialize();

            /* 
             AJAX POST
             --------- */

            $.ajax({
                type: "POST",
                data: dataString,
                url: "php/pre-order.php",
                cache: false,
                success: function(d) {
                    $(".form-group").removeClass("has-success");
                    if (d == 'success') {

                        if (noredirect) {
                            setTimeout(function() {
                                $(".js-preorder-btn").removeClass('sending').addClass('is-success');
                                $(".js-preorder-btn span").html('<span class="checkmark"></span>');
                            }, 2000);

                        } else {
                            window.location.href = redirect;
                        }

                    } else {

                        // Show failed message
                        setTimeout(function() {
                            $(".js-preorder-btn").removeClass('sending').addClass('is-failed');
                            $(".js-preorder-btn span").text('Error!');
                            console.log(d);
                        }, 2000);

                        // Revert to default if failed
                        setTimeout(function() {
                            $(".js-preorder-btn").removeClass('is-failed');
                            $(".js-preorder-btn span").html('<span>Finish Purchase</span>');
                            $(".js-preorder-btn").attr("disabled", false);
                        }, 4000);

                    }
                },
                error: function(d) {

                    // Show failed message
                    setTimeout(function() {
                        $(".js-preorder-btn").removeClass('sending').addClass('is-failed');
                        $(".js-preorder-btn span").html('<span class="crossmark"></span>');
                        console.log(d);
                    }, 2000);

                    // Revert to default if failed
                    setTimeout(function() {
                        $(".js-preorder-btn").removeClass('is-failed');
                        $(".js-preorder-btn span").html('<span>Finish Purchase</span>');
                        $(".js-preorder-btn").attr("disabled", false);
                    }, 4000);



                }
            });
            return false;

        }
    });

})
