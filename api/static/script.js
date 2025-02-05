function fetchEOLInfo() {
    let softwareName = document.getElementById("softwareName").value.trim();
    let resultsDiv = document.getElementById("eolResults");

    if (!softwareName) {
        resultsDiv.innerHTML = "<p>Please enter a software name.</p>";
        return;
    }

    fetch(`/api/eol_info?name=${encodeURIComponent(softwareName)}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultsDiv.innerHTML = `<p>${data.error}</p>`;
            } else {
                let output = "<h2>End of Life Information</h2><ul>";
                data.forEach(item => {
                    output += `<li>
                        <strong>Version:</strong> ${item.version} <br>
                        <strong>Release Date:</strong> ${item.release_date} <br>
                        <strong>EOL Date:</strong> ${item.eol_date} <br>
                        <strong>Latest Version:</strong> ${item.latest_version} <br>
                        <strong>Latest Release Date:</strong> ${item.latest_release_date} <br>
                        <strong>Support Status:</strong> ${item.support_status}
                    </li><hr>`;
                });
                output += "</ul>";
                resultsDiv.innerHTML = output;
            }
        })
        .catch(error => {
            resultsDiv.innerHTML = `<p>Error fetching data: ${error}</p>`;
        });
}
