setTimeout(function() {
    var alert = document.getElementById('tempAlert');
    alert.style.opacity = '0'; // Altera a opacidade para 0 gradualmente
    setTimeout(function() {
        alert.style.display = 'none'; // Esconde o alerta depois que a opacidade for totalmente reduzida
    }, 2000); // Tempo igual ao tempo de transição
}, 3000);