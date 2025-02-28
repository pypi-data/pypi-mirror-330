console.log("hello world");

document.addEventListener('DOMContentLoaded', function () {
    // Function to update the connections table using the fetched data.
    function updateConnectionsTable(connections) {
        const tbody = document.getElementById('connections-tbody');
        if (!tbody) return;
        // Clear existing rows
        tbody.innerHTML = '';

        // If no connections exist, show a fallback row
        if (Object.keys(connections).length === 0) {
            tbody.innerHTML = '<tr><td colspan="2">No connections available.</td></tr>';
            return;
        }

        // Create and append a new row for each connection
        Object.entries(connections).forEach(([sid, connection]) => {
            const row = document.createElement('tr');

            const nameCell = document.createElement('td');
            nameCell.textContent = connection.name || "N/A";
            row.appendChild(nameCell);

            const sidCell = document.createElement('td');
            sidCell.textContent = connection.sid;
            row.appendChild(sidCell);

            tbody.appendChild(row);
        });
    }

    // Function to fetch connections from the API
    function fetchConnections() {
        fetch('/api/connections')
            .then(response => response.json())
            .then(data => {
                updateConnectionsTable(data);
            })
            .catch(error => console.error('Error fetching connections:', error));
    }

    // Initial fetch
    fetchConnections();

    // Update the connections table every 3 seconds
    setInterval(fetchConnections, 3000);
});