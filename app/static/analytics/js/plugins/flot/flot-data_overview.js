
//Image Views Per Image
$(document).ready(function() {
    console.log("document ready");
    var offset = 0;
    // var test_data;
    // $.get('url return file', function(response) {
    //     test_data = response;
    // });
    // console.log(test_data);
    plot(image_views, user_total_views, user_is_pro);

    function plot(image_views) {

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
    }
});

//Image Views Per User
$(function plot(user_total_views) {

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
});

// Flot Pie Chart with Tooltips
$(function(user_is_pro) {

    var plotObj = $.plot($("#flot-pie-chart"), user_is_pro, {
        series: {
            pie: {
                show: true
            }
        },
        grid: {
            hoverable: true
        },
        tooltip: true,
        tooltipOpts: {
            content: "%p.0%, %s", // show percentages, rounding to 2 decimal places
            shifts: {
                x: 20,
                y: 0
            },
            defaultTheme: false
        }
    });

});

// Flot Chart Dynamic Chart

$(function() {

    var container = $("#flot-moving-line-chart");

    // Determine how many data points to keep based on the placeholder's initial size;
    // this gives us a nice high-res plot while avoiding more than one point per pixel.

    var maximum = container.outerWidth() / 2 || 300;

    //

    var data = [];

    function getRandomData() {

        if (data.length) {
            data = data.slice(1);
        }

        while (data.length < maximum) {
            var previous = data.length ? data[data.length - 1] : 50;
            var y = previous + Math.random() * 10 - 5;
            data.push(y < 0 ? 0 : y > 100 ? 100 : y);
        }

        // zip the generated y values with the x values

        var res = [];
        for (var i = 0; i < data.length; ++i) {
            res.push([i, data[i]])
        }

        return res;
    }

    //

    series = [{
        data: getRandomData(),
        lines: {
            fill: true
        }
    }];

    //

    var plot = $.plot(container, series, {
        grid: {
            borderWidth: 1,
            minBorderMargin: 20,
            labelMargin: 10,
            backgroundColor: {
                colors: ["#fff", "#e4f4f4"]
            },
            margin: {
                top: 8,
                bottom: 20,
                left: 20
            },
            markings: function(axes) {
                var markings = [];
                var xaxis = axes.xaxis;
                for (var x = Math.floor(xaxis.min); x < xaxis.max; x += xaxis.tickSize * 2) {
                    markings.push({
                        xaxis: {
                            from: x,
                            to: x + xaxis.tickSize
                        },
                        color: "rgba(232, 232, 255, 0.2)"
                    });
                }
                return markings;
            }
        },
        xaxis: {
            tickFormatter: function() {
                return "";
            }
        },
        yaxis: {
            min: 0,
            max: 110
        },
        legend: {
            show: true
        }
    });

    // Update the random dataset at 25FPS for a smoothly-animating chart

    setInterval(function updateRandom() {
        series[0].data = getRandomData();
        plot.setData(series);
        plot.draw();
    }, 40);

});

// Flot Chart Bar Graph

$(function() {

    var barOptions = {
        series: {
            bars: {
                show: true,
                barWidth: 43200000
            }
        },
        xaxis: {
            mode: "time",
            timeformat: "%m/%d",
            minTickSize: [1, "day"]
        },
        grid: {
            hoverable: true
        },
        legend: {
            show: false
        },
        tooltip: true,
        tooltipOpts: {
            content: "x: %x, y: %y"
        }
    };
    var barData = {
        label: "bar",
        data: [
            [1354521600000, 1000],
            [1355040000000, 2000],
            [1355223600000, 3000],
            [1355306400000, 4000],
            [1355487300000, 5000],
            [1355571900000, 6000]
        ]
    };
    $.plot($("#flot-bar-chart-image-results-1"), [barData], barOptions);

});
