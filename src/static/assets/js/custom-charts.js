// SG Design system data vis palette
// https://designsystem.gov.scot/guidance/charts/data-visualisation-colour-palettes#:~:text=Categorical%20data%20palette,within%20our%20organisation.
const dsDatavisDarkBlue = '#002d54';
const dsDatavisTeal = '#2b9c93';
const dsDatavisPurple = '#6a2063';
const dsDatavisOrange = '#e5682a';
const dsDatavisDarkGreen = '#0b4c0b';
const dsDatavisGreen = '#5d9f3c';
const dsDatavisBrown = '#592c20';
const dsDatavisPink = '#ca72a2';

const dsBackgroundColours = [
    dsDatavisDarkBlue,
    dsDatavisTeal,
    dsDatavisPurple,
    dsDatavisOrange,
    dsDatavisDarkGreen,
    dsDatavisGreen,
    dsDatavisBrown,
    dsDatavisPink
];


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

// Function to get labels and counts for a chart from the selected properties
function getLabelsAndCounts(data, labelProperty, countProperty) {
    const labels = data.map((item) => item[labelProperty]);
    const counts = data.map((item) => item[countProperty]);

    return [labels, counts];
}

// Function to decide if to pluralise a label or not
function getPluralisedLabel(value, labelText) {
    return value == 1 ? labelText : `${labelText}s`;
}

function createPrisonersByCrimeTypeChart(data) {
    // Extract labels and data
    const [labels, counts] = getLabelsAndCounts(data, 'crime', 'count');

    // Create the chart
    const ctx = document
        .getElementById('prisoners-by-crime-type-chart')
        .getContext('2d');
    const prisonersByCrimeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Occurrence of crime (count)',
                    data: counts,
                    backgroundColor: dsDatavisDarkBlue,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Occurrences of crime'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Crime Type'
                    }
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.formattedValue} ${getPluralisedLabel(context.raw, 'occurrence')}`;
                        },
                    },
                },
            },
        },
    });
}

function createAverageSentenceLengthChart(data) {
    // Extract labels and data
    const [labels, counts] = getLabelsAndCounts(
        data,
        'crime',
        'average_sentence_years'
    );

    // Create the chart
    const ctx = document
        .getElementById('average-sentence-length-chart')
        .getContext('2d');
    const averageSentenceLengthChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Average Sentence Length (years)',
                    data: counts,
                    backgroundColor: dsDatavisDarkBlue,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Sentence length (years)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Crime Type'
                    }
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            const value = context.raw;
                            return formatYearsAndMonths(value);
                        },
                    },
                },
            },
        },
    });
}

function createGenderDistributionChart(data) {
    // Extract labels and data
    const [labels, counts] = getLabelsAndCounts(data, 'gender', 'count');

    // Create the chart
    const ctx = document
        .getElementById('gender-distribution-chart')
        .getContext('2d');
    const genderDistributionChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Prisoner gender (count)',
                    data: counts,
                    backgroundColor: [dsDatavisDarkBlue, dsDatavisTeal],
                },
            ],
        },
        options: {
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {                            
                            return `${context.formattedValue} ${getPluralisedLabel(context.raw, 'prisoner')}`;
                        },
                    },
                },
                datalabels: {
                    display: true,
                    color: '#ffffff',
                    formatter: function (value, context) {
                        const gender = context.chart.data.labels[context.dataIndex];
                        return `${gender}: ${value} ${getPluralisedLabel(value, 'prisoner')}`
                    }
                }
            },
        },
    });
}

function createGenderDistributionByCrimeTypeChart(data) {
    const labels = Object.keys(data);

    // Extract unique set of genders
    const genders = new Set();
    for (const crime in data) {
        for (const gender in data[crime]) {
            genders.add(gender);
        }
    }

    // Convert genders set to array
    const gendersArray = Array.from(genders);

    // Prepare data arrays for each gender
    const datasets = gendersArray.map((gender, index) => {
        return {
            label: gender,
            data: Object.keys(data).map(crime => data[crime][gender] || 0),
            backgroundColor: index < dsBackgroundColours.length - 1 ? dsBackgroundColours[index] : dsBackgroundColours[0]
        };
    });

    // Create the chart
    const ctx = document
        .getElementById('gender-distribution-by-crime-type-chart')
        .getContext('2d');
    const genderDistributionByCrimeTypeChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Prisoners (count)'
                    },
                    stacked: true
                },
                x: {
                    title: {
                        display: true,
                        text: 'Crime Type'
                    },
                    stacked: true
                },
            },
            plugins: {
                legend: { display: true },
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.formattedValue} ${getPluralisedLabel(context.raw, 'prisoner')}`;
                        },
                    },
                },
            },
        },
    });
}

function createPrisonersByPrisonChart(data) {
    // Extract labels and data
    const [labels, counts] = getLabelsAndCounts(data, 'prison', 'count');

    // Create the chart
    const ctx = document
        .getElementById('prisoners-by-prison-chart')
        .getContext('2d');
    const prisonersByPrison = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Prisoners (count)',
                    data: counts,
                    backgroundColor: dsDatavisDarkBlue,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Prisoners (count)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Prison'
                    }
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.formattedValue} ${getPluralisedLabel(context.raw, 'prisoner')}`;
                        },
                    },
                },
            },
        },
    });
}

function createAgeDistributionChart(data) {
    // Extract labels and data
    const [labels, counts] = getLabelsAndCounts(data, 'age', 'count');

    // Create the chart
    const ctx = document
        .getElementById('age-distribution-chart')
        .getContext('2d');
    const ageDistribution = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Prisoners (count)',
                    data: counts,
                    backgroundColor: dsDatavisDarkBlue,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Prisoners (count)'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Age band'
                    }
                },
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function (context) {
                            return `${context.formattedValue} ${getPluralisedLabel(context.raw, 'prisoner')}`;
                        },
                    },
                },
            },
        },
    });
}
