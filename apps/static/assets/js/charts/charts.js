var Charts = (function() {

    // Variables
    var $toggle = $('[data-toggle="chart"]');
    var mode = 'light';//(themeMode) ? themeMode : 'light';
    var fonts = {
        base: 'Open Sans'
    }

    // Colors
    var colors = {
        gray: {
            100: '#f6f9fc',
            200: '#e9ecef',
            300: '#dee2e6',
            400: '#ced4da',
            500: '#adb5bd',
            600: '#8898aa',
            700: '#525f7f',
            800: '#32325d',
            900: '#212529'
        },
        theme: {
            'default': '#172b4d',
            'primary': '#5e72e4',
            'secondary': '#f4f5f7',
            'info': '#11cdef',
            'success': '#2dce89',
            'danger': '#f5365c',
            'warning': '#fb6340'
        },
        black: '#12263F',
        white: '#FFFFFF',
        transparent: 'transparent',
    };


  // Methods
  // Chart.js global options
  // THE METHOD FOR THE CHART THAT SETS THE COLORS
  // AND ALSO THE OVERALL THEME
  function chartOptions() {
      // Options
      var options = {
          defaults: {
              global: {
                  responsive: true,
                  maintainAspectRatio: false,
                  defaultColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
                  defaultFontColor: (mode == 'dark') ? colors.gray[700] : colors.gray[600],
                  defaultFontFamily: fonts.base,
                  defaultFontSize: 13,
                  layout: {
                      padding: 0
                  },
                  legend: {
                      display: false,
                      position: 'bottom',
                      labels: {
                          usePointStyle: true,
                          padding: 16
                      }
                  },
                  elements: {
                      point: {
                          radius: 0,
                          backgroundColor: colors.theme['primary']
                      },
                      line: {
                          tension: .4,
                          borderWidth: 4,
                          borderColor: colors.theme['primary'],
                          backgroundColor: colors.transparent,
                          borderCapStyle: 'rounded'
                      },
                      rectangle: {
                          backgroundColor: colors.theme['warning']
                      },
                      arc: {
                          backgroundColor: colors.theme['primary'],
                          borderColor: (mode == 'dark') ? colors.gray[800] : colors.white,
                          borderWidth: 4
                      }
                  },
                  tooltips: {
                      enabled: true,
                      mode: 'index',
                      intersect: false,
                  }
              },
              doughnut: {
                  cutoutPercentage: 83,
                  legendCallback: function(chart) {
                      var data = chart.data;
                      var content = '';

                      data.labels.forEach(function(label, index) {
                          var bgColor = data.datasets[0].backgroundColor[index];

                          content += '<span class="chart-legend-item">';
                          content += '<i class="chart-legend-indicator" style="background-color: ' + bgColor + '"></i>';
                          content += label;
                          content += '</span>';
                      });
                      return content;
                  }
              }
          }
      }


      // THE CHART SECTION THAT SETS
      // THE LINES INSIDE THE CHART
      // yAxes
      Chart.scaleService.updateScaleDefaults('linear', {
          gridLines: {
              borderDash: [2],
              borderDashOffset: [2],
              color: (mode == 'dark') ? colors.gray[900] : colors.gray[300],
              drawBorder: false,
              drawTicks: false,
              drawOnChartArea: true,
              zeroLineWidth: 0,
              zeroLineColor: 'rgba(0,0,0,0)',
              zeroLineBorderDash: [2],
              zeroLineBorderDashOffset: [2]
          },
          ticks: {
              beginAtZero: true,
              padding: 10,
              callback: function(value) {
                  if (!(value % 10)) {
                      return value
                  }
              }
          }
      });

      // xAxes
      Chart.scaleService.updateScaleDefaults('category', {
          gridLines: {
              drawBorder: false,
              drawOnChartArea: false,
              drawTicks: false
          },
          ticks: {
              padding: 20
          },
          maxBarThickness: 10
      });
      return options;
  }


  // Parse global options
  function parseOptions(parent, options) {
      for (var item in options) {
          if (typeof options[item] !== 'object') {
              parent[item] = options[item];
          } else {
              parseOptions(parent[item], options[item]);
          }
      }
  }


  // Push options
  function pushOptions(parent, options) {
      for (var item in options) {
          if (Array.isArray(options[item])) {
              options[item].forEach(function(data) {
                  parent[item].push(data);
              });
          } else {
              pushOptions(parent[item], options[item]);
          }
      }
  }


  // Pop options
  function popOptions(parent, options) {
      for (var item in options) {
          if (Array.isArray(options[item])) {
              options[item].forEach(function(data) {
                  parent[item].pop();
              });
          } else {
              popOptions(parent[item], options[item]);
          }
      }
  }


  // Toggle options
  function toggleOptions(elem) {
      var options = elem.data('add');
      var $target = $(elem.data('target'));
      var $chart = $target.data('chart');

      if (elem.is(':checked')) {

          // Add options
          pushOptions($chart, options);

          // Update chart
          $chart.update();
      } else {

          // Remove options
          popOptions($chart, options);

          // Update chart
          $chart.update();
      }
  }

  // Update options
  function updateOptions(elem) {
      var options = elem.data('update');
      var $target = $(elem.data('target'));
      var $chart = $target.data('chart');

      // Parse options
      parseOptions($chart, options);

      // Toggle ticks
      toggleTicks(elem, $chart);

      // Update chart
      $chart.update();
  }

  // Toggle ticks
  function toggleTicks(elem, $chart) {

      if (elem.data('prefix') !== undefined || elem.data('prefix') !== undefined) {
          var prefix = elem.data('prefix') ? elem.data('prefix') : '';
          var suffix = elem.data('suffix') ? elem.data('suffix') : '';

          // Update ticks
          $chart.options.scales.yAxes[0].ticks.callback = function(value) {
              if (!(value % 10)) {
                  return prefix + value + suffix;
              }
          }

          // Update tooltips
          $chart.options.tooltips.callbacks.label = function(item, data) {
              var label = data.datasets[item.datasetIndex].label || '';
              var yLabel = item.yLabel;
              var content = '';

              if (data.datasets.length > 1) {
                  content += '<span class="popover-body-label mr-auto">' + label + '</span>';
              }

              content += '<span class="popover-body-value">' + prefix + yLabel + suffix + '</span>';
              return content;
          }

      }
  }


  // Events

  // Parse global options
  if (window.Chart) {
      parseOptions(Chart, chartOptions());
  }

  // Toggle options
  $toggle.on({
      'change': function() {
          var $this = $(this);

          if ($this.is('[data-add]')) {
              toggleOptions($this);
          }
      },
      'click': function() {
          var $this = $(this);

          if ($this.is('[data-update]')) {
              updateOptions($this);
          }
      }
  });


  // Return
  return {
      colors: colors,
      fonts: fonts,
      mode: mode
  };

})();
//  END OF CHARTS SHAPE AND COLOR DEFENITION


