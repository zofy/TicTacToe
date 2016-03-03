/**
 * Created by Patrik on 3. 3. 2016.
 */
//var menu = {};
//    menu.ws = new WebSocket('ws://localhost:9001/');
//    menu.listOfPlayers = '';

$('#search').keyup(function(){
    $.ajax({
        type: 'POST',
        url: '/ttt/menu/searchPlayer/',
        data: {'player': $('#search').val(), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
        success: searchSuccess,
        dataType: 'html'
    })
});

function searchSuccess(data, textStatus, jqXHR){
    $('#search_results').html(data);
}

