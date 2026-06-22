document.getElementById('shortenBtn').addEventListener('click', async () => {
    const longUrlInput = document.getElementById('longUrl').value;
    const resultContainer = document.getElementById('resultContainer');
    const shortLink = document.getElementById('shortLink');

    if (!longUrlInput) {
        alert("Please paste a valid URL first!");
        return;
    }

    try {
        // Send request to your FastAPI server
        const response = await fetch('/shorten', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ long_url: longUrlInput })
        });

        if (!response.ok) {
            throw new Error("Failed to shorten link. Make sure the URL format is correct.");
        }

        const data = await response.json();

        // Show result box and attach link details
        shortLink.href = data.short_url;
        shortLink.innerText = data.short_url;
        resultContainer.classList.remove('hidden');

    } catch (error) {
        alert(error.message);
    }
});