document.getElementById('loginBtn').addEventListener('click', function () {
    const phoneNumber = document.getElementById('phoneNumber').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('error-message');

    // Predefined login credentials
    const supervisor = { phone: '01878287485', password: '12345', redirectUrl: 'supervisor.html' };
    const ohs = { phone: '01725692402', password: 'ayonayon', redirectUrl: 'ohs.html' };

    // Validate login
    if (phoneNumber === supervisor.phone && password === supervisor.password) {
        window.location.href = supervisor.redirectUrl;
    } else if (phoneNumber === ohs.phone && password === ohs.password) {
        window.location.href = ohs.redirectUrl;
    } else {
        errorMessage.textContent = 'Invalid phone number or password';
    }
});
