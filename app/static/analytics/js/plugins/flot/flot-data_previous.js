
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;
    plot_image_views(ivq_proba);
    plot_user_views(uvq_proba);

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
              min: 0,
              max: 10,
              tickDecimals: 0
          },
          yaxis: {
              show: true,
              mode: null,
              min: 0,
              max: 1,
              tickDecimals: 3
          },
          grid: {
              hoverable: true,
              autoHighlight: true
          },
          legend: {
              show: true
          }
          //tooltip: false
      };
      var barData = {
          label: "Probabilities",
          data: ivq_proba
      };
      var plotObj = $.plot($("#flot-bar-chart-image-results-1"), [barData], barOptions);
    }

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
              min: 0,
              max: 10,
              tickDecimals: 3
          },
          yaxis: {
              show: true,
              mode: null,
              min: 0,
              max: 1,
              tickDecimals: 0
          },
          grid: {
              hoverable: true,
              autoHighlight: true
          },
          legend: {
              show: true
          }
          //tooltip: false
      };
      var barData = {
          label: "Probabilities",
          data: uvq_proba
      };
      var plotObj = $.plot($("#flot-bar-chart-user-results-1"), [barData], barOptions);
    }
});
