document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Send login data to the backend for validation
    fetch("/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    })
        .then((response) => response.json())
        .then((data) => {
            if (data.status === "success") {
                // Successful login
                document.getElementById('message').innerText = 'Login successful!';
                document.getElementById('message').style.color = 'green';

                // Redirect to the home page after 1 second (optional delay)
                setTimeout(() => {
                    window.location.href = '/home'; // Adjust route as needed
                }, 1000);
            } else {
                // Show error message for invalid user
                alert(data.message);
                document.getElementById('message').innerText = 'Invalid username or password.';
                document.getElementById('message').style.color = 'red';
            }
        })
        .catch((error) => {
            console.error("Error:", error);
            alert("An error occurred. Please try again later.");
        });
});


document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(function(messageElement) {
        const message = messageElement.getAttribute('data-message');
        alert(message);  // This will show the flash messages as alerts
    });
});
