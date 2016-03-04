/**
 * Created by Patrik on 3. 3. 2016.
 */

    var menu = {};

    menu.name = '';

$('#search').keyup(function(){
    $.ajax({
        type: 'POST',
        url: '/ttt/menu/searchPlayer/',
        data: {'player': $('#search').val(), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
        success: menu.getPlayers,
        dataType: 'json'
    });
});

    menu.getPlayers = function(data){
        console.log(data)
        var arr = [];
        for(var x in data){
             arr.push(data[x]);
        }
    }

    menu.getName = function(){
        $.ajax({
            type: 'GET',
            url: '/ttt/menu/searchPlayer/',
            success: function(name){
                console.log(name['name']);
                menu.name = name['name'];
            },
            dataType: 'json'
        });
    }
menu.getName();