function stringfy(elem) {
    return elem.timestamp.split('T')[0]
}


//TIMESTAMPS
let times = []
fetch('/assissjo-api/api/farm-timestamps/')
.then((resp) => resp.json())//get data and turn it into JSON
.then(function(data){
    console.log(data);
    times = data.map(stringfy);
})
.catch(error => {
    console.error('Error:', error);
});



let sensor_chart;
const $chart = $('#chart-sensor-dark');
function init( $chart ) {
    fetch('/assissjo-api/api/farm-humidity-results/')
    .then((resp) => resp.json())//get data and turn it into JSON
    .then(function(data){
        let list_of_results = [];

        //this function turns the array of arrays (data) into one single array
        let flattenedArray = [];
        
        let i = 50;
        let j = 20;
        //place holder
        let itterator = 1
        for(let object of data){
            flattenedArray.push(object.humidity)
            list_of_results.push(
                {
                    label: `Sensor ID : ${object.sensor_id} \n Unit : (${object.unit}) \n and Value is `,
                    data: object.humidity,
                    borderColor: `rgba(200, ${i}, ${j})`,
                },                
            )
            i += 50;
            j += 10;
            itterator += 1;

            if(i >= 255){
                i = 0;
            }

            if(j >= 255){
                j = 0;
            }
        }
        
        flattenedArray = flattenedArray.flat();
        const chart_share = new Chart(($chart), {
            type: 'line',
            data:  {
                labels: times,
                datasets: list_of_results
            },
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                    callback:(value)=>value,
                    max: Math.max(...flattenedArray),
                    min: Math.min(...flattenedArray),
                    stepSize: 1
                    }
                }]
            }
            }
        });

        // VARIABLE FOR OUTSIDE CHART USAGE
        sensor_chart = chart_share;

        let month_button = document.getElementById('humidity-chart-month');
        month_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-month/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
            
        })

        let week_button = document.getElementById('humidity-chart-week');
        week_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-week/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
        })
          
    })
    .catch(error => {
        console.error('Error:', error);
    });
};
//  END HUMIDITY SENSOR RESULTS ************************** */


