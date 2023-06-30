const btnsEditar = document.querySelectorAll('.btnEditar');

btnsEditar.forEach((btn) => {
    btn.addEventListener('click', function (e) {
        const tds = e.target.closest('tr').querySelectorAll('td');
        id = tds[0].innerText;
        direccion = tds[1].innerText;
        tipo = tds[2].innerText;
        superficie_m2 = tds[3].innerText;
        valor = tds[4].innerText;
        imagen = tds[5].innerText;
        window.location.href = `cambio?id=${id}&direccion=${direccion}&tipo=${tipo}&superficie_m2=${superficie_m2}&valor=${valor}&imagen=${imagen}`
    });
});