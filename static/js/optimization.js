(function($) {

  String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted
  }

  function draw_charts() {
    var port_id = $('#saved_port_id').attr('value')

    $.ajax({
      method: "GET",
      url: '/api/portfolio/' + port_id + '/optimization/',
      success: function(data){
        $('#loader-wrapper').fadeOut(1000)
        $('#rms_portfolio_section').fadeIn(1000)
        $('#sub_footer').fadeIn(1000)
        $('.bee_icon').fadeIn(1000)

        var old_ratio_array = data.result.old_weights
        var ratio_array = data.result.weights
        var left_ratio = 1
        for (var i = 0; i < ratio_array.length; i++) {
          left_ratio -= ratio_array[i][1]
        }
        ratio_array.push(['현금', left_ratio])
        console.log(ratio_array)
        draw_port_situation('port_situation', ratio_array)

        var port_spec = data.result.port_specs
        draw_port_spec(port_spec)

        var ret = data.result.return
        var avg_ret = data.result.average_return
        var avg_vol = data.result.average_volatility
        var sharpe = data.result.sharpe_ratio
        parse_port_info(ret, avg_ret, avg_vol, sharpe)

        var result = data.result.backtest_result
        var algo = result['Portfolio']
        var bm = result['Benchmark']
        draw_result_graph(algo, bm)

        var variance_list = data.result.weight_differences
        parse_variance_table(old_ratio_array, ratio_array, variance_list)
        // var algo_1mon = algo.slice(-1)[1] - algo.slice(-2)[1]
        // console.log(algo_1mon)
        var market_array = data.result.market
        draw_port_situation('market_donut', market_array)
        var size_array = data.result.size
        draw_port_situation('size_donut', size_array)
        var industry_array = data.result.industry
        draw_port_situation('sector_donut', industry_array)
      },
      error: function(data){
        console.log(data)
      }
    })
  }

  $('#rms_portfolio_section').hide()
  $('#sub_footer').hide()
  $('.bee_icon').hide()
  draw_charts()

  function parse_variance_table(old_ratio_array, ratio_array, variance_list) {
    var item_html = ''
    for (var i = 0; i < variance_list.length; i++) {
      var var_data = variance_list[i]
      var old_weight = old_ratio_array[i][1]*100
      var weight = ratio_array[i][1]*100
      var name = var_data[0]
      var code = var_data[1]
      var diff = var_data[2]*100
      if (diff >= 0) {
        var td_color = 'plus_td'
        var sign = '+'
      } else {
        var td_color = 'minus_td'
        var sign = ''
      }
      var variance_item = `
      <div class="variance_tr clear_col {0}">
          <div class="variance_td col">{1}({2})</div>
          <div class="variance_td val_td col">
              <span>{3}%</span>
              <span class="variance_icon"></span>
              <span>{4}% ({5}{6}%)</span>
          </div>
      </div>
      `.format(td_color, name, code, old_weight.toFixed(2), weight.toFixed(2), sign, diff.toFixed(2))
      item_html = item_html.concat(variance_item)
    }
    $('#variance_table_list').html(item_html)
  }

  function parse_port_info(ret, avg_ret, avg_vol, sharpe) {
    if (ret >= 0) {
      var line_color = 'plus_line'
      var sign = '+'
    } else {
      var line_color = 'minus_line'
      var sign = ''
    }
    if (avg_ret >= 0) {
      var td_color = 'plus_td'
    } else {
      var td_color = 'minux_td'
    }
    var port_html = `
    <div class="portfolio_name accent-color">포트폴리오 수익률</div>
    <div class="portfolio_increase {0}">{1}<span class="counter_num">{2}</span>%</div>
    <div class="info_portfolio_table_wrap">
        <table id="rms_portfolio_table" class="rms_info_table">
            <thead>
                <tr>
                    <th>평균 수익률</th>
                    <th>평균 변동성</th>
                    <th>샤프 지수</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td class="{3}">{4}%</td>
                    <td class="yellow_td">{5}%</td>
                    <td>{6}</td>
                </tr>
            </tbody>
        </table>
    </div>
    `.format(line_color, sign, ret.toFixed(2), td_color, avg_ret, avg_vol, sharpe)
    $('#port_info_area').html(port_html)
  }

  function draw_port_situation(place_id, data) {
    // 포트폴리오 현황
    var port_situation_chart = new Highcharts.Chart({
        title: {
            text: '',
            style: {
                display: 'none'
            }
        },
        subtitle: {
            text: '',
            style: {
                display: 'none'
            }
        },
        tooltip: {
            valueDecimals: 2
        },
        chart: {
            renderTo: place_id,
            type: 'pie',
            backgroundColor: '#27314f',
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                borderColor: '#27314f',
                innerSize: '60%',
                dataLabels: {
                    enabled: true,
                    style: {
                        color: 'white'
                    }
                }
            }
        },
        series: [{
            name: '비중',
            data: data}]
      },
      // using
      function(port_situation_chart) { // on complete
          var xpos = '50%'
          var ypos = '53%'
          var circleradius = 102
      // Render the circle
      port_situation_chart.renderer.circle(xpos, ypos, circleradius).attr({
          fill: '#27314f',
      }).add()
    })
  }

  function draw_port_spec(data) {
    // 포트폴리오 스펙
    var port_spec_chart = new Highcharts.Chart({
      title: {
          text: ''
      },
      chart: {
          renderTo: 'port_spec',
          polar: true,
          type: 'line',
          backgroundColor: '#27314f',
      },
      credits: {
          enabled: false
      },
      pane: {
          size: '85%'
      },
      xAxis: {
          categories: ['전체', '수익성', '안정성', '독립성', '거래량'],
          tickmarkPlacement: 'on',
          lineWidth: 0,
          labels: {
            style: {
              color: 'white'
            }
          }
      },
      yAxis: {
          gridLineInterpolation: 'polygon',
          lineWidth: 0,
          min: 0,
          max: 100,
          labels: {
            style: {
              color: 'white'
            }
          }
      },
      legend: {
          enabled: false
      },
      series: [{
          name: '점수',
          data: data,
          pointPlacement: 'on',
          color: '#E99364'
      }]
    })
  }

  function draw_result_graph(algo, bm) {
    // 사용자 포트폴리오
    var result_graph = new Highcharts.stockChart({
      title: {
          text: '',
          style: {
              display: 'none'
          }
      },
      chart: {
          renderTo: 'result_graph2',
          backgroundColor: '#27314f',
          height: 320,
      },
      credits: {
          enabled: false
      },
      xAxis: {
          tickmarkPlacement: 'on',
          lineWidth: 0,
          tickLength: 0,
          labels: {
            style: {
              color: 'silver'
            }
          }
      },
      yAxis: {
          lineWidth: 0,
          // min: 0,
          labels: {
            style: {
              color: 'white'
            }
          },
          gridLineColor: '#0A163A'
      },
      rangeSelector: {
         buttonTheme: {
            fill: '#505053',
            stroke: '#000000',
            style: {
               color: '#CCC'
            },
            states: {
               hover: {
                  fill: '#707073',
                  stroke: '#000000',
                  style: {
                     color: 'white'
                  }
               },
               select: {
                  fill: '#000003',
                  stroke: '#000000',
                  style: {
                     color: 'white'
                  }
               }
            }
         },
         inputBoxBorderColor: '#505053',
         inputStyle: {
            backgroundColor: '#333',
            color: 'silver'
         },
         labelStyle: {
            color: 'silver'
         }
      },
      navigator: {
         enabled: false
      },
      scrollbar: {
         enabled: false
      },
      series: [
      {
          name: 'Algorithm',
          data: algo,
          type: 'areaspline',
          threshold: null,
          tooltip: {
              valueDecimals: 2
          },
          color: 'white',
          lineWidth: 1,
          states: {
              hover: {
                  enabled: true
              }
          },
          fillColor: {
              linearGradient: {
                  x1: 0,
                  y1: 0,
                  x2: 0,
                  y2: 1
              },
              stops: [
                  [0, Highcharts.Color(Highcharts.getOptions().colors[7]).setOpacity(0.6).get('rgba')],
                  [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
              ]
          }
      },
      {
          name: 'Benchmark',
          data: bm,
          tooltip: {
              valueDecimals: 2
          },
          color: 'red',
          dataLabels: {
             color: 'red'
          },
          marker: {
             lineColor: 'red'
          },
          lineWidth: 1,
          states: {
              hover: {
                  enabled: true
              }
          }
      }]
    })
  }

})(jQuery)
