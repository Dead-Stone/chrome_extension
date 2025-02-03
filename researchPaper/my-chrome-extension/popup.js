document.addEventListener('DOMContentLoaded', function() {
    const userId = 'user123';  // Replace with dynamic user ID
    let currentPaperId = null;  // Variable to store the current paper ID

    // Fetch recommendations from the backend API
    fetch(`http://localhost:5000/recommend?user_id=${userId}`)
        .then(response => response.json())
        .then(data => {
            displayPaper(data[0]);  // Show the first recommended paper
        });

    // Event listener for the Like button
    document.getElementById('like-btn').addEventListener('click', function() {
        interactWithPaper('like');
    });

    // Event listener for the Dislike button
    document.getElementById('dislike-btn').addEventListener('click', function() {
        interactWithPaper('dislike');
    });

    // Function to display the paper information in the popup
    function displayPaper(paper) {
        // Set the current paper ID
        currentPaperId = paper.paper_id;

        // Display the paper title, abstract, and link in the popup
        document.getElementById('title').textContent = paper.title;
        document.getElementById('abstract').textContent = paper.abstract;
        document.getElementById('link').href = paper.link;
    }

    // Function to handle Like/Dislike interactions
    function interactWithPaper(interaction) {
        if (!currentPaperId) {
            console.error("No paper ID found for interaction.");
            return;
        }

        // Send the interaction to the backend API
        fetch('http://localhost:5000/interact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, paper_id: currentPaperId, interaction_type: interaction })
        });
    }
});
