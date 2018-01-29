( function($) {

    // function formatNumber(num) {
    //   // return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
    //   return num.replace(/(\d)(?=(\d{3})+(?!\d))/g, "$1,")
    // }

    // 1st page: set capital amount to 10000000 if not given
    function set_capital() {
      var capital_amt = $('#capital_set').val()
      if (!capital_amt | 0 === capital_amt.length) {
        $('#msg-area').text('')
        $('#capital_amt').text('10,000,000원')
        $('#slider_next').click()
      } else {
        if (isNaN(Number(capital_amt))) {
          var msg = '자본금을 다시 한 번 입력해주세요'
          $('#msg-area').text(msg)
          $('#capital_set').val('')
        } else {
          $('#msg-area').text('')
          var formatted_capital = parseInt(capital_amt).toLocaleString()
          $('#capital_amt').text(formatted_capital + '원')
          $('#slider_next').click()
        }
      }
    }

    $(document).on('click', '#save_capital_btn', function () {
      set_capital()
    })

    $(document).on('keydown', '#capital_set', function (e) {
      if (e.keyCode == 13) {
        set_capital()
      }
    })

    // 2nd page: set portfolio type to stock and cash if not chosen
    $(document).on('click', '#stock_btn', function () {
      $('#kinds_type').text('주식형')
      $('#slider_next').click()
    })

    $(document).on('click', '#stock_cash_btn', function () {
      $('#kinds_type').text('현금 + 주식형')
      $('#slider_next').click()
    })

    // 3rd page
    Number.prototype.pad = function(size) {
      var s = String(this);
      while (s.length < (size || 2)) {s = "0" + s;}
      return s;
    }

    String.prototype.format = function() {
      var formatted = this
      for (var i = 0; i < arguments.length; i++) {
          var regexp = new RegExp('\\{'+i+'\\}', 'gi')
          formatted = formatted.replace(regexp, arguments[i])
      }
      return formatted
    }

    function check_recent_ticker_update(ticker) {
      $.ajax({
        method: "GET",
        url: '/api/ticker-updated',
        success: function(data){
          check_ticker_exists(data.updated_date, ticker)
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    function check_ticker_exists(date, ticker) {
      $.ajax({
        method: "GET",
        url: '/api/ticker/?date=' + date + '&code=' + ticker,
        success: function(data){
          if (data.results.length > 0) {
            var name = data.results[0].name
            var ticker = data.results[0].code
            add_code_list(name, ticker)
          } else {
            var msg2 = '종목을 다시 입력해주세요'
            $('#msg-area-2').text(msg2)
          }
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    function add_code_list(name, ticker) {
      if ($.inArray(ticker, codes_list) != -1) {
        var msg2 = '이미 담으신 종목입니다'
        $('#msg-area-2').text(msg2)
      } else {
        var code_list = `
        <div class="list_col">
            <div class="list_col_title">{0} {1}</div>
            <a class="list_del_btn">삭제</a>
        </div>
        `.format(name, ticker)
        $('.search_list').append(code_list)
        codes_list.push(ticker)
        $('#msg-area-2').text('')
      }
    }

    var codes_list = []
    $(document).on('click', '#rms_save_list', function () {
      var search_code = $('#search_code').val()
      if (search_code != '') {
        check_recent_ticker_update(search_code)
        $('#search_code').val('')
      } else if (search_code == '') {
        // pass
      }
    })

    $(document).on('keydown', '#search_code', function (e) {
        if (e.keyCode == 13) {
          var search_code = $('#search_code').val()
          if (search_code != '') {
            check_recent_ticker_update(search_code)
            $('#search_code').val('')
          } else if (search_code == '') {
            // pass
          }
        }
    })

    $(document).on('click', '.list_del_btn', function () {
      var list_col = $(this).parents('.list_col').text()
      var list_col_text = list_col.replace(/\s+/g, '')
      var string_length = list_col_text.length
      var ticker = list_col_text.substr(string_length-8, 6)
      codes_list = codes_list.filter(function(code) {
        return code != ticker
      })
      $(this).parents('.list_col').remove()
    })

    // last step: save portfolio data to server

    // function getCookie(name) {
    //   var cookieValue = null
    //   if (document.cookie && document.cookie !== '') {
    //       var cookies = document.cookie.split(';')
    //       for (var i = 0; i < cookies.length; i++) {
    //           var cookie = jQuery.trim(cookies[i])
    //           // Does this cookie string begin with the name we want?
    //           if (cookie.substring(0, name.length + 1) === (name + '=')) {
    //               cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
    //               break;
    //           }
    //       }
    //   }
    //   return cookieValue;
    // }

    function save_portfolio_data(name, capital, type_raw, start_clicked) {
      // var csrftoken = getCookie('csrftoken')

      var type
      if (type_raw == '주식형') {
        type = 'S'
      } else if (type_raw == '현금 + 주식형') {
        type = 'CS'
      }
      $.ajax({
        method: "POST",
        url: '/api/portfolio/',
        data: {
            'name': name,
            'capital': capital,
            'portfolio_type': type,
            // 'csrfmiddlewaretoken': csrftoken
        },
        success: function(data){
          $('#saved_port_id').attr('value', data.id)
          if (start_clicked == true) {
            if (codes_list.length == 0) {
              var msg2 = '관심있는 종목을 선택하여 주세요'
              $('#msg-area-2').text(msg2)
            } else {
              save_history()
            }
          }
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    function update_portfolio_data(portfolio_id, name, capital, type_raw, start_clicked) {
      var type
      if (type_raw == '주식형') {
        type = 'S'
      } else if (type_raw == '현금 + 주식형') {
        type = 'CS'
      }
      $.ajax({
        type: "PUT",
        dataType: "json",
        url: '/api/portfolio/' + String(portfolio_id) + '/',
        data: {
            'id': parseInt(portfolio_id),
            'name': name,
            'capital': capital,
            'portfolio_type': type,
        },
        success: function(data){
          console.log(data)
          if (start_clicked == true) {
            if (codes_list.length == 0) {
              var msg2 = '관심있는 종목을 선택하여 주세요'
              $('#msg-area-2').text(msg2)
            } else {
              save_history()
            }
          }
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    function save_code_list(portfolio_id, code, saved) {
      var status = 'B'
      $.ajax({
        method: "POST",
        url: '/api/history/',
        data: {
            'portfolio': portfolio_id,
            'date': '',
            'code': code,
            'status': status,
            'price': 0
            // 'csrfmiddlewaretoken': csrftoken
        },
        success: function(data){
          if (saved == true) {
            start_diagnosis()
          } else {
            // pass
          }
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    function save_history() {
      if ($('#saved_port_id').attr('value') != '') {
        for (var i = 0; i < codes_list.length; i++) {
          if (i == codes_list.length - 1) {
            save_code_list($('#saved_port_id').attr('value'), codes_list[i], true)
          } else {
            save_code_list($('#saved_port_id').attr('value'), codes_list[i], false)
          }
        }
      }
    }

    function save_portfolio_on_click(start_clicked) {
      var name = $('#save_name').val()
      var capital = parseInt($('#capital_amt').text().replace(/,/g , '').replace('원', ''))
      var type_raw = $('#kinds_type').text()

      if (name == '') {
        var d = new Date()
        var year = d.getFullYear()
        var month = (d.getMonth()+1).pad(2)
        var date = d.getDate().pad(2)
        var hours = d.getHours().pad(2)
        var mins = d.getMinutes().pad(2)
        name = year + month + date + hours + mins
      }

      if (!isNaN(capital) && type_raw != '') {
        if ($('#saved_port_id').attr('value') != '') {
          update_portfolio_data($('#saved_port_id').attr('value'), name, capital, type_raw, start_clicked)
          $('#save_submit_pop').removeClass('active')
        } else {
          save_portfolio_data(name, capital, type_raw, start_clicked)
          $('#save_submit_pop').removeClass('active')
        }
      }

      else if (!isNaN(capital) && type_raw == '') {
        if ($('#saved_port_id').attr('value') != '') {
          update_portfolio_data($('#saved_port_id').attr('value'), name, capital, '현금 + 주식형', start_clicked)
          $('#save_submit_pop').removeClass('active')
        } else {
          save_portfolio_data(name, capital, '현금 + 주식형', start_clicked)
          $('#save_submit_pop').removeClass('active')
        }
      }

      else {
        $('#save_submit_pop').removeClass('active')
      }
    }

    function start_diagnosis() {
      $.ajax({
        method: "GET",
        url: '/api/history/',
        data: {
            'portfolio': portfolio_id,
            'date': '',
            'code': code,
            'status': status,
            'price': 0
            // 'csrfmiddlewaretoken': csrftoken
        },
        success: function(data){
          console.log(data)
        },
        error: function(data){
          console.log('error')
          console.log(data)
        }
      })
    }

    function start_diagnosis() {
      location.href = '/rms/diagnosis/' + $('#saved_port_id').attr('value')
    }

    $(document).on('click', '.slider_btn2', function () {
      save_portfolio_on_click(true)
    })

    $(document).on('click', '#save_name_btn', function () {
      save_portfolio_on_click()
    })

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

})(jQuery);
