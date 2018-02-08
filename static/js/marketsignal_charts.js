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

  function makeOneLineChart(name, chartName, lineColors){
    $.getJSON('/stock-api/bm/?name='+name+'&&ordering=date', function(data) {
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

  function makeManyLineChart(url, names, start, end, lineColors,
                          seriesOptions, seriesCounter, chartName)
  {
      $.each(names, function(i, name) {
        $.getJSON(url + name + '&&start=' + start + '&&end=' + end +'&&ordering=date', function(data) {
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
  $.getJSON('/stock-api/ohlcv/?code=005930&ordering=-date', function(data) {
        var processed_data = []
        for (var d in data['results']) {
          var d_in = []
          d_in.push(data['results'][d]['date'])
          d_in.push(data['results'][d]['close_price'])
          processed_data.push(d_in)
        }
        // console.log(processed_data)
          chart = new Highcharts.StockChart('mini_chart', {
            chart : {
                renderTo : 'container'
            },
            xAxis: {
              gridLineColor: 'transparent',
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
            margin: [ 2, 2, 2, 2],
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
                color : 'red',
                gapSize: 0,
                tooltip: {
                    valueDecimals: 2
                },
                threshold: null
            }]
        });

    })



  //update!
  function updateData(url, names, chartId, start, end, seriesOptions, seriesCounter) {
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
                data: processed_data
              })
              console.log(processed_data)
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

          seriesOptions[i] = {
            name: name,
            data: processed_data,
          };
          seriesCounter += 1


          if (seriesCounter === names.length){
            chart.addSeries({
              processed_data
            })
            chart.redraw();
          }
        })
      })
    }
  }



    todayDate = getTodayDate();
    startDate = '20170102';//tmp

    $('#1weekBtn').click(function(infoSet){
      infoSet = [['/stock-api/bm/?name=', 'KOSPI', '#kospi_chart'], ['/stock-api/bm/?name=', 'KOSDAQ', '#kosdaq_chart'],
                ['/api/index/?category=S&&name=', ['L', 'M', 'S'], '#size_chart'], ['/api/index/?category=ST&&name=', ['G', 'V'], '#style_chart'],
                  ]
      $.each(infoSet, function(i, info){
        var seriesOptions = []
        var seriesCounter = 0
        updateData(info[0], info[1], info[2],
              getStartDate('1week'), todayDate, seriesOptions, seriesCounter)

      })
    })
    $('#1monthBtn').click(function(){
      infoSet = [['/stock-api/bm/?name=', 'KOSPI', '#kospi_chart'], ['/stock-api/bm/?name=', 'KOSDAQ', '#kosdaq_chart']]
      $.each(infoSet, function(i, info){
        var seriesOptions = []
        var seriesCounter = 0
        updateData(info[0], info[1], info[2],
              getStartDate('1month'), todayDate, seriesOptions, seriesCounter)

      })
    })
    $('#3monthBtn').click(function(){
      infoSet = [['/stock-api/bm/?name=', 'KOSPI', '#kospi_chart'], ['/stock-api/bm/?name=', 'KOSDAQ', '#kosdaq_chart']]
      $.each(infoSet, function(i, info){
        var seriesOptions = []
        var seriesCounter = 0
        updateData(info[0], info[1], info[2],
              getStartDate('3month'), todayDate, seriesOptions, seriesCounter)

      })
    })
    $('#6monthBtn').click(function(){
      infoSet = [['/stock-api/bm/?name=', 'KOSPI', '#kospi_chart'], ['/stock-api/bm/?name=', 'KOSDAQ', '#kosdaq_chart']]
      $.each(infoSet, function(i, info){
        var seriesOptions = []
        var seriesCounter = 0
        updateData(info[0], info[1], info[2],
              getStartDate('6month'), todayDate, seriesOptions, seriesCounter)

      })
    })
    $('#1yearBtn').click(function(){
      infoSet = [['/stock-api/bm/?name=', 'KOSPI', '#kospi_chart'], ['/stock-api/bm/?name=', 'KOSDAQ', '#kosdaq_chart']]
      $.each(infoSet, function(i, info){
        var seriesOptions = []
        var seriesCounter = 0
        updateData(info[0], info[1], info[2],
              getStartDate('1year'), todayDate, seriesOptions, seriesCounter)

      })
    })




  //kospi_chart
  makeOneLineChart('KOSPI', 'kospi_chart', ['silver'])

  //kosdaq_chart
  makeOneLineChart('KOSDAQ', 'kosdaq_chart', ['silver'])

  //size_chart
  var sizeChartColor = ['orange', 'white', 'pink', '#04b8b8']
  var seriesOptions = [],
  seriesCounter = 0,
  sizeChartList = ['L', 'M', 'S'];

  makeManyLineChart('/api/index/?category=S&&name=', sizeChartList, startDate, todayDate,
            sizeChartColor, seriesOptions, seriesCounter, 'size_chart')


  //style_chart
  var styleChartColor = ['red', 'pink', 'silver']
  var seriesOptions1 = [],
  seriesCounter = 0,
  styleChartList = ['G', 'V'];

  makeManyLineChart('/api/index/?category=ST&&name=', styleChartList, startDate, todayDate,
            styleChartColor, seriesOptions1, seriesCounter, 'style_chart')





})(jQuery)
