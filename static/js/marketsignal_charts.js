(function($) {

  String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted
  }

  $.getJSON('/stock-api/bm/?name=KOSPI&&ordering=date', function(data) {
      var processed_data = []
      for (var d in data['results']) {
        var d_in = []
        d_in.push(data['results'][d]['date'])
        d_in.push(data['results'][d]['index'])
        processed_data.push(d_in)
      }
      console.log(processed_data)
      Highcharts.stockChart('kospi_chart', {
          chart: {
              backgroundColor: '#27314f',
          },
          title: {
              text: ''
          },
          subtitle: {
              text: ''
          },
          xAxis: {
              lineColor: 'transparent',
              labels: {
                  style: {
                    color: '#27314f'
                  }
              },
              minorTickLength: 0,
              tickLength: 0
          },
          yAxis: {
              title: {
                  text: ''
              },
              gridLineColor: 'transparent',
              labels: {
                  enabled: false
              },
          },
          legend: {
              enabled: false
          },
          credits: {
              enabled: false
          },
          rangeSelector: {
              enabled: false
          },
          navigator: {
             enabled: false
          },
          scrollbar: {
             enabled: false
          },
          series: [{
              name: 'KOSPI',
              color: '#bdc3c7',
              data: processed_data,
              tooltip: {
                  valueDecimals: 2
              }
          }]
      });
  });

  $.getJSON('/stock-api/bm/?name=KOSDAQ&&ordering=date', function(data) {
      var processed_data = []
      for (var d in data['results']) {
        var d_in = []
        d_in.push(data['results'][d]['date'])
        d_in.push(data['results'][d]['index'])
        processed_data.push(d_in)
      }
      console.log(processed_data)
      Highcharts.stockChart('kosdaq_chart', {
          chart: {
              backgroundColor: '#27314f',
          },
          title: {
              text: ''
          },
          subtitle: {
              text: ''
          },
          xAxis: {
              lineColor: 'transparent',
              labels: {
                  style: {
                    color: '#27314f'
                  }
              },
              minorTickLength: 0,
              tickLength: 0
          },
          yAxis: {
              title: {
                  text: ''
              },
              gridLineColor: 'transparent',
              labels: {
                  enabled: false
              },
          },
          legend: {
              enabled: false
          },
          credits: {
              enabled: false
          },
          rangeSelector: {
              enabled: false
          },
          navigator: {
             enabled: false
          },
          scrollbar: {
             enabled: false
          },
          series: [{
              name: 'KOSDAQ',
              color: '#bdc3c7',
              data: processed_data,
              tooltip: {
                  valueDecimals: 2
              }
          }]
      });
  });

  // $.ajax({
  //   method: "GET",
  //   url: '/stock-api/bm/?name=KOSPI&&ordering=date',
  //   success: function(data){
  //     var processed_data = []
  //     for (var d in data['results']) {
  //       var d_in = []
  //       d_in.push(data['results'][d]['date'])
  //       d_in.push(data['results'][d]['index'])
  //       processed_data.push(d_in)
  //     }
  //     console.log(processed_data)
  //     draw_kospi(processed_data)
  //   },
  //   error: function(data){
  //     console.log('error')
  //   }
  // })

  function draw_kospi(data) {
    Highcharts.chart('chart_graph_wrap1', {
        chart: {
            type: 'spline',
            backgroundColor: '#27314f',
        },
        title: {
            text: ''
        },
        subtitle: {
            text: ''
        },
        xAxis: {
            lineColor: 'transparent',
            labels: {
                enabled: false
            },
            minorTickLength: 0,
            tickLength: 0
        },
        yAxis: {
            title: {
                text: ''
            },
            gridLineColor: 'transparent',
            labels: {
                enabled: false
            },
        },
        legend: {
            enabled: false
        },
        credits: {
            enabled: false
        },
        plotOptions: {
            series: {
                label: {
                    connectorAllowed: false
                },
                pointStart: data[0][0]
            }
        },
        series: [{
            name: 'KOSPI',
            data: data
        }],
    });
  }
  // $.getJSON('/api/index/?category=S&&name=L', function(data) {
  //     var processed_data = []
  //     for (var d in data['results']) {
  //       var d_in = []
  //       d_in.push(data['results'][d]['date'])
  //       d_in.push(data['results'][d]['index'])
  //       processed_data.push(d_in)
  //     }
  //     console.log(processed_data)
  //
  //     seriesOptions = [{
  //         name: name,
  //         data: processed_data
  //     }]
  //
  //     Highcharts.stockChart('chart_graph_wrap1', {
  //         chart: {
  //             type: 'line',
  //             backgroundColor: '#27314f',
  //         },
  //         yAxis: {
  //             labels: {
  //                 formatter: function () {
  //                     return (this.value > 0 ? ' + ' : '') + this.value + '%';
  //                 }
  //             },
  //             plotLines: [{
  //                 value: 0,
  //                 width: 2,
  //                 color: 'silver'
  //             }]
  //         },
  //         plotOptions: {
  //             series: {
  //                 compare: 'percent',
  //                 showInNavigator: true
  //             }
  //         },
  //         tooltip: {
  //             pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
  //             valueDecimals: 2,
  //             split: true
  //         },
  //         series: seriesOptions
  //     })
  // });

  // $.ajax({
  //   method: "GET",
  //   url: '/api/index/?category=S&&name=L',
  //   success: function(data){
  //     console.log(data)
  //   },
  //   error: function(data){
  //     console.log('error')
  //   }
  // })

  function draw_charts() {
    var port_id = $('#saved_port_id').attr('value')

    $.ajax({
      method: "GET",
      url: '/api/portfolio/' + port_id + '/diagnosis/',
      success: function(data){
        $('#loader-wrapper').fadeOut(1000)
        $('#rms_portfolio_section').fadeIn(1000)
        $('#sub_footer').fadeIn(1000)
        $('.bee_icon').fadeIn(1000)

        var ratio = data.port_info.ratio
        var left_ratio = 1
        var ratio_array = []
        for (var key in ratio) {
          if (key != 'cash') {
            var ratio_point = parseFloat(ratio[key]['ratio'])
            var ratio_data = [ratio[key]['name'], ratio_point*100]
            ratio_array.push(ratio_data)
            left_ratio -= ratio_point
          } else {
            // pass
          }
        }
        var ratio_data = ['현금', left_ratio*100]
        ratio_array.push(ratio_data)
        draw_port_situation(ratio_array)

        var port_spec = data.port_specs
        draw_port_spec(port_spec)

        var ret = data.port_info.return
        var avg_ret = data.port_info.average_return
        var avg_vol = data.port_info.average_volatility
        var sharpe = data.port_info.sharpe_ratio
        parse_port_info(ret, avg_ret, avg_vol, sharpe)

        console.log(data.port_info.backtest_result)
        var result = data.port_info.backtest_result
        var algo = result['Portfolio']
        var bm = result['Benchmark']
        draw_result_graph(algo, bm)

        var algo_1mon = algo.slice(-1)[1] - algo.slice(-2)[1]
        console.log(algo_1mon)
      },
      error: function(data){
        console.log('error')
      }
    })
  }

  $('#rms_portfolio_section').hide()
  $('#sub_footer').hide()
  $('.bee_icon').hide()
  draw_charts()

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

  function draw_port_situation(data) {
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
            renderTo: 'port_situation',
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

  // // 시장
  // var port_situation_chart = new Highcharts.Chart({
  //     title: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     subtitle: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     chart: {
  //         renderTo: 'market_chart',
  //         type: 'pie',
  //         backgroundColor: '#27314f',
  //     },
  //     credits: {
  //         enabled: false
  //     },
  //     plotOptions: {
  //         pie: {
  //             allowPointSelect: true,
  //             cursor: 'pointer',
  //             borderColor: '#27314f',
  //             innerSize: '60%',
  //             dataLabels: {
  //                 enabled: true,
  //                 style: {
  //                     color: 'white'
  //                 }
  //             }
  //         }
  //     },
  //     series: [{
  //         name: '비중',
  //         data: [
  //             ['Firefox', 44.2],
  //             ['IE7', 26.6],
  //             ['IE6', 20],
  //             ['Chrome', 3.1],
  //             ['Other', 5.4]
  //             ]}]
  //   },
  //   // using
  //   function(port_situation_chart) { // on complete
  //       var xpos = '50%'
  //       var ypos = '53%'
  //       var circleradius = 102
  //   // Render the circle
  //   port_situation_chart.renderer.circle(xpos, ypos, circleradius).attr({
  //       fill: '#27314f',
  //   }).add()
  // })
  //
  // // 사이즈
  // var port_situation_chart = new Highcharts.Chart({
  //     title: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     subtitle: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     chart: {
  //         renderTo: 'size_chart',
  //         type: 'pie',
  //         backgroundColor: '#27314f',
  //     },
  //     credits: {
  //         enabled: false
  //     },
  //     plotOptions: {
  //         pie: {
  //             allowPointSelect: true,
  //             cursor: 'pointer',
  //             borderColor: '#27314f',
  //             innerSize: '60%',
  //             dataLabels: {
  //                 enabled: true,
  //                 style: {
  //                     color: 'white'
  //                 }
  //             }
  //         }
  //     },
  //     series: [{
  //         name: '비중',
  //         data: [
  //             ['Firefox', 44.2],
  //             ['IE7', 26.6],
  //             ['IE6', 20],
  //             ['Chrome', 3.1],
  //             ['Other', 5.4]
  //             ]}]
  //   },
  //   // using
  //   function(port_situation_chart) { // on complete
  //       var xpos = '50%'
  //       var ypos = '53%'
  //       var circleradius = 102
  //   // Render the circle
  //   port_situation_chart.renderer.circle(xpos, ypos, circleradius).attr({
  //       fill: '#27314f',
  //   }).add()
  // })
  //
  // // 스타일
  // var port_situation_chart = new Highcharts.Chart({
  //     title: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     subtitle: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     chart: {
  //         renderTo: 'style_chart',
  //         type: 'pie',
  //         backgroundColor: '#27314f',
  //     },
  //     credits: {
  //         enabled: false
  //     },
  //     plotOptions: {
  //         pie: {
  //             allowPointSelect: true,
  //             cursor: 'pointer',
  //             borderColor: '#27314f',
  //             innerSize: '60%',
  //             dataLabels: {
  //                 enabled: true,
  //                 style: {
  //                     color: 'white'
  //                 }
  //             }
  //         }
  //     },
  //     series: [{
  //         name: '비중',
  //         data: [
  //             ['Firefox', 44.2],
  //             ['IE7', 26.6],
  //             ['IE6', 20],
  //             ['Chrome', 3.1],
  //             ['Other', 5.4]
  //             ]}]
  //   },
  //   // using
  //   function(port_situation_chart) { // on complete
  //       var xpos = '50%'
  //       var ypos = '53%'
  //       var circleradius = 102
  //   // Render the circle
  //   port_situation_chart.renderer.circle(xpos, ypos, circleradius).attr({
  //       fill: '#27314f',
  //   }).add()
  // })
  //
  // // 섹터
  // var port_situation_chart = new Highcharts.Chart({
  //     title: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     subtitle: {
  //         text: '',
  //         style: {
  //             display: 'none'
  //         }
  //     },
  //     chart: {
  //         renderTo: 'sector_chart',
  //         type: 'pie',
  //         backgroundColor: '#27314f',
  //     },
  //     credits: {
  //         enabled: false
  //     },
  //     plotOptions: {
  //         pie: {
  //             allowPointSelect: true,
  //             cursor: 'pointer',
  //             borderColor: '#27314f',
  //             innerSize: '60%',
  //             dataLabels: {
  //                 enabled: true,
  //                 style: {
  //                     color: 'white'
  //                 }
  //             }
  //         }
  //     },
  //     series: [{
  //         name: '비중',
  //         data: [
  //             ['Firefox', 44.2],
  //             ['IE7', 26.6],
  //             ['IE6', 20],
  //             ['Chrome', 3.1],
  //             ['Other', 5.4]
  //             ]}]
  //   },
  //   // using
  //   function(port_situation_chart) { // on complete
  //       var xpos = '50%'
  //       var ypos = '53%'
  //       var circleradius = 102
  //   // Render the circle
  //   port_situation_chart.renderer.circle(xpos, ypos, circleradius).attr({
  //       fill: '#27314f',
  //   }).add()
  // })

})(jQuery)
