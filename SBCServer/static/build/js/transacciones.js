
var incremento = $('#my-data').data()["incremento"];
var pagosHoy = $('#my-data').data()["pagoshoy"];
var pagosAyer = $('#my-data').data()["pagosayer"];

if(pagosHoy>pagosAyer){
    pagosHoy = 100;
    pagosAyer = 0;
}else if(pagosAyer == 0){
    pagosHoy = 0;
    pagosAyer = 100;
}
var cargas = JSON.parse($('#my-data').data()["cargas"].replace("(","[").replace(")","]").replace(/'/g,'"').replace(/(,]$)/g,"]"));
var pagos = JSON.parse($('#my-data').data()["pagos"].replace("(","[").replace(")","]").replace(/'/g,'"').replace(/(,]$)/g,"]"));

var data_cargas = [{x: 0, y: 0},{x: 1, y: 0},{x: 2, y: 0},{x: 3, y: 0},{x: 4, y: 0},{x: 5, y: 0},{x: 6, y: 0},{x: 7, y: 0},
    {x: 8, y: 0},{x: 9, y: 0},{x: 10, y: 0},{x: 11, y: 0},{x: 12, y: 0},{x: 13, y: 0},{x: 14, y: 0},{x: 15, y: 0},{x: 16, y: 0},
    {x: 17, y: 0},{x: 18, y: 0},{x: 19, y: 0},{x: 20, y: 0},{x: 21, y: 0},{x: 22, y: 0},{x: 23, y: 0}]

for (var i in cargas){
    carga = cargas[i];
    if (carga.Hora !== ""){
        data_cargas[carga.Hora].y = carga.Cargas;
    }
}

var data_pagos = [{x: 0, y: 0},{x: 1, y: 0},{x: 2, y: 0},{x: 3, y: 0},{x: 4, y: 0},{x: 5, y: 0},{x: 6, y: 0},{x: 7, y: 0},
    {x: 8, y: 0},{x: 9, y: 0},{x: 10, y: 0},{x: 11, y: 0},{x: 12, y: 0},{x: 13, y: 0},{x: 14, y: 0},{x: 15, y: 0},{x: 16, y: 0},
    {x: 17, y: 0},{x: 18, y: 0},{x: 19, y: 0},{x: 20, y: 0},{x: 21, y: 0},{x: 22, y: 0},{x: 23, y: 0}]

for (var i in pagos){
    pago = pagos[i];
    if (pago.Hora !== ""){
        data_pagos[pago.Hora].y = pago.Pagos;
    }
}

var config = {
    type: 'doughnut',
    data: {
        labels:["Incremento en ventas"],
        datasets: [
            {
                data: [pagosHoy, pagosAyer],
                backgroundColor: [
                    "#46bb9b",
                    "#bec4c8"
                ],
                hoverBackgroundColor: [
                    "#46bb9b",
                    "#bec4c8"
                ]
            }]
    },
    options: {
    	rotation: 1 * Math.PI,
        circumference: 1 * Math.PI,
        responsive: true,
        tooltips: false,
        legend: {
            display:true,
            position: 'bottom'
        },
    }
};

var config2 = {
    type: 'line',
    data: {
        labels: ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00","12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00",],
        datasets: [{
            label: "Cargas",
            backgroundColor: "rgba(38, 185, 154, 0.31)",
            borderColor: "rgba(38, 185, 154, 0.7)",
            pointBorderColor: "rgba(38, 185, 154, 0.7)",
            pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointBorderWidth: 1,
            data: data_cargas
        }, {
            label: "Pagos",
            backgroundColor: "rgba(3, 88, 106, 0.3)",
            borderColor: "rgba(3, 88, 106, 0.70)",
            pointBorderColor: "rgba(3, 88, 106, 0.70)",
            pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(151,187,205,1)",
            pointBorderWidth: 1,
            data: data_pagos
        }]
    },
    options: {
        responsive: true,
        legend: {
            display:true,
            position: 'bottom'
        },
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        hover: {
            mode: 'nearest',
            intersect: true
        },
        scales: {
            xAxes: [{
                display: true
            }],
            yAxes: [{
                display: true
            }]
        }
    }
};


window.onload = function() {
    var ctx = document.getElementById("canvas").getContext("2d");
    var ctx2 = document.getElementById("canvas2").getContext("2d");
    window.aforo = new Chart(ctx, config)
    window.accesos = new Chart(ctx2, config2);
    $('#datatable').dataTable({"fnRowCallback": function( nRow, aData, iDisplayIndex, iDisplayIndexFull ) {
        if ( aData[4] < 0 )
        {
            $('td', nRow).css('background-color', '#ffc1bf');
        }
        else
        {
            $('td', nRow).css('background-color', '#d3ffbf');
        }
    }});
};
