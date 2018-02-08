(function($) {

  String.prototype.format = function() {
    var formatted = this
    for (var i = 0; i < arguments.length; i++) {
        var regexp = new RegExp('\\{'+i+'\\}', 'gi')
        formatted = formatted.replace(regexp, arguments[i])
    }
    return formatted
  }

  function draw_chart() {
    var ticker = window.location.href.slice(-7, -1)
    $.getJSON('/stock-api/ohlcv/?code=' + ticker + '&ordering=-date', function(data) {
        var processed_data = []
        for (var d in data['results']) {
          var d_in = []
          d_in.push(data['results'][d]['date'])
          d_in.push(data['results'][d]['close_price'])
          processed_data.push(d_in)
        }
        seriesOptions = [{
          name: name,
          color: 'silver',
          data: processed_data.reverse(),
          tooltip: {
              valueDecimals: 2
          }
        }]
        $('#loader-wrapper').fadeOut(1000)
        $('#defacto_section1').fadeIn(1000)
        $('#sub_footer').fadeIn(1000)
        $('.bee_icon').fadeIn(1000)
        createChart('stock_chart', seriesOptions);
    })
  }

  function createChart(id, data) {
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

  $('#defacto_section1').hide()
  $('#sub_footer').hide()
  $('.bee_icon').hide()
  draw_chart()

})(jQuery)
