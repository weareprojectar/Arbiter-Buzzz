( function($) {

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
    }

    function save_portfolio_data() {
      var capital = parseInt($('#capital_set').val())
      var csrftoken = getCookie('csrftoken')
      $.ajax({
        method: "POST",
        url: '/api/portfolio/',
        data: {
            'capital': capital,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(data){
          $('#capital_amt').text(String(data.capital) + '원')
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    $(document).on('click', '#save_capital_btn', function () {
      var capital_amt = $('#capital_set').val()
      if (!capital_amt | 0 === capital_amt.length) {
        $('#capital_amt').text('0')
        $('#slider_next').click()
      } else {
        $('#capital_amt').text(String(capital_amt) + '원')
        $('#slider_next').click()
      }
    })

    $(document).on('keydown', '#capital_set', function (e) {
      if (e.keyCode == 13) {
        var capital_amt = $('#capital_set').val()
        if (!capital_amt | 0 === capital_amt.length) {
          $('#capital_amt').text('0')
          $('#slider_next').click()
        } else {
          $('#capital_amt').text(String(capital_amt) + '원')
          $('#slider_next').click()
        }
      }
    })

    $(document).on('click', '#stock_btn', function () {
      $('#kinds_type').text('주식형')
      $('#slider_next').click()
    })

    $(document).on('click', '#stock_cash_btn', function () {
      $('#kinds_type').text('현금 + 주식형')
      $('#slider_next').click()
    })

})(jQuery);
