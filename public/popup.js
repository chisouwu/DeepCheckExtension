// Extension FrontEnd
// Extract URL
( async () =>{
    const [tab] = await chrome.tabs.query({ active: true, lastFocusedWindow: true });
    const currentURL = tab.url;

    console.log("test2");
    // Display URL in the page
    var desc = document.getElementById("description");

    // Extract file name from URL
    const fileName = currentURL.substring(32, currentURL.length - 1) + ".mp4";

    // Debugging
    console.log(currentURL + fileName);

    // Send POST request to the Python backend
    const response = await fetch('http://127.0.0.1:5000/process-url', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: currentURL, file_name: fileName })
    });

    const data = await response.json();

    if (response.ok) {
        // Display the result from the backend
        desc.insertAdjacentHTML("afterend", `<p>Result: ${data.result}</p>`);
    } else {
        desc.insertAdjacentHTML("afterend", `<p>Error: ${data.error}</p>`);
    }
})();