let watertank_chart;  
const $water_tank_chart = $('#chart-watertank-dark');
function init_water_tank($water_tank_chart) {
    fetch('/assissjo-api/api/farm-general-results/capacity')
    .then((resp) => resp.json())//get data and turn it into JSON
    .then(function(response){
        let list_of_results = [];

        


        
        //TIMESTAMPS
        let timesWater = []
        fetch('/assissjo-api/api/farm-timestamps/capacity')
        .then((resp) => resp.json())//get data and turn it into JSON
        .then(function(data){
            //this function turns the array of arrays (data) into one single array
            let flattenedArray = []
            
            let i = 50;
            let j = 20;
            //place holder
            let itterator = 1
            for(let object of response){
                flattenedArray.push(object.number)            
                list_of_results.push(
                    {
                        label: `Water Tank ID : ${object.unit} \n Unit : ${object.unit} \n and Value is`,
                        data: object.number,
                        borderColor: `rgba(200, ${i}, ${j})`,
                    },                
                )
                i += 50;
                j += 10;
                itterator += 1;

                if(i >= 255){
                    i = 0;
                }

                if(j >= 255){
                    j = 0;
                }
            }
            console.log(data);
            timesWater = data.map(stringfy);
            flattenedArray = flattenedArray.flat()
            const chart_share = new Chart(($water_tank_chart), {
                type: 'line',
                data:  {
                    labels: timesWater,
                    datasets: list_of_results
                },
                options: {
                scales: {
                    yAxes: [{
                        ticks: {
                        callback:(value)=>value,
                        max: Math.max(...flattenedArray),
                        min: Math.min(...flattenedArray),
                        stepSize: 1
                        }
                    }]
                }
                }
            });
        })
        .catch(error => {
            console.error('Error:', error);
        });
        

        // VARIABLE FOR OUTSIDE CHART USAGE
        watertank_chart = chart_share;

        let month_button = document.getElementById('watertank-chart-month');
        month_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-month/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
            
        })

        let week_button = document.getElementById('watertank-chart-week');
        week_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-week/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
        })
          
    })
    .catch(function(error){
        console.error('Error:', error);
    });
};
// END OF WATER TANK CHART  



