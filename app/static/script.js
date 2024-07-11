setTimeout(function() {
    var alert = document.getElementById('tempAlert');
    alert.style.opacity = '0'; // Altera a opacidade para 0 gradualmente
    setTimeout(function() {
        alert.style.display = 'none'; // Esconde o alerta depois que a opacidade for totalmente reduzida
    }, 2000); // Tempo igual ao tempo de transição
}, 3000);


document.getElementById('copyLinkBtn3').addEventListener('click', function() {
    const linkButton = document.getElementById('linkToCopy4');
    const link = linkButton.innerText.trim();

    navigator.clipboard.writeText(link).then(function() {
        alert('Link copiado com sucesso!');
    }, function(err) {
        console.error('Erro ao copiar o link: ', err);
    });
});

document.getElementById('copyLinkBtn5').addEventListener('click', function() {
    const linkButton = document.getElementById('linkToCopy5');
    const link = linkButton.innerText.trim();

    navigator.clipboard.writeText(link).then(function() {
        alert('Link copiado com sucesso!');
    }, function(err) {
        console.error('Erro ao copiar o link: ', err);
    });
});

document.getElementById('copyLinkBtn4').addEventListener('click', function() {
    const linkButton = document.getElementById('linkToCopy3');
    const link = linkButton.innerText.trim();

    navigator.clipboard.writeText(link).then(function() {
        alert('Link copiado com sucesso!');
    }, function(err) {
        console.error('Erro ao copiar o link: ', err);
    });
});

document.getElementById('copyLinkBtn2').addEventListener('click', function() {
    const linkButton = document.getElementById('linkToCopy2');
    const link = linkButton.innerText.trim();

    navigator.clipboard.writeText(link).then(function() {
        alert('Link copiado com sucesso!');
    }, function(err) {
        console.error('Erro ao copiar o link: ', err);
    });
});

document.getElementById('copyLinkBtn').addEventListener('click', function() {
    const linkButton = document.getElementById('linkToCopy');
    const link = linkButton.innerText.trim();

    navigator.clipboard.writeText(link).then(function() {
        alert('Link copiado com sucesso!');
    }, function(err) {
        console.error('Erro ao copiar o link: ', err);
    });
});