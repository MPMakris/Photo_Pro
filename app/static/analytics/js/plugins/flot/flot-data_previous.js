
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;
    plot(bar_numbers);

    function plot(bar_numbers) {

      var barOptions = {
          series: {
              bars: {
                  show: true,
                  barWidth: 43200000
              }
          },
          xaxis: {
              show: true
              mode: null
          },
          grid: {
              hoverable: false
          },
          legend: {
              show: false
          },
          tooltip: false
      };
      var barData = {
          label: "bar",
          data: bar_numbers
      };
      var plotObj = $.plot($("#flot-bar-chart-image-results-1"), [barData], barOptions);
    }
});
