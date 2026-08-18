// Chart.js Visual Analytics Engine for SkillPassport

document.addEventListener('DOMContentLoaded', () => {
  const skillChartCanvas = document.getElementById('skillDistributionChart');
  const evidenceCategoryCanvas = document.getElementById('evidenceCategoryChart');

  if (skillChartCanvas) {
    fetch('/analytics/api/data/')
      .then(res => res.json())
      .then(data => {
        // 1. Skill Radar / Bar Chart
        new Chart(skillChartCanvas, {
          type: 'bar',
          data: {
            labels: data.skills.labels,
            datasets: [{
              label: 'Verified Skill Score (%)',
              data: data.skills.data,
              backgroundColor: 'rgba(79, 70, 229, 0.75)',
              borderColor: '#4f46e5',
              borderWidth: 1.5,
              borderRadius: 6
            }]
          },
          options: {
            responsive: true,
            scales: {
              y: { beginAtZero: true, max: 100 }
            },
            plugins: {
              legend: { display: false }
            }
          }
        });

        // 2. Evidence Category Doughnut Chart
        if (evidenceCategoryCanvas) {
          new Chart(evidenceCategoryCanvas, {
            type: 'doughnut',
            data: {
              labels: data.evidence_categories.labels,
              datasets: [{
                data: data.evidence_categories.data,
                backgroundColor: [
                  '#4f46e5',
                  '#06b6d4',
                  '#10b981',
                  '#8b5cf6',
                  '#f59e0b',
                  '#ef4444'
                ]
              }]
            },
            options: {
              responsive: true,
              plugins: {
                legend: { position: 'bottom' }
              }
            }
          });
        }
      })
      .catch(err => console.log('Analytics Chart error:', err));
  }
});
