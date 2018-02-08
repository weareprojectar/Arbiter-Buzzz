( function($) {

    $(document).on('click', '.defacto_table_filter_wrap>.filter_num', function (){
        $('.defacto_table_filter_wrap>.filter_num').removeClass('active');
        $(this).addClass('active');
    });


})(jQuery);
