/**
 * Created by Patrik on 3. 3. 2016.
 */

    var menu = {};

    menu.name = '';
    menu.ws = new WebSocket('ws://localhost:9001/');

    menu.ws.onmessage = function(msg){
        try {
            var json = JSON.parse(msg.data);
            menu.refreshPlayers(json);
        }catch (e){
            console.log(msg.data);
            if(msg.data == 'make_request'){
                menu.refreshPlayers();
            }
        }
    }

    menu.ws.onopen = function(){
        console.log('Connection established!');
        if(menu.name != '') {
            var msg = '{"status": 0, "name": ' + '"' + menu.name + '"' + '}';
            menu.ws.send(msg);
        }
    }

    menu.init = function(){
        this.findPlayers();
        this.getName();
        this.vsComp();
    }

    menu.vsComp = function(){
        $('button').click(function(){
            location.href = '/ttt/comp/3/';
        });
    }

    menu.getPlayers = function(json){
        $('#search_results').html('');
        console.log(json.names);
        json.names.forEach(function(player){
            console.log(player);
           $('#search_results').append('<li>' + player + '</li>');
        });
    }

    menu.findPlayers = function() {
        $('#search').keyup(function () {
            $.ajax({
                type: 'POST',
                url: '/ttt/menu/searchPlayer/',
                data: {'player': $('#search').val(), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
                success: menu.getPlayers,
                dataType: 'json'
            });
        });
    }

    menu.refreshPlayers = function() {
        $.ajax({
            type: 'GET',
            url: '/ttt/menu/searchPlayer/',
            success: menu.getPlayers,
            dataType: 'json'
        });
    }


    menu.getName = function(){
        $.ajax({
            type: 'GET',
            url: '/ttt/menu/getUser/',
            success: function(name){
                console.log(name['name']);
                menu.name =  name['name'];
            },
            dataType: 'json'
        });
    }


menu.init();

