function filterClients() {
    const input = document.getElementById("search");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("clients-table");
    const trs = table.getElementsByTagName("tr");

    for (let i = 1; i < trs.length; i++) {
        const tds = trs[i].getElementsByTagName("td");
        if (tds.length > 0) {
            const name = tds[1].textContent.toLowerCase();
            const username = tds[2].textContent.toLowerCase();
            if (name.includes(filter) || username.includes(filter)) {
                trs[i].style.display = "";
            } else {
                trs[i].style.display = "none";
            }
        }
    }
}

window.addEventListener("DOMContentLoaded", () => {
    const rows = document.querySelectorAll("#clients-table tbody tr");
    rows.forEach(row => {
        const loanBalCell = row.children[4];
        const balance = parseFloat(loanBalCell.textContent.replace(/[^\d.-]/g, ''));
        if (balance > 100000) {
            row.style.backgroundColor = "#fff3cd";
        }
    });
});
