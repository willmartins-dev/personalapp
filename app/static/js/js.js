$(document).ready(function() {    
    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
    //MENU
    $('.open-menu').on('click', function(){
        $('.menu').removeClass('hidden');
        $('.menu').addClass('fade-in');
        $('.menu').removeClass('fade-out');

        $('.bg-menu').removeClass('hidden');
        $('.bg-menu').addClass('fade-in');
        
        
    });
    $('#close-menu').on('click', function(){
         $('.menu').removeClass('fade-in');
        $('.menu').addClass('fade-out');
        $('.menu').addClass('hidden');
        $('.bg-menu').addClass('hidden');
       $('.bg-menu').removeClass('fade-out');
    });

    $("#buscaInput").on("keyup", function() {
        var termoBusca = $(this).val();
        if (termoBusca.length > 2) { // Opcional: buscar após 3 caracteres
            $.ajax({
                url: '/buscar_exercicio/', // Substitua por seu URL
                type: 'GET', // ou 'POST'
                data: {
                    'termo': termoBusca
                },
                dataType: 'json',
                success: function(data) {
                    var resultadosHtml = "";
                    if (data.length > 0) {
                        $.each(data, function(i, item) {
                            resultadosHtml += "<p>" + item.titulo + "</p>"; // Adapte conforme seus dados
                        });
                    } else {
                        resultadosHtml = "<p>Nenhum resultado encontrado.</p>";
                    }
                    $("#resultadosBusca").html(resultadosHtml);
                },
                error: function(jqXHR, textStatus, errorThrown) {
                    console.error("Erro na requisição AJAX: " + textStatus, errorThrown);
                }
            });
        } else {
            $("#resultadosBusca").html(""); // Limpa os resultados se a busca for muito curta
        }
    });
    $('#close').on('click', function(e){
        e.preventDefault()
         $('#modal').addClass('hidden')
         $('#modal-busca').addClass('hidden')
    });
    $('#close-busca').on('click', function(e){
        e.preventDefault()
        $('#resultadosBuscaexercicio').innerHtml="<p class='m-auto'><i class='fa-solid fa-search'></i> Pesquise os exercícios!</p>";
         $('#modal-busca').addClass('hidden');
    });
    $('[data-modal-busca]').on('click', function(e){
        $('#modal-busca').removeClass('hidden')
        e.preventDefault();
        const urlId = document.getElementById('buscar-exercicio');
        
        url_busca = $(this).attr('href');
        urlId.dataset.buscar=$(this).data('modal-busca');

    });
    $('[data-modal-view]').on('click', function(e){
        $('#modal').removeClass('hidden')
        e.preventDefault()

        url2 = $(this).attr('href');

          $.ajax({
                url: url2,
                type: 'GET', // ou 'POST'
                beforeSend: function() {
                    $('#ajaxLoader').show(); // Show loader
                },
                success: function(data) {
                    $(".content-modal").load(url2);
                },
                complete: function() {
                    $('#ajaxLoader').hide(); // Hide loader after completion (success or error)
                }
            })
        
    });
    $('.avaliacao').on('click', function(e){
        $('#modal').removeClass('hidden')
        e.preventDefault()

        url2 = $(this).attr('href');

          $.ajax({
                url: url2,
                type: 'GET', // ou 'POST'
                beforeSend: function() {
                    $('#ajaxLoader').show(); // Show loader
                },
                success: function(data) {
                    $(".content-modal").load(url2);
                },
                complete: function() {
                    $('#ajaxLoader').hide(); // Hide loader after completion (success or error)
                }
            })
        
    });


    $('[data-buscar]').on("keyup", function(e) {
        var termoBusca = $(this).val();
        var id = e.target.dataset.buscar;
        var url_busca_exercicio = '/buscar_exercicio_sessao/?termo='+termoBusca+'&id_sessao='+id;
        var resultadosHtml = document.getElementById('resultadosBuscaexercicio');
        if (termoBusca.length > 2) { 
            resultadosHtml.innerHtml = '';
            $.ajax({
                url:url_busca_exercicio,
                method:'GET',
                data:{
                    'termo':termoBusca,
                    'id_sessao':id,
                },
                dataType:'html',
                success: function(data){
                    const queryString =url_busca_exercicio
                    
                    const params = new URLSearchParams(queryString.split('?')[1]);
                    resultadosHtml.innerHTML=data;
                    //inserir banco
                    const listaExercicio = document.querySelectorAll('.addExercicios');
                    listaExercicio.forEach(item => {
                        item.addEventListener('click', function(e){
                            $('.add-success').slideDown(1000).fadeIn(400).delay(1000);
                            $('.add-success').slideUp(1000).fadeOut(400);

                            e.preventDefault();
                            const url_2 = item.getAttribute('href');
                            const dataId = params.get('id_sessao');
                            const dataNome = item.dataset.nome;
                            const dataImg = item.dataset.imagem;
                            
                            let jsonData = {'id':dataId, 'exercicio':dataNome, 'imagem':dataImg} 
                            fetch(url_2, {
                                method:'POST',
                                headers:{
                                    'Content-type': 'application/json',
                                    'X-CSRFToken':csrftoken,
                                },
                                body: JSON.stringify(jsonData)
                            })
                            .then(response => response.json())
                            .then(data =>{
                                
                                
                            })
                            .catch((error)=>{
                                console.error('Erro', error);
                            }); 
                        });
                    });
                    
                },
                error: function(jqXHR, textStatus,errorThrown){
                    console.error('Error:', textStatus, errorThrown);
                },
            });
        } else {

           //resultadosHtml.innerHTML="Nenhum resultado"; // Limpa os resultados se a busca for muito curta
        }
    });
   
});
   