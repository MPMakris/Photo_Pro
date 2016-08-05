
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;
    plot(ivq_proba);

    function plot(ivq_proba, uvq_proba) {

      var barOptions = {
          series: {
              bars: {
                  show: true,
                  barWidth: 432
              }
          },
          xaxis: {
              show: true,
              mode: null
          },
          grid: {
              hoverable: false
          },
          legend: {
              show: false
          }
          //tooltip: false
      };
      var barData = {
          label: "bar",
          data: ivq_proba
      };
      var plotObj = $.plot($("#flot-bar-chart-image-results-1"), [barData], barOptions);
    }
});

 //User Total Views
$(function plot(uvq_proba) {

  var barOptions = {
      series: {
          bars: {
              show: true,
              barWidth: 10
          }
      },
      xaxis: {
          show: true,
          mode: null,
          min: 0,
          max: 10,
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
      label: "bar",
      data: uvq_proba
  };
  var plotObj = $.plot($("#flot-bar-chart-user-results-1"), [barData], barOptions);
});
