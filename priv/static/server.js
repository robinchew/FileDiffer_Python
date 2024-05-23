document.addEventListener("DOMContentLoaded", function() {
    // Fetch the JSON data from the Flask server
    fetch('/raw')
    .then(response => response.json())
    .then(data => {
        const resultContainer = document.getElementById("result");

        // Clear the container
        resultContainer.innerHTML = "";

        // Process each file's details
        Object.entries(data.changes).forEach(([_, change]) => {
            // Create a table for each file
            const table = document.createElement('table');
            const headerRow = table.insertRow();
            const headerCell = headerRow.insertCell();
            headerCell.colSpan = "4";
            headerCell.innerHTML = change.file_path;
            
            // Add file content to the table
            change.hunks.forEach(fileDetail => {
                fileDetail.lines.forEach(lineDetail => {
                    const row = table.insertRow();
    
                    if (lineDetail.type === "+") {
                        row.className = 'green-highlight'; // Use a class to style the row
                    } else if (lineDetail.type === "-") {
                        row.className = 'pink-highlight'; // Use a class to style the row
                    }
    
                    const cellOldLine = row.insertCell();
                    cellOldLine.textContent = lineDetail.old_lineno;
    
                    const cellNewLine = row.insertCell();
                    cellNewLine.textContent = lineDetail.new_lineno;
    
                    const cellChange = row.insertCell();
                    cellChange.textContent = lineDetail.type;
    
                    const cellValue = row.insertCell();
                    cellValue.textContent = lineDetail.content;
                })
            });

            // Append the table to the result container
            resultContainer.appendChild(table);
            resultContainer.appendChild(document.createElement('br')); // Add a spacer after each table
        });
    })
    .catch(error => console.error('Error fetching data:', error));
});
