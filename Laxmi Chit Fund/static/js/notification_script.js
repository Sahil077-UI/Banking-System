// Highlight recent notifications
window.addEventListener('DOMContentLoaded', () => {
    const notificationItems = document.querySelectorAll('.notification-item');
    const today = new Date().toISOString().split('T')[0];

    notificationItems.forEach(item => {
        const dateEl = item.querySelector('.date');
        if (dateEl && dateEl.textContent.includes(today)) {
            item.style.borderLeft = '4px solid #27ae60';
            item.style.background = '#eafaf1';
        }
    });
});