//WATER SHARE CHART
let watershare_chart;
const $water_share_chart = $('#chart-watershare-dark');
function init_water_share($water_share_chart) {
    fetch('/assissjo-api/api/farm-water-share/')
    .then((resp) => resp.json())//get data and turn it into JSON
    .then(function(response){
        let list_of_results = [];

        //this function turns the array of arrays (data) into one single array
        let flattenedArray = [];
        // console.log(flattenedArray)
        
        let i = 50;
        let j = 20;

        // //place holder
        // let itterator = 1
        for(let object of response){
            flattenedArray.push(object.shares)            

            list_of_results.push(
                {
                    label: `Tree ID : ${object.tree_id} \n Unit : (${object.unit}) \n and Value is `,
                    data: object.shares,
                    borderColor: `rgba(200, ${i}, ${j})`,
                },                
            )
            i += 50;
            j += 10;            

            if(i >= 255){
                i = 0;
            }

            if(j >= 255){
                j = 0;
            }
        }

        flattenedArray = flattenedArray.flat()
        const chart_share = new Chart(($water_share_chart), {
            type: 'line',
            data:  {
                labels: times,
                datasets: list_of_results
            },
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                    callback:(value)=>value,
                    max: Math.max(...flattenedArray),
                    min: Math.min(...flattenedArray),
                    stepSize: 1
                    }
                }]
            }
            }
        });

        // VARIABLE FOR OUTSIDE CHART USAGE
        watershare_chart = chart_share;
          
        let month_button = document.getElementById('watershare-chart-month');
        month_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-month/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })  
        })

        let week_button = document.getElementById('watershare-chart-week');
        week_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-week/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
        })

    })
    .catch(error => {
        console.error('Error:', error);
    });    
};
// END OF WATER SHARE CHART


// VALVE FLOW CHART
let valveflow_chart;
const $valve_flow_chart = $('#chart-valve-dark');
function init_valve_flow($valve_flow_chart) {
    fetch('/assissjo-api/api/farm-valveflow-results/')
    .then((resp) => resp.json())//get data and turn it into JSON
    .then(function(data){
        let list_of_results = [];

        //this function turns the array of arrays (data) into one single array
        let flattenedArray = [];
        
        let i = 50;
        let j = 20;
        //place holder
        let itterator = 1
        for(let object of data){
            flattenedArray.push(object.valve_flow_results)
            list_of_results.push(
                {
                    label: `Valve ID ${object.valve_id} \n Unit : (${object.unit}) \n and Value is `,
                    data: object.valve_flow_results,
                    borderColor: `rgba(200, ${i}, ${j})`,
                },                
            )
            i += 50;
            j += 10;
            itterator += 1;

            if(i >= 255){
                i = 0;
            }

            if(j >= 255){
                j = 0;
            }
        }

        flattenedArray = flattenedArray.flat()
        const chart_share = new Chart(($valve_flow_chart), {
            type: 'line',
            data:  {
                labels: times,
                datasets: list_of_results
            },
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                    callback:(value)=>value,
                    max: Math.max(...flattenedArray),
                    min: Math.min(...flattenedArray),
                    stepSize: 1
                    }
                }]
            }
            }
        });

        // VARIABLE FOR OUTSIDE CHART USAGE
        valveflow_chart = chart_share;
          
        let month_button = document.getElementById('valve-chart-month');
        month_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-month/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
            
        })

        let week_button = document.getElementById('valve-chart-week');
        week_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-week/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
        })

    })
    .catch(error => {
        console.error('Error:', error);
    });
};
// END POF VALVE FLOWMETER CHART


// ENERGY LEVEL CHART
let energylevel_chart;
function init_energy_level(energy_level_chart) {
    fetch('/assissjo-api/api/farm-energy-levels/')
    .then((resp) => resp.json())//get data and turn it into JSON
    .then(function(data){
        let list_of_results = [];

        //this function turns the array of arrays (data) into one single array
        let flattenedArray = [];
        
        let i = 50
        let j = 20
        //place holder
        let itterator = 1
        for(let object of data){
            flattenedArray.push(object.energy_levels)
            list_of_results.push(
                {
                    label: `Water Pump ID. ${object.Water_pump_id} \n Unit : (${object.unit}) \n and Value is `,
                    data: object.energy_levels,
                    borderColor: `rgba(200, ${i}, ${j})`,
                },                
            )
            i += 50;
            j += 10;
            itterator += 1;
            
            if(i >= 255){
                i = 0;
            }

            if(j >= 255){
                j = 0;
            }
        }

        flattenedArray = flattenedArray.flat()
        const chart_share = new Chart($(energy_level_chart[0]), {
            type: 'line',
            data:  {
                labels: times,
                datasets: list_of_results
            },
            options: {
            scales: {
                yAxes: [{
                    ticks: {
                    callback:(value)=>value,
                    max: Math.max(...flattenedArray),
                    min: Math.min(...flattenedArray),
                    stepSize: 1
                    }
                }]
            }
            }
        });

        // VARIABLE FOR OUTSIDE CHART USAGE
        energylevel_chart = chart_share;

        let month_button = document.getElementById('energylevel-chart-month');
        month_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-month/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
            
        })

        let week_button = document.getElementById('energylevel-chart-week');
        week_button.addEventListener('click', () => {
            fetch('/assissjo-api/api/farm-timestamps-week/')
            .then((resp) => resp.json())
            .then((data) => {
                chart_share.data.labels = data;
                chart_share.update();
            })
        })

    })
    .catch(error => {
        console.error('Error:', error);
    });
};
// END OF ENERGY LEVEL CHART


