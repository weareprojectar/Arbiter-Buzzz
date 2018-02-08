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
    $.ajax({
      method: "POST",
      url: '/stock-api/candle/',
      data: {
          'code': window.location.href.slice(-7, -1),
          // 'csrfmiddlewaretoken': csrftoken
      },
      success: function(data){
        $('#loader-wrapper').fadeOut(1000)
        $('#defacto_section1').fadeIn(1000)
        $('#sub_footer').fadeIn(1000)
        $('.bee_icon').fadeIn(1000)
        // split the data set into ohlc and volume
        var ohlc = []
        var volume = []
        var data = data.candle_data
        var dataLength = data.length
        console.log(dataLength)

        var groupingUnits = [['week', [1]], ['month', [1, 2, 3, 4, 6]]]

        var i = 0;
        for (i; i < dataLength; i += 1) {
            ohlc.push([
                data[i][0], // the date
                data[i][1], // open
                data[i][2], // high
                data[i][3], // low
                data[i][4] // close
            ]);

            volume.push([
                data[i][0], // the date
                data[i][5] // the volume
            ]);
        }
        console.log(ohlc)
        console.log(volume)

        highchart_setup(groupingUnits, ohlc, volume)
      },
      error: function(data){
        console.log('error')
        console.log(data)
      }
    })
  }

  function highchart_setup(groupingUnits, ohlc, volume) {
    // create the chart
    Highcharts.stockChart('stock_chart', {

        rangeSelector: {
            selected: 2
        },

        title: {
            text: 'AAPL Historical'
        },

        subtitle: {
            text: 'With SMA and Volume by Price technical indicators'
        },

        yAxis: [{
            startOnTick: false,
            endOnTick: false,
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'OHLC'
            },
            height: '60%',
            lineWidth: 2,
            resize: {
                enabled: true
            }
        }, {
            labels: {
                align: 'right',
                x: -3
            },
            title: {
                text: 'Volume'
            },
            top: '65%',
            height: '35%',
            offset: 0,
            lineWidth: 2
        }],

        tooltip: {
            split: true
        },

        plotOptions: {
            series: {
                dataGrouping: {
                    units: groupingUnits
                }
            }
        },

        series: [{
            type: 'candlestick',
            name: 'AAPL',
            id: 'aapl',
            zIndex: 2,
            data: ohlc
        }, {
            type: 'column',
            name: 'Volume',
            id: 'volume',
            data: volume,
            yAxis: 1
        }, {
            type: 'vbp',
            linkedTo: 'aapl',
            params: {
                volumeSeriesID: 'volume'
            },
            dataLabels: {
                enabled: false
            },
            zoneLines: {
                enabled: false
            }
        }, {
            type: 'sma',
            linkedTo: 'aapl',
            zIndex: 1,
            marker: {
                enabled: false
            }
        }]
    });
  }

  $('#defacto_section1').hide()
  $('#sub_footer').hide()
  $('.bee_icon').hide()
  draw_chart()

})(jQuery)
