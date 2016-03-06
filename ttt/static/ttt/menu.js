/**
 * Created by Patrik on 3. 3. 2016.
 */

    var menu = {};

    menu.name = '';
    menu.ws = new WebSocket('ws://localhost:9001/');


    menu.ws.onmessage = function(msg){
        console.log(msg.data);
        menu.refreshPlayers(msg);
    }

    menu.ws.onopen = function(){
        console.log('Connection established!');
        if(menu.name != '') {
            var msg = '{"status": 0, "name": ' + '"' + menu.name + '"' + '}';
            console.log(msg);
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

    menu.refreshPlayers = function(msg){
        var data = JSON.parse(msg.data);
        var names = data.slice(1, -1).split(',');
        names.forEach(function(name){
            $('#search_results').append('<li>' + name.trim().slice(1, -1) + '</li>')
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
                menu.name =  name['name'];
            },
            dataType: 'json'
        });
    }


menu.init();

