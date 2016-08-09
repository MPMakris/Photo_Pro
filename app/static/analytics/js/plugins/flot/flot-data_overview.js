
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;

    plot_image_views_hist(image_views);
    plot_user_pro_bar();
    plot_user_views_hist(user_total_views);

    function plot_image_views_hist(image_views) {

        var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: false
                }
            },
            grid: {
                hoverable: false //IMPORTANT! this is needed for tooltip to work
            },
            xaxis: {
                show: true,
                min: 0,
                max: 400,
                axisLabel: "Views",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif",
                // transform: function (v) { return Math.log(v); },
                // inverseTransform: function (v) { return Math.exp(v); }
            },
            yaxis: {
                show: true,
                min: 0,
                max: 2200,
                axisLabel: "# Images",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif"
            },
            tooltip: false
        };

        var plotObj = $.plot($("#flot-line-chart-all-image-views"), [{
                data: image_views,
                label: "Images",
                color: "rgb(204, 0, 102)"
            }],
            options);
    };
    // Flot Chart for User Views
    function plot_user_views_hist(user_total_views) {

        var options = {
            series: {
                lines: {
                    show: true
                },
                points: {
                    show: false
                }
            },
            grid: {
                hoverable: false //IMPORTANT! this is needed for tooltip to work
            },
            xaxis: {
                show: true,
                min: 0,
                max: 1000,
                axisLabel: "Total Views",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif"
            },
            yaxis: {
                show: true,
                min: 0,
                max: 25,
                axisLabel: "# Users",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif"
            },
            tooltip: false
        };

        var plotObj = $.plot($("#flot-line-chart-all-categories-user-views"), [{
                data: user_total_views,
                label: "Users",
                color: "rgb(204, 0, 102)"
            }],
            options);
    };

    // Flot Pie Chart with Tooltips
    function plot_user_pro_bar() {

        var barOptions = {
            series: {
                bars: {
                    show: true,
                    barWidth: 0.5
                }
            },
            xaxis: {
                mode: null,
                min: 0,
                max: 2
            },
            yaxis: {
                show: true,
                mode: null
            },
            grid: {
                hoverable: true
            },
            legend: {
                show: true
            }
        };
        var barData = {[
            label: "Non-Pro",
            data: [[0, 42]]
          ]
            // color: "rgb(204, 0, 102)"
          //
          //   label: "Non-Pro",
          //   data: [[1, 58]],
          //   color: "rgb(204, 0, 102)"
        };
        var plotObj = $.plot($("#flot-bar-chart_user_pro"), [barData],
            barOptions);
    };
});
