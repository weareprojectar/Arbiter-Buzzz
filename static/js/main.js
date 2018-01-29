( function($) {

    $(document).on('click', '#main_login_btn', function (){
        $('.popup_contents').removeClass('active');
        $('body').css('overflow', 'hidden');
        $('#popup').addClass('active');
        $('#login_popup').addClass('active');

    });

    $(document).on('click', '.login_up', function (){
        $('.popup_contents').removeClass('active');
        /*$('body').css('overflow', 'hidden');*/
        $('#popup').addClass('active');
        $('#login_popup').addClass('active');

    });

    $(document).on('click', '#main_register_btn', function (){
        $('.popup_contents').removeClass('active');
        /*$('body').css('overflow', 'hidden');*/
        $('#popup').addClass('active');
        $('#register_popup').addClass('active');
    });

    $(document).on('click', '.register_pop', function (){
        $('.popup_contents').removeClass('active');
        /*$('body').css('overflow', 'hidden');*/
        $('#popup').addClass('active');
        $('#register_popup').addClass('active');
    });

    $(document).on('click', '.password_pop', function (){
        $('.popup_contents').removeClass('active');
        /*$('body').css('overflow', 'hidden');*/
        $('#popup').addClass('active');
        $('#password_popup').addClass('active');
    });

    $(document).on('click', '.popup_close', function (){
        $('.popup_contents').removeClass('active');
        $('#popup').removeClass('active');
        var sh = $(window).height();
        console.log(sh);
        if(sh <= 720 ) {
            $('body').css('overflow', 'auto');
        }

    });
})(jQuery);
