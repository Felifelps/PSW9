function flipCard(id) {
    let card = document.getElementById(id);
    card.style.display =  card.style.display === 'none' ? 'block': 'none';
}