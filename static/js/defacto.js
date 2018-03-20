(function($) {

  String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted;
  }

  function request_filter_rank(filter_by) {
    $.ajax({
      method: "GET",
      url: '/sd-api/rank-data/?category=' + filter_by,
      success: function(data){
        console.log(data)
        $.each(data.results, function(i, rankdata){
          if (i < 10) {
            var tr = `
            <tr class="plus_line">
                <td class="first_num">
                    <div class="num_contents_wrap">
                        <div class="info_contetns clear_col">
                            <div class="up_down_icon col"></div>
                            <!-- 증감 숫자 -->
                            <div class="info_num col">1</div>
                            <!-- END 증감 숫자 -->
                        </div>
                    </div>
                </td>
                <td class="normal_num">1</td>
                <td class="left_td title_td">삼성전자</td>
                <td class="lead_td">외국인</td>
                <td class="grade_num">90</td>
                <td class="cart_wrap"><div class="cart_button">+</div></td>
            </tr>
            `.format('', rankdata.num, rankdata.code, rankdata.name, rankdata.momentum_score, rankdata.volatility_score, rankdata.volume_score, rankdata.total_score)
            $('.filter_rank_table').append(tr)
          }
        })
      },
      error: function(data){
        console.log('error')
      }
    })
  }



})(jQuery)
