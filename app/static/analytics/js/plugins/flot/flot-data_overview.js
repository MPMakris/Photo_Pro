
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;

    plot_image_views_hist(image_views);
    // plot_user_pro_pie(user_is_pro);
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
                max: 300,
                axisLabel: "Views",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif"
            },
            yaxis: {
                show: true,
                min: 0,
                max: 2000,
                axisLabel: "Images",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif"
            },
            tooltip: false
        };

        var plotObj = $.plot($("#flot-line-chart-all-image-views"), [{
                data: image_views,
                label: "Photos",
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
                axisLabel: "Users",
                axisLabelUseCanvas: true,
                axisLabelFontSizePixels: 20,
                axisLabelFontFamily: "sans-serif"
            },
            tooltip: false
        };

        var plotObj = $.plot($("#flot-line-chart-all-categories-user-views"), [{
                data: user_total_views,
                label: "Photos",
                color: "rgb(204, 0, 102)"
            }],
            options);
    };

    // Flot Pie Chart with Tooltips
    // function plot_user_pro_pie(user_is_pro) {
    //
    //     var plotObj = $.plot($("#flot-pie-chart_user_pro"), user_is_pro, {
    //         series: {
    //             pie: {
    //                 show: true
    //             }
    //         },
    //         grid: {
    //             hoverable: true
    //         },
    //         tooltip: true,
    //         tooltipOpts: {
    //             content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
    //             shifts: {
    //                 x: 20,
    //                 y: 0
    //             },
    //             defaultTheme: false
    //         }
    //     });
    //
    // }
});
