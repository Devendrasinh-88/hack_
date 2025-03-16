function initializeCharts(data) {
    // Project Types Chart
    new Chart(document.getElementById('projectTypesChart'), {
        type: 'pie',
        data: {
            labels: Object.keys(data.project_types),
            datasets: [{
                data: Object.values(data.project_types),
                backgroundColor: [
                    '#ff6384',
                    '#36a2eb',
                    '#ffce56',
                    '#4bc0c0',
                    '#9966ff'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Status Distribution Chart
    new Chart(document.getElementById('statusChart'), {
        type: 'doughnut',
        data: {
            labels: Object.keys(data.status_distribution),
            datasets: [{
                data: Object.values(data.status_distribution),
                backgroundColor: [
                    '#28a745',
                    '#ffc107',
                    '#dc3545',
                    '#6c757d'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Monthly Costs Chart
    new Chart(document.getElementById('costChart'), {
        type: 'bar',
        data: {
            labels: Object.keys(data.monthly_costs),
            datasets: [{
                label: 'Project Costs (INR)',
                data: Object.values(data.monthly_costs),
                backgroundColor: '#36a2eb'
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₹' + value.toLocaleString();
                        }
                    }
                }
            }
        }
    });
}
