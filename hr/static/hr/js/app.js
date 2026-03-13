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