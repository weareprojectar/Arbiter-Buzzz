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

    $(document).mouseup(function(e){
        var container1 = $('#save_submit_pop');
        var container2 = $('#rms_search_list');
        var container3 = $('.identity_icon_btn.message_on.message_click');
        var container4 = $('.identity_icon_btn.message_off.message_click');

        if( container1.has(e.target).length === 0) {
            container1.removeClass('active');
        }

        if( container2.has(e.target).length === 0) {
            if ( e.target.id == 'search_code' ) {
              // pass
            } else {
              container2.removeClass('active');
            }
        }

        if( container3.has(e.target).length === 0) {
            container3.removeClass('message_on');
            container3.removeClass('message_click');
            container3.addClass('message_off');
        }

        if( container4.has(e.target).length === 0) {
            container4.removeClass('message_on');
            container4.removeClass('message_click');
            container4.addClass('message_off');
        }
    });

})(jQuery);
