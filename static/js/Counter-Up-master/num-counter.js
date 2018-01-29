( function($) {
    $(document).ready(function(){
        $('.counter_num').counterUp({
            delay: 10,
            time: 1000
        });
        $(".scramble").scramble( 1500, 100, "alphabet", true );
    });
    
    
    
    
    
})(jQuery);