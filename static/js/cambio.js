var args = location.search.substr(1).split('&');
//separa el string por los “&” creando una lista
// [“id=3” , “nombre=’tv50’” , ”precio=1200”,”stock=20”]
console.log(args)

var parts = []
for (let i = 0; i < args.length; ++i) {
    parts[i] = args[i].split('=');
}
console.log(parts)

document.getElementById("id").value = decodeURIComponent(parts[0][1])
document.getElementById("direccion").value = decodeURIComponent(parts[1][1])
document.getElementById("tipo").value = decodeURIComponent(parts[2][1])
document.getElementById("superficie").value = decodeURIComponent(parts[3][1])
document.getElementById("valor").value = decodeURIComponent(parts[4][1])
document.getElementById("imagen").value = decodeURIComponent(parts[5][1])

async function modificar() {
    let id = document.getElementById("id").value
    let direccion = document.getElementById("direccion").value
    let tipo = parseFloat(document.getElementById("tipo").value)
    let superficie = parseInt(document.getElementById("superficie").value)
    let valor = document.getElementById("valor").value
    let imagen = document.getElementById("imagen").value

    let producto = {
        direccion: direccion,
        tipo: tipo,
        superficie: superficie,
        valor: valor,
        imagen: imagen
    }
    let url = "http://localhost:5000/inmuebles/" + id
    var options = {
        body: JSON.stringify(producto),
        method: 'PUT',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json' },
        redirect: 'follow'
    }
    // await fetch(url, options)
    //     .then(function () {
    //         console.log("modificado")
    //         alert("Registro modificado")
    //         //window.location.href = "/inmuebles_lindo";
    //         //NUEVO,  si les da error el fetch  comentar esta linea que puede dar error  
    //     })
    //     .catch(err => {
    //         //this.errored = true
    //         console.error(err);
    //         alert("Error al Modificar")
    //     })

    await fetch(`${window.origin}/inmuebles/${id}`, {
        method: 'PUT',
        redirect: 'follow',
        mode: 'same-origin',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(producto)
    }).then(response => {
        // HTTP 301 response
        // HOW CAN I FOLLOW THE HTTP REDIRECT RESPONSE?
        if (response.redirected) {
            window.location.href = response.url;
        }
        console.log(response);

    }).catch(err => {
        //this.errored = true
        console.error(err);
        alert("Error al Modificar")
    })
}
