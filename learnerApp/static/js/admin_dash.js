// admin_dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    // Example Data - replace with dynamic data from Django context or API
    const enrollmentData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'Enrollments',
            data: [30, 40, 50, 60, 70, 80, 90],
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1
        }]
    };

    const revenueData = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'Revenue',
            data: [500, 700, 800, 900, 1100, 1200, 1300],
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1
        }]
    };

    // Enrollment Chart
    const ctxEnrollment = document.getElementById('enrollmentChart').getContext('2d');
    new Chart(ctxEnrollment, {
        type: 'line',
        data: enrollmentData,
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Revenue Chart
    const ctxRevenue = document.getElementById('revenueChart').getContext('2d');
    new Chart(ctxRevenue, {
        type: 'bar',
        data: revenueData,
        options: {
            responsive: true,
            scales: {
                x: {
                    beginAtZero: true
                },
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
