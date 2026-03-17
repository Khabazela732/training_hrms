document.addEventListener("DOMContentLoaded", function () {

    /* ===================== SALARY CHART ===================== */

    const salaryCanvas = document.getElementById('salaryChart');

    if (salaryCanvas) {

        new Chart(salaryCanvas.getContext('2d'), {
            type: 'bar',
            data: {
                labels: ['IT', 'HR', 'Finance', 'Marketing'],
                datasets: [{
                    label: 'Number of Employees',
                    data: [12, 8, 10, 6],
                    backgroundColor: [
                        'rgba(75,192,192,0.7)',
                        'rgba(255,159,64,0.7)',
                        'rgba(153,102,255,0.7)',
                        'rgba(255,205,86,0.7)'
                    ],
                    borderColor: [
                        'rgba(75,192,192,1)',
                        'rgba(255,159,64,1)',
                        'rgba(153,102,255,1)',
                        'rgba(255,205,86,1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true } }
            }
        });

    }


    /* ===================== TRAINING PIE ===================== */

    const revenueCanvas = document.getElementById('revenueChart');

    if (revenueCanvas) {

        new Chart(revenueCanvas.getContext('2d'), {
            type: 'pie',
            data: {
                labels: ['Completed', 'In Progress', 'Pending'],
                datasets: [{
                    label: 'Training Status',
                    data: [5, 3, 2],
                    backgroundColor: [
                        'rgba(54,162,235,0.7)',
                        'rgba(255,205,86,0.7)',
                        'rgba(255,99,132,0.7)'
                    ],
                    borderColor: [
                        'rgba(54,162,235,1)',
                        'rgba(255,205,86,1)',
                        'rgba(255,99,132,1)'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                plugins: { legend: { position: 'bottom' } }
            }
        });

    }


    /* ===================== DEPARTMENT PERFORMANCE ===================== */

    const perfCanvas = document.getElementById("performanceDeptChart");

    if (perfCanvas) {

        const labels = JSON.parse(perfCanvas.dataset.labels);
        const ratings = JSON.parse(perfCanvas.dataset.ratings);

        const colors = labels.map(() =>
            `hsl(${Math.random() * 360},70%,60%)`
        );

        new Chart(perfCanvas.getContext("2d"), {
            type: "bar",
            data: {
                labels: labels,
                datasets: [{
                    label: "Average Rating",
                    data: ratings,
                    backgroundColor: colors,
                    borderColor: colors,
                    borderWidth: 1
                }]
            },
            options: {
                indexAxis: 'y',
                responsive: true,
                plugins: { legend: { display: true } },
                scales: {
                    x: {
                        beginAtZero: true,
                        max: Math.max(...ratings) + 1
                    }
                }
            }
        });

    }

});
// Payroll Statistics Chart
const payrollCanvas = document.getElementById("payrollChart");

if (payrollCanvas) {

    const months = JSON.parse(payrollCanvas.dataset.months);
    const amounts = JSON.parse(payrollCanvas.dataset.amounts);

    new Chart(payrollCanvas.getContext("2d"), {
        type: "bar",
        data: {
            labels: months,
            datasets: [{
                label: "Monthly Payroll",
                data: amounts,
                backgroundColor: "rgba(59,130,246,0.6)",
                borderColor: "rgb(59,130,246)",
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { position: "top" }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

}
//Daily Attendance Chart//

const balanceCtx = document.getElementById('balanceChart').getContext('2d');

const balanceChart = new Chart(balanceCtx, {
    type: 'bar',

    data: {
        labels: ['Present', 'Absent', 'Late'],

        datasets: [{
            label: 'Today\'s Attendance',

            data: [
                presentToday,
                absentToday,
                lateToday
            ],

            backgroundColor: [
                'rgba(34,197,94,0.6)',
                'rgba(239,68,68,0.6)',
                'rgba(245,158,11,0.6)'
            ],

            borderColor: [
                'rgb(34,197,94)',
                'rgb(239,68,68)',
                'rgb(245,158,11)'
            ],

            borderWidth: 2
        }]
    },

    options: {
        responsive: true,

        plugins: {
            legend: {
                display: true,
                position: 'top'
            }
        },

        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});