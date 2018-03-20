(function($) {

  String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted;
  }

  function getTodayDate() {
    var dt = new Date();
    var month = dt.getMonth() + 1;
    var day = dt.getDate();
    var year = dt.getFullYear();

    return [year,
            (month>9 ? '' : '0') + month,
            (day>9 ? '' : '0') + day
          ].join('');
  }

  function getStartDate(range) {
    var today = new Date();
    var start = new Date();

    switch(range) {
      case "1week":
        start.setDate(today.getDate() - 7)
        break;
      case "1month":
        start.setMonth(today.getMonth() - 1)
        break;
      case "3month":
        start.setMonth(today.getMonth() - 3)
        break;
      case "6month":
        start.setMonth(today.getMonth() - 6)
        break;
      case "1year":
        start.setYear(today.getFullYear() - 1)
        break;
      default:
        break;
    }

    date = [start.getFullYear(),
            (start.getMonth()>8 ? '' : '0') + (start.getMonth()+1),
            (start.getDate()>9 ? '' : '0') + start.getDate()
          ].join('');
    return date;

  }



  function createChart(id, data, colorSet) {
      Highcharts.stockChart(id, {
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
              gridLineColor: '#545b64',
              labels: {
                style: {
                  color: 'pink'
                }
             // formatter: function () {
             //     return (this.value > 0 ? ' + ' : '') + this.value;
             // }
              },
             plotLines: [{
                 value: 0,
                 width: 2,
                 // color: 'red'
               }]
          },
          colors: colorSet,
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
          // plotOptions: {
          //     series: {
          //         compare: 'percent',
          //         showInNavigator: true
          //     }
          // },
          tooltip: {
              pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b><br/>', // ({point.change}%)
              valueDecimals: 2,
              split: true
          },
          series: data

      });
  }

  //kospi, kosda chart
  function makeOneLineChart(chartName, url, name, lineColors, start, end){
    $.getJSON(url + name + '&start=' + start + '&end=' + end + '&&ordering=date', function(data) {
        var processed_data = []
        for (var d in data['results']) {
          var d_in = []
          d_in.push(data['results'][d]['date'])
          d_in.push(data['results'][d]['index'])
          processed_data.push(d_in)
        }
        seriesOptions = [{
          name: name,
          color: 'silver',
          data: processed_data,
          tooltip: {
              valueDecimals: 2
          }
        }]
        createChart(chartName, seriesOptions, lineColors);
    })
  }

  //size, style, sector chart
  function makeManyLineChart(chartName, url, names, start, end,
                            lineColors, seriesOptions, seriesCounter)
  {
      $.each(names, function(i, name) {
        $.getJSON(url + name + '&start=' + start + '&end=' + end +'&ordering=date', function(data) {
          var processed_data = []
          for (var d in data) {
            var d_in = []
            d_in.push(data[d]['date'])
            d_in.push(data[d]['index'])
            processed_data.push(d_in)
          }

          seriesOptions[i] = {
            name: name,
            data: processed_data,
          };
          seriesCounter += 1;

          if (seriesCounter === names.length) {
            createChart(chartName, seriesOptions, lineColors);
          }
        })
      })
  }


