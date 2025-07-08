function toggleAdminPassword() {
    const passwordInput = document.getElementById('admin-password');
    const type = passwordInput.getAttribute('type');
    passwordInput.setAttribute('type', type === 'password' ? 'text' : 'password');
}