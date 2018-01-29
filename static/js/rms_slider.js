( function($) {

    $(document).ready(function(){
        var origin_cotainer = $('.slider_container');
        var container = $('#slider_content');
        var count = container.children().length;
        var nav_next = $('#slider_next');
        var nav_prev = $('#slider_prev');
        var col = $('.slider_col');
        container.attr('data-all', count);

        $(document).on('click', '#slider_next', function() {
            var page_num = parseInt($('.slider_col.active').attr('data-num'))

            // on page slide - default behaviors override
            if (page_num == 3) {
              save_portfolio_on_click(true)
            }

            else if (page_num == 1) {
              var capital_amt = $('#capital_set').val()
              if (!capital_amt | 0 === capital_amt.length) {
                $('#msg-area').text('')
                $('#capital_amt').text('10,000,000원')
              } else {

                if (isNaN(Number(capital_amt))) {
                  var msg = '자본금을 다시 한 번 입력해주세요'
                  $('#msg-area').text(msg)
                  $('#capital_set').val('')
                } else {
                  $('#msg-area').text('')
                  var formatted_capital = parseInt(capital_amt).toLocaleString()
                  $('#capital_amt').text(formatted_capital + '원')
                }

              }
            }

            else if (page_num == 2) {
              if ($('#kinds_type').text() == '주식형') {
                // pass
              } else {
                $('#kinds_type').text('현금 + 주식형')
              }
            }

            var origin_click = parseInt(origin_cotainer.attr('data-click'));
            col.removeClass('active');

            if( origin_click < count-1 ){
                origin_click++;
                origin_cotainer.attr('data-click', origin_click);
            } else {
                origin_cotainer.attr('data-click', '2');
            }
            container.css({
                'margin-left' : '-'+(origin_click*100)+'%'
            });
            $('.slider_col[data-num="'+(origin_click+1)+'"]').addClass('active');
        });

        nav_prev.click(function(){
            var page_num = parseInt($('.slider_col.active').attr('data-num'))
            if (page_num == 1) {
              location.href = '/rms'
            }
            var origin_click = parseInt(origin_cotainer.attr('data-click'));
            col.removeClass('active');

            if( origin_click > 0 ){
                origin_click--;
                origin_cotainer.attr('data-click', origin_click);
            } else {
                origin_cotainer.attr('data-click', '0');
            }
            container.css({
                'margin-left' : '-'+(origin_click*100)+'%'
            });
            $('.slider_col[data-num="'+(origin_click+1)+'"]').addClass('active');
        });
    });

})(jQuery);
