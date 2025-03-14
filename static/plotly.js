// async function loadChart() {
//     const response = await fetch('/api/statistiques');  // Utilise la nouvelle API
//     const data = await response.json();
    
//     const ctx = document.getElementById('venteChart').getContext('2d');
//     new Chart(ctx, {
//         type: 'bar',
//         data: {
//             labels: data.labels,
//             datasets: [{
//                 label: 'Produits vendus',
//                 data: data.data,
//                 backgroundColor: 'rgba(75, 192, 192, 0.2)',
//                 borderColor: 'rgba(75, 192, 192, 1)',
//                 borderWidth: 1
//             }]
//         },
//         options: {
//             responsive: true,
//             scales: {
//                 y: {
//                     beginAtZero: true
//                 }
//             }
//         }
//     });
// }
// loadChart()