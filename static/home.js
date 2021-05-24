var HOST = "localhost:5000";

function enviarPeticion(){
    var keyWords = $("#keywords").val();
    var format = $("input:radio[name='format']:checked").val();
    var accept = $("#accept").val();
    var url = "/search?keyWords="+keyWords+"&format="+format+"&accept="+accept;
    $.ajax({
        url: url,
        type:"GET",
        success: function(response){
            //datos = JSON.parse(response);
            //console.log(response);
            $("#resultado").val(response);
            $(".preloader").css("display", "none");
            $("input, label, button ").toggleClass("disabled");
            $("#guardar").removeClass("disabled");
            $("input, label, button ").prop('disabled', false);
        },
        error: function(error){
            console.log(error);
            if(error.status == 500){
                $("#resultado").val("Lo sentimos, algo ha fallado en el proceso. Intente nuevamente más tarde o comuníquelo al administrador.");
            }
            $(".preloader").css("display", "none");
            $("input, label, button ").toggleClass("disabled");
            $("#guardar").addClass("disabled");
            $("input, label, button ").prop('disabled', false);
        },
    });
    $(".preloader").css("display", "block");
    $("input, label, button ").toggleClass("disabled");
    $("input, label, button ").prop('disabled', true);
}

function saveTextAsFile() {
  var textToWrite = document.getElementById('resultado').value;
  var textFileAsBlob = new Blob([ textToWrite ], { type: 'text/plain' });
  var filename = $("#keywords").val().replaceAll(",","_");
  var extension = $("input:radio[name='format']:checked").val();
  var fileNameToSaveAs = filename + "." + extension; //filename.extension

  var downloadLink = document.createElement("a");
  downloadLink.download = fileNameToSaveAs;
  downloadLink.innerHTML = "Download File";
  if (window.webkitURL != null) {
    // Chrome allows the link to be clicked without actually adding it to the DOM.
    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
  } else {
    // Firefox requires the link to be added to the DOM before it can be clicked.
    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
    downloadLink.onclick = destroyClickedElement;
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
  }

  downloadLink.click();
}

function destroyClickedElement(event) {
  // remove the link from the DOM
  document.body.removeChild(event.target);
}

function cambiarVista(vista){
    $(".visible").removeClass("visible");
    if(["api","contacto"].includes(vista)){
        $("#"+vista).addClass("visible");
    }else{
        $("#principal").addClass("visible");
    }
}