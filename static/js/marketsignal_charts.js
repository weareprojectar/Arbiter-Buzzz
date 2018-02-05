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
          plotOptions: {
              series: {
                  compare: 'percent',
                  showInNavigator: true
              }
          },
          tooltip: {
              pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
              valueDecimals: 2,
              split: true
          },
          series: data
      });
  }

  var seriesOptions = [],
  seriesCounter = 0,
  names = ['L', 'M', 'S'];

  $.each(names, function (i, name) {
      $.getJSON('/api/index/?category=S&&name=' + name, function(data) {
          var processed_data = []
          for (var d in data['results']) {
            var d_in = []
            d_in.push(data['results'][d]['date'])
            d_in.push(data['results'][d]['index'])
            processed_data.push(d_in)
          }
          seriesOptions[i] = {
              name: name,
              data: processed_data
          };
          seriesCounter += 1;
          if (seriesCounter === names.length) {
              createChart('size_chart', seriesOptions);
          }
      });
  });

  var seriesOptions1 = [],
  seriesCounter1 = 0,
  names1 = ['G', 'V'];

  $.each(names1, function (i, name) {
      $.getJSON('/api/index/?category=ST&&name=' + name, function(data) {
          var processed_data1 = []
          for (var d in data['results']) {
            var d_in = []
            d_in.push(data['results'][d]['date'])
            d_in.push(data['results'][d]['index'])
            processed_data1.push(d_in)
          }
          seriesOptions1[i] = {
              name: name,
              data: processed_data1
          };
          seriesCounter1 += 1;
          if (seriesCounter1 === names.length) {
              createChart('style_chart', seriesOptions1);
          }
      });
  });

})(jQuery)
