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
            $("#resultado").val(response);
            $(".preloader").css("display", "none");
            $("input, label, button ").toggleClass("disabled");
            $("input, label, button ").prop('disabled', false);
        },
        error: function(error){
            console.log(error);
            $("#resultado").val(error);
            $(".preloader").css("display", "none");
            $("input, label, button ").toggleClass("disabled");
            $("input, label, button ").prop('disabled', false);
        },
    });
    $(".preloader").css("display", "block");
    $("input, label, button ").toggleClass("disabled");
    $("input, label, button ").prop('disabled', true);
}