// Events
//HUMIDITY LEVEL CHART
$(document).ready(function(){
    init($chart);
});


//WATER TANK CHART
$(document).ready(function(){
    init_water_tank($water_tank_chart);
});

// WATER SHARE
$(document).ready(function(){
    init_water_share($water_share_chart);
});


// VALVE FLOW METER CHART
$(document).ready(function(){
    init_valve_flow($valve_flow_chart);
});


// ENERGY LEVEL CHART
$(document).ready(function(){
    init_energy_level($('#chart-energy-level-dark'));
});



// if ($energy_level_chart.length) {
//     init_energy_level($energy_level_chart);
// };


// TIME FILTER SECTION
let time_filter = document.getElementById('time-filter-button');
time_filter.addEventListener('click', (event) =>{
    event.preventDefault();

    let start_date = document.getElementById('start-date').value;
    let end_date = document.getElementById('end-date').value;   
    
    // API call
    fetch(`/assissjo-api/api/farm-timestamps/?start-date=${start_date}&end-date=${end_date}`)
            .then(response => response.json())
            .then((data) => {
                //assignment section
                sensor_chart.data.labels = data;
                watertank_chart.data.labels = data;
                watershare_chart.data.labels = data;
                valveflow_chart.data.labels = data;
                energylevel_chart.data.labels = data;

                //chart updating section
                sensor_chart.update();
                watertank_chart.update();
                watershare_chart.update();
                valveflow_chart.update();
                energylevel_chart.update();

                console.log('success')
            })
            .catch(error => console.error('Error fetching data:', error));
})







