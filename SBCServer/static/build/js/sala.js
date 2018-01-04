var config = {
    type: 'doughnut',
    data: {
        labels:["Asistentes", "Aforo restante"],
        datasets: [
            {
                data: [300, 100],
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
        legend: {
            display:true,
            position: 'bottom'
        },
    }
};

var config2 = {
    type: 'line',
    data: {
        labels: ["00:00", "02:00", "10:00", "12:00", "14:00", "18:00", "22:00"],
        datasets: [{
            label: "Entradas",
            backgroundColor: "rgba(38, 185, 154, 0.31)",
            borderColor: "rgba(38, 185, 154, 0.7)",
            pointBorderColor: "rgba(38, 185, 154, 0.7)",
            pointBackgroundColor: "rgba(38, 185, 154, 0.7)",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(220,220,220,1)",
            pointBorderWidth: 1,
            data: [125, 81, 70, 112, 124, 170, 30]
        }, {
            label: "Salidas",
            backgroundColor: "rgba(3, 88, 106, 0.3)",
            borderColor: "rgba(3, 88, 106, 0.70)",
            pointBorderColor: "rgba(3, 88, 106, 0.70)",
            pointBackgroundColor: "rgba(3, 88, 106, 0.70)",
            pointHoverBackgroundColor: "#fff",
            pointHoverBorderColor: "rgba(151,187,205,1)",
            pointBorderWidth: 1,
            data: [81, 125, 158, 112, 70, 36, 84],
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
    $('#datatable').dataTable();
};
