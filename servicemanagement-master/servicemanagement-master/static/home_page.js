
document.addEventListener('DOMContentLoaded', function () {
    // Mock user object for demonstration purposes
    let currentUser = { username: 'demoUser', role: 'user' };

    // Check if the user is authenticated
    if (!currentUser) {
        alert('User not authenticated. Redirecting to login page.');
        window.location.href = 'index.html';
    }

    // Logout button functionality
    document.getElementById('logoutBtn').addEventListener('click', function () {
        // Clear the current user session and redirect to the login page
        currentUser = null;
        alert('Logout successful. Redirecting to login page.');
        window.location.href = 'index.html';
    });document.addEventListener('DOMContentLoaded', function () {
    // Login button functionality
    document.getElementById('loginBtn').addEventListener('click', function () {
        // Add login functionality here
        alert('Login functionality goes here');
    });

    // Redirect to service request page
    document.getElementById('createRequestBtn').addEventListener('click', function () {
        window.location.href = 'service_request_Page.html'; // Replace with the correct URL of your service request page
    });

    // Redirect to request status page
    document.getElementById('requestStatusBtn').addEventListener('click', function () {
        window.location.href = 'request_status.html'; // Replace with the correct URL of your request status page
    });
    // Example button click event for "Create Request"
    const createRequestBtn = document.getElementById('createRequestBtn');

    createRequestBtn.addEventListener('click', () => {
        // Redirect to the Service_Request_Page.html
        window.location.href = 'Service_Request_Page.html';
    });
});
});
