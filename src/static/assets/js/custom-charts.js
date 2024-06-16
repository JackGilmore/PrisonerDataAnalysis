// Function to fetch data from the API endpoint
async function fetchData() {
    try {
        const response = await fetch('/api/analysis');
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
        return [];
    }
}

// Function to format a numerical year value into a string of years and months
function formatYearsAndMonths(value) {
    const years = Math.floor(value);
    const months = Math.round((value % 1) * 12);
    return `${years} years and ${months} months`;
}

async function createPrisonersByCrimeTypeChart(data) {

    // Extract labels and data from the JSON
    const labels = data.map(item => item.crime);
    const counts = data.map(item => item.count);

    // Create the chart
    const ctx = document.getElementById('prisoners-by-crime-type-chart').getContext('2d');
    const crimeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Occurrence of crime (count)',
                data: counts,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function createAverageSentenceLengthChart(data) {
    // Extract labels and data
    const labels = data.map(item => item.crime);
    const counts = data.map(item => item.average_sentence_years);

    // Create the chart
    const ctx = document.getElementById('average-sentence-length-chart').getContext('2d');
    const crimeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Average Sentence Length (years)',
                data: counts,
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.raw;
                            return formatYearsAndMonths(value);
                        }
                    }
                }
            }
        },
    });
}