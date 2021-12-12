// Convert data into correct format for HighCharts JS
function readyData(data) {
    var ohlc = [],
        dataLength = data.length, // including header
        i = 0,
        dateTime,
        parts,
        epochTime;

    for (i; i < dataLength - 1; i += 1) {
        // Convert datetime string to epoch time for HighCharts JS
        dateTime = $.trim(data[i]['Date']) + ' ' + $.trim(data[i]['Time']);
        parts = dateTime.match(/(\d{1,2})\/(\d{1,2})\/(\d{4}) (\d{1,2}):(\d{2}):(\d{2})/);
        parts = parts.map(function(dateStr) {
            return parseInt(dateStr, 10);
        });
        epochTime = Date.UTC(parts[3], parts[1] - 1, parts[2], parts[4], parts[5], parts[6]);

        ohlc.push([
            epochTime,
            parseInt(data[i]['Open'], 10), // open
            parseInt(data[i]['High'], 10), // high
            parseInt(data[i]['Low'], 10), // low
            parseInt(data[i]['Close'], 10) // close
        ]);
    }
    console.log(ohlc);
    return ohlc;
}

var fileName = $("#filename").text();

// Plot data into candlesticks graph
function graphCandlestick(data) {
    Highcharts.stockChart('chart-container', {
        rangeSelector: {
            allButtonsEnabled: true,
            buttons: [{
                type: 'minute',
                count: 10,
                text: '10m'
            }, {
                type: 'hour',
                count: 1,
                text: '1hr'
            }, {
                type: 'hour',
                count: 6,
                text: '6hr'
            }, {
                type: 'day',
                count: 1,
                text: '1d'
            }, {
                type: 'all',
                text: 'All'
            }],
            selected: 1 // On load, initially at 1 hour
        },
        title: {
            text: 'Candlestick Graph Analysis'
        },
        series: [{
            type: 'candlestick',
            name: fileName,
            data: data
        }]
    });
}
