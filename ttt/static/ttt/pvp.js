/**
 * Created by Patrik on 18. 3. 2016.
 */

    var game = {};

    game.user = '';
    game.myColor = '';
    game.opponentColor = '';
    game.squares = $('.square');
    game.size = 4;
    game.board = [];
    game.myPoints = [];
    game.opponentPoints = [];

    game.init = function(){
        this.setUpSquares();
        this.setUpBoard(game.size);
        //this.setUpConnection();
    }

    game.randomColor = function(){
        return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
    }

    game.getUser = function(){
        $.ajax({
           type: 'GET',
           url: '/ttt/getUser/',
           success: function(json){
               game.user = json.name;
           },
           dataType: 'json'
        });
    }

    game.setUpBoard = function(size){
        for(var i = 1; i < size + 1; i++){
            for(var j = 1; j < size + 1; j++){
                game.board.push([i, j]);
            }
        }
    }

    game.changeColor = function(){
        var color = this.randomColor();
        $('.player').css('backgroundColor', color);
        game.myColor = color;
        $.each(game.myPoints, function(idx, value){
            $($(game.squares).get(value)).css('backgroundColor', color);
        })
    }

    game.setUpSquares = function(){
        $('.square').addClass('noEvent');
        var colorP = this.randomColor();
        var colorO = this.randomColor();
        $('.player').css('backgroundColor', colorP);
        $('.opponent').css('backgroundColor', colorO);
        game.myColor = colorP;
        game.opponentColor = colorO;
        $('.player').click(function() {
            game.changeColor();
        });
        $('.square').on('click', function(){
           var idx = game.squares.index($(this));
           console.log('You clicked on square with index ' + idx + '!')
           $(this).css('backgroundColor', game.myColor);
           game.ws.send('{"status": 2, "point": ' + idx + '}');
           game.myPoints.push(idx);
           $(this).addClass('noEvent');
        });
    }

    game.markPoint = function(idx){
        console.log('Marking square of opponent!');
        $(game.squares.get(idx)).css('backgroundColor', game.opponentColor);
        $(game.squares.get(idx)).addClass('noEvent');
    }

    game.freeSquares = function(){
        //if not in myPoints or opPoints then remove noEvent
        //$.each(game.squares, function(idx, value){
        //    $($(game.squares).get(value)).css('backgroundColor', color);
        //})
    }

    game.manageJson = function(json){
        console.log('I am here');
        if('point' in json){
            console.log('Prisiel bod');
            this.markPoint(json['point']);
        }else if('go' in json){
        //    do smth
            // let player know it is his turn
            this.freeSquares();
        }
    }

    window.onbeforeunload = function(){
        $.ajax({
            type: 'GET',
            url: '/ttt/menu/dropConnection/'
        });
    }

    game.setUpConnection = function(){
        $.ajax({
            type: 'GET',
            url: '/ttt/menu/createConnection/',
            success: function(json){
                console.log(json);
                if(!('none' in json)) {
                    game.ws.send('{"status": 2, "connection": [' + '"' + json.me + '"' + ', ' + '"' + json.opponent + '"' + ']}');
                }
            },
            dataType: 'json'
        });
    }

// get user name via ajax request
game.getUser();
game.init();

    // Connection to the server
    game.ws = new WebSocket('ws://localhost:9001/');

    game.ws.onopen = function(){
        if(game.user !== '') {
            console.log(game.user);
            this.send('{"status": 2, "name": ' + '"' + game.user + '"' + '}');
            game.setUpConnection();
        }
    };

    game.ws.onmessage = function(msg){
        try{
            var json = JSON.parse(msg);
            game.manageJson(json);
        }catch (e){
            console.log('Huhuuuu');
            console.log(msg);
        }
    }

//game.init();