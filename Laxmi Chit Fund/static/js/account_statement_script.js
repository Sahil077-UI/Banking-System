// Live search for the account statement table
const searchInput = document.getElementById('searchInput');
const table = document.getElementById('statementTable');
const rows = table ? table.getElementsByTagName('tr') : [];

if (searchInput) {
    searchInput.addEventListener('input', function () {
        const filter = this.value.toLowerCase();

        for (let i = 1; i < rows.length; i++) {
            const rowText = rows[i].textContent.toLowerCase();
            rows[i].style.display = rowText.includes(filter) ? '' : 'none';
        }
    });
}