/*
 
    OLD IMPLEMENTATION AND CODE UNDERNEATH FOR DOCMENTATION AND REFERENCE PURPOSES


        <script>

    //CHARTS VIEW SECTION
    // Variables
    // let times = {{ times2|safe }};
      // 3 9 3 2 new Date(3)
      
</script>


//CHARTS VIEW SECTION
// Variables
//   let times = {{ times2|safe }};
//   3 9 3 2 new Date(3)
//   let results = {{ sensor_results|safe }};
  // {#let numbers = numbersss.map(function(result) {return new Date(result);});#}
  // let chartData = results.map((result,index)=> (result));


// let water_tank_results = {{ water_tank_results|safe }};
// const $water_tank_chart = $('#chart-watertank-dark');
// function init_water_tank($water_tank_chart) {
//     const chart_tank = new Chart($water_tank_chart, {
//         type: 'line',
//         data:  {
//             labels: times,
//             datasets: [{
//               label: 'WaterTank',
//               data: water_tank_results
//             }]
//         },
//         options: {
//         scales: {
//             yAxes: [{

//                 ticks: {
//                 callback:(value)=>value,
//                 max: Math.max(...water_tank_results),
//                 min: Math.min(...water_tank_results),
//                 stepSize: 1
//             }
//         }]
//     }
// }
//     });

// // Save to jQuery object

// /* {#$chart.data('chart', chart);#}

// };

    // // {#let numbers = numbersss.map(function(result) {return new Date(result);});#}
    // // let chartData = results.map((result,index)=> (result));


    // const $chart = $('#chart-sensor-dark');
    // function init( $chart ) {
    //     const chart = new Chart( $chart , {
    //         type: 'line',
    //         data:  {
    //             labels: times,
    //             datasets: [
    //                 {% for sensor in list_of_humidity_results %}
    //                     {
    //                     label: "Sensor ID.{{ humidity_sensors.id }}",
    //                     data: {{ sensor|safe }},
    //                     },
    //                 {% endfor %}
    //             ]
    //         },
    //         options: {
    //             scales: {
    //                 yAxes: [{
    //                     ticks: {
    //                         callback:(value)=>value,
    //                         max: Math.max(...results),
    //                         min: Math.min(...results),
    //                         stepSize: 1
    //                     }
    //                 }]
    //             }
    //         }
    //     });// Save to jQuery object{#$chart.data('chart', chart);#}

    // };
    // //  END HUMIDITY SENSOR RESULTS ************************** */

    // let water_share_results = {{ water_share_results|safe }};
    // const $water_share_chart = $('#chart-watershare-dark');
    // function init_water_share($water_share_chart) {
    //     const chart_share = new Chart($water_share_chart, {
    //         type: 'line',
    //         data:  {
    //             labels: times,
    //             datasets: [
    //                 {% for tree in list_of_watershare_results %}
    //                 {
    //                     label: 'Tree ID.{{ tree.id }}',
    //                     data: {{ tree|safe }},
    //                 },
    //                 {% endfor %}
    //             ]
    //         },
    //         options: {
    //         scales: {
    //             yAxes: [{
    //                 ticks: {
    //                 callback:(value)=>value,
    //                 max: Math.max(...water_share_results),
    //                 min: Math.min(...water_share_results),
    //                 stepSize: 1
    //             }
    //         }]
    //     }
    // }
    //     });

    // Save to jQuery object

    /* {#$chart.data('chart', chart);#} 

  // };
    // let valve_flow_results = {{ valve_flow_results|safe }};
    // const $valve_flow_chart = $('#chart-valve-dark');
    // function init_valve_flow($valve_flow_chart) {
    //     const chart_share = new Chart($valve_flow_chart, {
    //         type: 'line',
    //         data:  {
    //             labels: times,
    //             datasets: [
    //                 {% for valve in list_of_flow_meter_results %}
    //                 {
    //                     label: 'valve ID. {{ valve.id }}',
    //                     data: {{ valve|safe }},
    //                 },{% endfor %}
    //             ]
    //         },
    //         options: {
    //         scales: {
    //             yAxes: [{
    //                 ticks: {
    //                 callback:(value)=>value,
    //                 max: Math.max(...valve_flow_results),
    //                 min: Math.min(...valve_flow_results),
    //                 stepSize: 1
    //             }
    //         }]
    //     }
    // }
    //     });

    // Save to jQuery object

    // {#$chart.data('chart', chart);#}

  // };

    // let energy_level_results = {{ energy_level_results|safe }};
    // const $energy_level_chart = $('#chart-energy-level-dark');
    // function init_energy_level($energy_level_chart) {
    //     const chart_share = new Chart($energy_level_chart, {
    //         type: 'line',
    //         data:  {
    //             labels: times,
    //             datasets: [
    //                 {% for waterpump in list_of_energy_level_results %}
    //                 {
    //                     label: 'Water Pump ID. {{ waterpump.id }}',
    //                     data: {{ waterpump|safe }},
    //                     borderColor: [
    //                         'rgba(75, 192, 192,1)',
    //                         'rgba(175, 105, 192,1)',
    //                         'rgba(60, 200, 102,1)',
    //                     ]
    //                 },
    //                 {% endfor %}
    //                 ]
    //         },
    //         options: {
    //         scales: {
    //             yAxes: [{
    //                 ticks: {
    //                 callback:(value)=>value,
    //                 max: Math.max(...energy_level_results),
    //                 min: Math.min(...energy_level_results),
    //                 stepSize: 1
    //             }
    //         }]
    //     }
    // }
    //     });

    // Save to jQuery object

    // {#$chart.data('chart', chart);#}

  // };
*/