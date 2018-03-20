(function($) {

  String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted;
  }

  function request_filter_rank(filter_by, rankpage, table_name) {
    $.ajax({
      method: "GET",
      url: '/sd-api/rank-data/?category=' + filter_by + '&rankpage=' + rankpage,
      success: function(data){
        console.log(data)
        $.each(data.results, function(i, rankdata){
          if (i < 10) {
            var class_name = rankdata.sign.split('-')[0] + '_line'
            var inc_dec = (rankdata.rank_change == 0) ? '' : rankdata.rank_change
            if ((filter_by == 'institution_score') || (filter_by == 'foreigner_score')) {
              var counter = (i + 1) + ((rankpage - 1) * 10)
            } else {
              var counter = (i + 1) + ((rankpage - 1) * 6)
            }
            var lead_agent = ''
            if (rankdata.lead_agent == 'institution') {
              lead_agent = '기관'
            } else if (rankdata.lead_agent == 'foreigner') {
              lead_agent = '외국인'
            } else {
              lead_agent = '-'
            }
            var tr = `
            <tr class="{0}">
                <td class="first_num">
                    <div class="num_contents_wrap">
                        <div class="info_contetns clear_col">
                            <div class="up_down_icon col"></div>
                            <!-- 증감 숫자 -->
                            <div class="info_num col">{1}</div>
                            <!-- END 증감 숫자 -->
                        </div>
                    </div>
                </td>
                <td class="normal_num">{2}</td>
                <td class="left_td title_td"><a href="/marketsignal/snapshot/{3}">{4}</a></td>
                <td class="lead_td">{5}</td>
                <td class="grade_num">{6}</td>
                <td class="cart_wrap"><div class="cart_button">+</div></td>
            </tr>
            `.format(class_name, inc_dec, counter, rankdata.code, rankdata.name, lead_agent, rankdata.total_score)
            $(table_name).append(tr)
          }
        })
      },
      error: function(data){
        console.log('error')
      }
    })
  }

  $('#agency_paging_nav a').click(function(){
    var a_s = document.querySelectorAll('#agency_paging_nav a')
    for (i=0; i<a_s.length; i++) {
      a_s[i].classList.remove('active')
    }
    this.classList.add('active')
    var rankpage = this.text
    $('.ins_score_table').html('')
    request_filter_rank('institution_score', rankpage, '.ins_score_table')
  })

  $('#foreigner_paging_nav a').click(function(){
    var a_s = document.querySelectorAll('#foreigner_paging_nav a')
    for (i=0; i<a_s.length; i++) {
      a_s[i].classList.remove('active')
    }
    this.classList.add('active')
    var rankpage = this.text
    $('.for_score_table').html('')
    request_filter_rank('foreigner_score', rankpage, '.for_score_table')
  })

  $('#jump_paging_nav a').click(function(){
    var a_s = document.querySelectorAll('#jump_paging_nav a')
    for (i=0; i<a_s.length; i++) {
      a_s[i].classList.remove('active')
    }
    this.classList.add('active')
    var rankpage = this.text
    $('.tot_inc_table').html('')
    request_filter_rank('total_increase', rankpage, '.tot_inc_table')
  })

  $('#trand_up_paging_nav a').click(function(){
    var a_s = document.querySelectorAll('#trand_up_paging_nav a')
    for (i=0; i<a_s.length; i++) {
      a_s[i].classList.remove('active')
    }
    this.classList.add('active')
    var rankpage = this.text
    $('.ins_inc_table').html('')
    request_filter_rank('institution_increase', rankpage, '.ins_inc_table')
  })

  $('#trand_down_paging_nav a').click(function(){
    var a_s = document.querySelectorAll('#trand_down_paging_nav a')
    for (i=0; i<a_s.length; i++) {
      a_s[i].classList.remove('active')
    }
    this.classList.add('active')
    var rankpage = this.text
    $('.for_inc_table').html('')
    request_filter_rank('foreigner_increase', rankpage, '.for_inc_table')
  })

})(jQuery)
