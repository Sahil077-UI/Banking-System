function filterTable() {
    const input = document.getElementById("searchInput");
    const filter = input.value.toLowerCase();
    const table = document.getElementById("repaymentTable");
    const tr = table.getElementsByTagName("tr");

    for (let i = 1; i < tr.length; i++) {
        const row = tr[i];
        const tdAccount = row.getElementsByTagName("td")[0];
        const tdName = row.getElementsByTagName("td")[1];

        if (tdAccount && tdName) {
            const accText = tdAccount.textContent.toLowerCase();
            const nameText = tdName.textContent.toLowerCase();
            row.style.display = (accText.includes(filter) || nameText.includes(filter)) ? "" : "none";
        }
    }
}