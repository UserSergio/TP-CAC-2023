function guardar() {
    if (document.getElementById("flexRadioDefault1").checked==true){
        e="Perdida"
    }else{
        e="Encontrada"}
 
    let n = document.getElementById("nameInput").value
    if (n === "") {
        alert("El nombre no puede estar vacío");
        return false;
      }
    // Verificar si el nombre contiene solo caracteres alfabéticos y espacios
    for (var x = 0; x < n.length; x++) {
        var charCode = n.charCodeAt(x);
        if (!((charCode >= 65 && charCode <= 90) || (charCode >= 97 && charCode <= 122) || charCode === 32)) {
          alert("El campo 'nombre' solo puede contener caracteres alfabéticos y espacios.");
          return false;
        }
      }
      
    let t = document.getElementById("phoneInput").value
    var phoneno = /^\d{10}$/;
    if (!t.match(phoneno)) {
      alert("Numero de telefono invalido");
      return false;
    }

    let m = document.getElementById("emailInput").value
    if (m === "") {
      alert("Necesitamos su dirección de email");
      return false;
    }
 
    let b = document.getElementById("dateSelect").value
    if (b == "Seleccionar el Barrio") {
        alert("Debe seleccionar un barrio");
        return false;
      }
  
    let f = document.getElementById("dateInput").value
    esFecha = Date.parse(f)
    if (isNaN(esFecha)) {
      alert("Debe ingresar la fecha del evento");
      return false;
    }

    let i = document.getElementById("dateFile").value

     let producto = {
        estado: e,
        nombre: n,
        telefono: t,
        email: m,
        barrio: b,
        fecha: f,
        imagen: i
    }
    let url = "http://localhost:5000/productos"
    var options = {
        body: JSON.stringify(producto),
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
    }
    fetch(url, options)
        .then(function () {
            console.log("creado")
            alert("Grabado")
            // Devuelve el href (URL) de la página actual
            window.location.href = "./index.html";  
            // Handle response we get from the API
        })
        .catch(err => {
            //this.errored = true
            alert("Error al grabar" )
            console.error(err);
        })
}
