const salaryCtx = document.getElementById('salaryChart').getContext('2d');
const salaryChart = new Chart(salaryCtx, {
    type: 'bar',
    data: {
        labels: ['IT', 'HR', 'Finance', 'Marketing'],
        datasets: [{
            label: 'Number of Employees',
            data: [12, 8, 10, 6, 4],
            backgroundColor: [
                'rgba(75, 192, 192, 0.7)',
                'rgba(255, 159, 64, 0.7)',
                'rgba(153, 102, 255, 0.7)',
                'rgba(255, 205, 86, 0.7)',
                'rgba(54, 162, 235, 0.7)'
            ],
            borderColor: [
                'rgba(75, 192, 192, 1)',
                'rgba(255, 159, 64, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(54, 162, 235, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: {
            y: { beginAtZero: true }
        }
    }
});

// Training Statistics - Pie Chart
const revenueCtx = document.getElementById('revenueChart').getContext('2d');
const revenueChart = new Chart(revenueCtx, {
    type: 'pie',
    data: {
        labels: ['Completed', 'In Progress', 'Pending'],
        datasets: [{
            label: 'Training Status',
            data: [5, 3, 2],
            backgroundColor: [
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 205, 86, 0.7)',
                'rgba(255, 99, 132, 0.7)'
            ],
            borderColor: [
                'rgba(54, 162, 235, 1)',
                'rgba(255, 205, 86, 1)',
                'rgba(255, 99, 132, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { position: 'bottom' } }
    }
});

// Monthly Attendance - Line Chart
const balanceCtx = document.getElementById('balanceChart').getContext('2d');
const balanceChart = new Chart(balanceCtx, {
    type: 'line',
    data: {
        labels: ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        datasets: [{
            label: 'Present Employees',
            data: [20, 22, 19, 23],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgb(13, 95, 95)',
            borderWidth: 2,
            tension: 0.3,
            fill: true,
            pointRadius: 4
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: true, position: 'top' } },
        scales: {
            y: { beginAtZero: true }
        }
    }
});
// ===================== CALENDAR =====================
document.addEventListener('DOMContentLoaded', function () {
    const calendarEl = document.getElementById('calendar');

    // Initialize FullCalendar
    const calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        selectable: true,
        editable: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        initialDate: new Date(), // show current date by default
        navLinks: true,
        businessHours: true,
        events: [], // start empty
        select: function (info) {
            const title = prompt('Enter event title:');
            if (title) {
                const type = prompt('Is this a "Meeting" or "Reminder"?', 'Meeting');
                calendar.addEvent({
                    title: title,
                    start: info.startStr,
                    end: info.endStr,
                    allDay: info.allDay,
                    classNames: type === 'Reminder' ? 'reminder' : 'meeting'
                });
            }
            calendar.unselect();
        },
        eventClick: function (info) {
            const action = confirm(`Do you want to delete the event "${info.event.title}"?`);
            if (action) {
                info.event.remove();
            }
        },
        editable: true,
        dayMaxEvents: true, // show "more" link when too many events
        themeSystem: 'standard'
    });

    calendar.render();
});