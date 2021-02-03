var json_data = JSON.parse($('#json_data').val());
Highcharts.chart('container', {

    chart: {
        type: 'line'
    },
    title: {
        text: 'Аналитика заказов интернет-магазина'
    },

    xAxis: {
        categories: json_data[0],
        title: {
            text: 'Дата'
        }
    },
    yAxis: {
        title: {
            text: 'Количество заказов в день'
        }
    },
    plotOptions: {
        line: {
            dataLabels: {
                enabled: true
            },
            enableMouseTracking: true
        }
    },
    series: [{
        name: 'Аналитика заказов интернет-магазина',
        data: json_data[1]
    }]
});