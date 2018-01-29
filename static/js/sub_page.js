( function($) {

    $(document).on('click', '.identity_icon_btn.message_on', function (){
        $(this).addClass('message_click');
    });
    $(document).on('click', '.identity_icon_btn.message_on.message_click', function (){
        $(this).removeClass('message_on');
        $(this).removeClass('message_click');
        $(this).addClass('message_off');
    });

    $(document).on('click', '.identity_icon_btn.message_off', function (){
        $(this).removeClass('message_on');
        $(this).addClass('message_click');
    });
    $(document).on('click', '.identity_icon_btn.message_off.message_click', function (){
        $(this).removeClass('message_on');
        $(this).removeClass('message_click');
        $(this).addClass('message_off');
    });



})(jQuery);
