const flashMessages = document.querySelectorAll('.flash-messages .alert');
flashMessages.forEach(msg => {
    setTimeout(() => {
        msg.style.transition = 'opacity o.5s';
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 500);
    }, 6000);
})


const searchInput = document.getElementById('search_id');
const searchBtn = document.getElementById('search_btn');
const resultsDiv = document.getElementById('search_results');

searchBtn.addEventListener('click', async () => {
    const id = searchInput.value.trim();
    if (!id) {
        resultsDiv.innerHTML = 'Veuillez entrer un ID.';
        setTimeout(() => { resultsDiv.innerHTML = ''; }, 10000);
        return;
    }

    const response = await fetch(`/search_transaction?id=${id}`);
    const data = await response.json();

    if (data.found) {
        resultsDiv.innerHTML = `Transaction trouvée : ${data.transaction.type}, Montant : ${data.transaction.amount} €, Destinataire : ${data.transaction.recipient}, Date : ${data.transaction.date}`;
    } else {
        resultsDiv.innerHTML = 'Aucune transaction trouvée.';
    }

    // Faire disparaître le message après 10 secondes
    setTimeout(() => {
        resultsDiv.innerHTML = '';
    }, 10000);
});



