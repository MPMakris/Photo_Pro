
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;
    plot_image_views(ivq_proba);
    plot_user_views(uvq_proba);
    plot_user_is_pro(uip_proba);

    //Image Views Graph:
    function plot_image_views(ivq_proba) {

      var barOptions = {
          series: {
              bars: {
                  show: true,
                  barWidth: 0.5
              }
          },
          xaxis: {
              show: true,
              mode: null,
              min: 0.75,
              max: 5.75,
              tickDecimals: 0,
              axisLabel: "Performance Bins, Higher Performing -->",
              axisLabelUseCanvas: true,
              axisLabelFontSizePixels: 20,
              axisLabelFontFamily: "sans-serif"
          },
          yaxis: {
              show: true,
              mode: null,
              min: 0,
              max: 1,
              tickDecimals: 3,
              axisLabel: "Likelihood (%)",
              axisLabelUseCanvas: true,
              axisLabelFontSizePixels: 20,
              axisLabelFontFamily: "sans-serif"
          },
          grid: {
              hoverable: true,
              autoHighlight: true
          },
          legend: {
              show: true
          }
      };
      var barData = {
          label: "Predicted Probabilities",
          data: ivq_proba,
          color: "rgb(204, 0, 102)"
      };
      var plotObj = $.plot($("#flot-bar-chart-image-results-1"), [barData], barOptions);
    };

    // User Views Graph:
    function plot_user_views(uvq_proba) {

      var barOptions = {
          series: {
              bars: {
                  show: true,
                  barWidth: 0.5
              }
          },
          xaxis: {
              show: true,
              mode: null,
              min: 0.75,
              max: 3.75,
              tickDecimals: 0,
              axisLabel: "Performance Bins, Higher Performing -->",
              axisLabelUseCanvas: true,
              axisLabelFontSizePixels: 20,
              axisLabelFontFamily: "sans-serif"
          },
          yaxis: {
              show: true,
              mode: null,
              min: 0,
              max: 1,
              tickDecimals: 3,
              axisLabel: "Likelihood (%)",
              axisLabelUseCanvas: true,
              axisLabelFontSizePixels: 20,
              axisLabelFontFamily: "sans-serif"
          },
          grid: {
              hoverable: true,
              autoHighlight: true
          },
          legend: {
              show: true
          }
      };
      var barData = {
          label: "Predicted Probabilities",
          data: uvq_proba,
          color: "rgb(204, 0, 102)"
      };
      var plotObj = $.plot($("#flot-bar-chart-user-results-1"), [barData], barOptions);
    };

    // User is Pro Pie Chart:
    function plot_user_is_pro(uip_proba) {

        var plotObj = $.plot($("#flot-pie-chart-user-is-pro-1"), uip_proba, {
            series: {
                pie: {
                    show: true,
                    label: {
                         show: true,
                         radius: 3/4,
                         background: {
                              opacity: 0.5,
                              color: '#000'
                         }
                    },
                    innerRadius: 0.5
                }
            },
            legend: {
                  show: true
            },
            grid: {
                hoverable: true,
                autoHighlight: true
            },
            tooltip: true,
            tooltipOpts: {
                shifts: {
                    x: 20,
                    y: 0
                },
            defaultTheme: false
            }
        });

    };
});