//ranking_chart
function makeRankingChart(chartName, url, code, start, end){
  $.getJSON(url + code + '&start=' + start + '&end=' + end + '&ordering=date', function(data) {
      var processed_data = []
      for (var d in data['results']) {
        var d_in = []
        d_in.push(data['results'][d]['date'])
        d_in.push(data['results'][d]['close_price'])
        processed_data.push(d_in)
      }
      // console.log(processed_data)
      Highcharts.StockChart(chartName, {
        chart : {
            backgroundColor:'#0a163a',
            renderTo : 'container',
            width: 300,
            height: 70,
            margin: [ 10, 5, 20, 5]
        },
        xAxis: {
          lineColor: 'transparent',
          title: {
              enabled: false
          },
          labels: {
            enabled: false
          },
          tickLength: 0
        },
        yAxis: {
          gridLineColor: 'transparent',
          title: {
            enabled: false
          },
          labels: {
            enabled: false
          },
          tickLength: 0
        },
        rangeSelector: {
         selected: 1
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
        series : [{
            name : 'SAMSUNG',
            data : processed_data,
            color : 'white',
            gapSize: 0,
            tooltip: {
                valueDecimals: 2
            },
            threshold: null
        }]
    });

    })
}


  //update!
  function updateData(chartId, url, names, chartColor, start, end) {
    var chart = $(chartId).highcharts()
    //delete old data for new series
    while(chart.series.length >0){
      chart.series[0].remove(true);
    }
    if (typeof names === 'string') {
      $.getJSON(url+ names +'&start='+ start +
               '&end=' + end + '&ordering=date', function(data)
        {
              var processed_data = []

              for (var d in data['results']) {
                var d_in = []
                d_in.push(data['results'][d]['date'])
                d_in.push(data['results'][d]['index'])
                processed_data.push(d_in)
              }

              //update series
              chart.addSeries({
                data: processed_data,
                color: chartColor[i]
              })
              chart.redraw();
      });
    } else {
      $.each(names, function(i, name) {
        $.getJSON(url + name + '&&start=' + start + '&&end='
                      + end +'&&ordering=date', function(data) {
          var processed_data = []

            for (var d in data) {
              var d_in = []
              d_in.push(data[d]['date'])
              d_in.push(data[d]['index'])
              processed_data.push(d_in)
            }

          //update
          chart.addSeries({
            name: name,
            data: processed_data,
            color: chartColor[i]
          })
          chart.redraw();

        })
      })
    }
  }


  //date
  todayDate = getTodayDate();
  startDate = getStartDate('1year') //default

  infoSet = [ ['#kospi_chart', '/stock-api/bm/?name=', 'KOSPI', ['white']],
            ['#kosdaq_chart', '/stock-api/bm/?name=', 'KOSDAQ', ['white']],
            ['#size_chart', '/ms-api/index/?category=S&&name=', ['L', 'M', 'S'], ['#00b9f1', '#f9c00c', '#f9320c']],
            ['#style_chart', '/ms-api/index/?category=ST&&name=', ['G', 'V'], ['red', 'silver']],
            ['#sector_chart', '/ms-api/top-industry/?rank=', ['1', '2', '3'], ['#2EC4B6', '#E71E36', '#EFFFE9']] ]


  //kospi, kosdaq, size, style. sector graph
  for (i=0; i<infoSet.length; i++) {
    if (infoSet[i][0] == '#kospi_chart' || infoSet[i][0] == '#kosdaq_chart') {
      makeOneLineChart(infoSet[i][0].slice(1), infoSet[i][1], infoSet[i][2], infoSet[i][3],
                        startDate, todayDate)
    } else {
      seriesOptions = [];
      seriesCounter = 0;
      makeManyLineChart(infoSet[i][0].slice(1), infoSet[i][1], infoSet[i][2],
                        startDate, todayDate, infoSet[i][3], seriesOptions, seriesCounter)
    }
  }

  //ranking_chart
  makeRankingChart('mini_chart', '/stock-api/ohlcv/?code=', '005930', getStartDate('1year'), todayDate)



  //change range
  $('#1weekBtn').click(infoSet, function() {
    $.each(infoSet, function(i, info){
      updateData(info[0], info[1], info[2], info[3], getStartDate('1week'), todayDate)

    })
  })

  $('#1monthBtn').click(infoSet, function(){
    $.each(infoSet, function(i, info){
      updateData(info[0], info[1], info[2], info[3], getStartDate('1month'), todayDate)
    })
  })

  $('#3monthBtn').click(infoSet, function(){
    $.each(infoSet, function(i, info){
      updateData(info[0], info[1], info[2], info[3], getStartDate('3month'), todayDate)

    })
  })

  $('#6monthBtn').click(infoSet, function(){
    $.each(infoSet, function(i, info){
      updateData(info[0], info[1], info[2], info[3], getStartDate('6month'), todayDate)
    })
  })

  $('#1yearBtn').click(infoSet, function(){
    $.each(infoSet, function(i, info){
      updateData(info[0], info[1], info[2], info[3], getStartDate('1year'), todayDate)
    })
  })

  function request_filter_rank(filter_by) {
    $.ajax({
      method: "GET",
      url: '/api/rank/?filter_by=' + filter_by,
      success: function(data){
        console.log(data)
        $.each(data.results, function(i, rankdata){
          if (i < 10) {
            var tr = `
            <tr>
                <td class="first_num left_td">
                    <div class="num_contents_wrap">
                        <div class="info_contetns clear_col">
                            <div class="up_down_icon"></div>
                            <div class="info_num">{0}</div>
                        </div>
                        <div class="normal_num">{1}</div>
                    </div>
                </td>
                <td class="left_td title_td"><a href="/marketsignal/snapshot/{2}">{3}</a></td>
                <td class="small">{4}</td>
                <td class="small">{5}</td>
                <td class="small">{6}</td>
                <!-- <td id='mini_chart' class="graph_td"></td> -->
                <td class="graph_td"></td>
                <td class="final_grade">
                    <div class="grade_contents">
                        <div class="grade_num">{7}</div>
                        <div class="cart_button" data-click="0">+</div>
                        <div class="cart_portfolio">
                            <div class="select_btn_wrap clear_col">
                                <div class="col cart_original_btn active">기존 포트폴리오</div>
                                <div class="col cart_new_btn">새로 만들기</div>
                            </div>
                            <div class="select_portfolio">
                                <div class="original_select active">
                                    <select>
                                        <option>선택</option>
                                    </select>
                                </div>
                                <div class="new_select">
                                    <input placeholder="포트폴리오 이름 입력" />
                                </div>
                            </div>
                            <div class="submit_btn">담기</div>
                        </div>
                    </div>
                </td>
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

  request_filter_rank('KOSPI')
  var active_filter = '#KOSPI'

  // get rank data by filter
  $('#KOSPI').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#KOSPI') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('KOSPI')

      this.parentElement.className = 'active'
      active_filter = '#KOSPI'
    }
  })

  $('#KOSDAQ').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#KOSDAQ') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('KOSDAQ')

      this.parentElement.className = 'active'
      active_filter = '#KOSDAQ'
    }
  })

  $('#L').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#L') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('L')

      this.parentElement.className = 'active'
      active_filter = '#L'
    }
  })

  $('#M').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#M') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('M')

      this.parentElement.className = 'active'
      active_filter = '#M'
    }
  })

  $('#S').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#S') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('S')

      this.parentElement.className = 'active'
      active_filter = '#S'
    }
  })

  $('#V').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#V') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('V')

      this.parentElement.className = 'active'
      active_filter = '#V'
    }
  })

  $('#G').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#G') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      request_filter_rank('G')

      this.parentElement.className = 'active'
      active_filter = '#G'
    }
  })

  $('#IND_1').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#IND_1') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      var filter_name = this.text
      request_filter_rank(filter_name)

      this.parentElement.className = 'active'
      active_filter = '#IND_1'
    }
  })

  $('#IND_2').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#IND_2') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      var filter_name = this.text
      request_filter_rank(filter_name)

      this.parentElement.className = 'active'
      active_filter = '#IND_2'
    }
  })

  $('#IND_3').click(function(){
    var par_el_class = this.parentElement.className
    if (par_el_class == 'active' || active_filter == '#IND_3') {
      // pass
    } else {
      $('.filter_rank_table').html('')
      var filter_name = this.text
      request_filter_rank(filter_name)

      this.parentElement.className = 'active'
      active_filter = '#IND_3'
    }
  })


  // $('#loader-wrapper').fadeOut(1000)
  // $('#market_section1').fadeIn(1000)
  // $('#market_section2').fadeIn(1000)
  // $('#sub_footer').fadeIn(1000)
  // $('.bee_icon').fadeIn(1000)

})(jQuery)
