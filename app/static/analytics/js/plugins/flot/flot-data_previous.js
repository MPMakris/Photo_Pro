
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;
    plot_image_views(ivq_proba);
    plot_user_views(uvq_proba);
    plot_user_is_pro(uip_proba_0, uip_proba_1);

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
      var plotObj = $.plot($("#flot-bar-chart-user-results"), [barData], barOptions);
    };

    // User is Pro Bar Chart:
    function plot_user_is_pro(uip_proba_0, uip_proba_1) {

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
              // min: -0.25,
              // max: 3.75,
              tickDecimals: 0,
          },
          yaxis: {
              show: true,
              mode: null,
              // min: 0,
              // max: 1,
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
      var barData = [{
        label: "Non-Pro Likelihood",
        data: uip_proba_0,
        color: "rgb(51, 51, 255)"
      }, {
        label: "Pro Likelihood",
        data: uip_proba_1,
        color: "rgb(204, 0, 102)"
      }];
      var plotObj = $.plot($("#flot-bar-chart-user-is-pro"), barData, barOptions);
    };
});
