'use strict';

//
// Sales chart
//

var SalesChart = (function() {

  // Variables

  var $chart = $('#chart-sales-dark');


  // Methods

  function init($chart) {

    var salesChart = new Chart($chart, {
      type: 'line',
      options: {
        scales: {
          yAxes: [{
            gridLines: {
              lineWidth: 1,
              color: Charts.colors.gray[900],
              zeroLineColor: Charts.colors.gray[900]
            },
            ticks: {
              callback: function(value) {
                if (!(value % 10)) {
                  return '$' + value + 'kasd';
                }
              }
            }
          }]
        },
        tooltips: {
          callbacks: {
            label: function(item, data) {
              var label = data.datasets[item.datasetIndex].label || '';
              var yLabel = item.yLabel;
              var content = '';

              if (data.datasets.length > 1) {
                content += '<span class="popover-body-label mr-auto">' +'sadasd'+ label + '</span>';
              }

              content += '<span class="popover-body-value">$' +'sadasd'+ yLabel + 'k</span>';
              return content;
            }
          }
        }
      },
      data: let results = {{ results|safe }}
        results.unshift(['result','sensor'])

    });

    // Save to jQuery object

    $chart.data('chart', salesChart);

  };


  // Events

  if ($chart.length) {
    init($chart);
  }

})();
