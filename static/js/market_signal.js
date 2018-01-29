( function($) {
    
    $(window).load(function(){
        var filter_container = $('#ranking_filter>ul');
        var filter_cont = filter_container.children().length;
        var filter_line = (filter_cont/8);
        var filter_H = filter_line*60;
        
        filter_container.css({
            'height' : filter_H+'px'
        });
        
        for(var i=0; i<filter_cont; i++ ){
            var selector = filter_container.find('li:nth-child('+(i+1)+')');
            if( parseInt(i/8) <1 ) {
                selector.css({
                    'left' : (i*140)+'px',
                    'top'  : (parseInt(i/8)*60)+'px'
                });
            } else {
                var i_result = (i%8);
                selector.css({
                    'left' : (i_result*140)+'px',
                    'top'  : (parseInt(i/8)*60)+'px'
                });
            }
        }
        
    });
    $(document).on('click', '#ranking_filter>ul>li>a', function (){
        
        var partent_li = $(this).parents('li');
        $('#ranking_filter>ul>li').removeClass('active');
        $('#ranking_filter>ul>li').attr('data-click', '0');
        $('ul.child_select').css('height', '0px');  
        
        
        if( partent_li.children('ul') ){
            var children = partent_li.find('ul');
            var count = children.children().length;
            
            if( partent_li.attr('data-click') == 0 ){
                children.css('height', (count*38)+'px');
            } else if( partent_li.attr('data-click') != 0 ) {
                children.css('height', '0px');
            }
        } else {
            
        }
        partent_li.removeClass('selected');
        partent_li.addClass('active');
        partent_li.attr('data-click','1');
    });
    $(document).on('click', '#ranking_filter>ul>li>ul>li>a', function (){
        var partent_filter = $(this).parents('.child_filter');
        partent_filter.attr('data-click', '0');
        var this_text = $(this).text();
        
        partent_filter.find('.child_select').css('height', '0px');
        
        partent_filter.find('.select_text').text(this_text);
        partent_filter.addClass('selected');
    });
   
    $(document).on('click', '.grade_contents>.cart_button', function (){
        var btn_container =  $(this).parent('.grade_contents');
        
        if( $(this).attr('data-click') == '1' ){
            $('.cart_button').attr('data-click', '0');
            $('.cart_portfolio').removeClass('active');
            $(this).attr('data-click', '0');
            btn_container.find('.cart_portfolio').removeClass('active');
        } else {
            $('.cart_button').attr('data-click', '0');
            $('.cart_portfolio').removeClass('active');
            $(this).attr('data-click', '1');
            btn_container.find('.cart_portfolio').addClass('active');
        }
    });
    
    $(document).on('click', '.select_btn_wrap>.cart_original_btn', function (){
        var btn_origin =  $(this).parents('.cart_portfolio');
        $(this).addClass('active');
        btn_origin.find('.cart_new_btn').removeClass('active');
        btn_origin.find('.select_portfolio>.original_select').addClass('active');
        btn_origin.find('.select_portfolio>.new_select').removeClass('active');
    });
    
    $(document).on('click', '.select_btn_wrap>.cart_new_btn', function (){
        var btn_new =  $(this).parents('.cart_portfolio');
        $(this).addClass('active');
        btn_new.find('.cart_original_btn').removeClass('active');
        btn_new.find('.select_portfolio>.original_select').removeClass('active');
        btn_new.find('.select_portfolio>.new_select').addClass('active');
    });
    
    $(document).on('click', '.cart_portfolio>.submit_btn', function (){
        var submit_cotainer = $(this).parents('.cart_portfolio');
        var port_cotainer = $(this).parents('.grade_contents');
        submit_cotainer.removeClass('active');
        port_cotainer.find('.cart_button').attr('data-click', '0');
    });
    
    
})(jQuery);