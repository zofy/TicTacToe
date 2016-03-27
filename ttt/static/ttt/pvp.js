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
    game.freePoints = [];

    game.init = function(){
        this.setUpSquares();
        this.setUpBoard(game.size);
        this.fillFreePoints(game.size);
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

    game.changeHeading = function(text){
        $('h2').fadeIn(500, function(){
            $(this).text(text);
        });
    }

    game.changeColor = function(points, color){
        $.each(points, function(idx, value){
            $($(game.squares).get(value)).css('backgroundColor', color);
        });
    }

    game.fillFreePoints = function(size){
        for(var i = 0; i < size*size; i++){
           game.freePoints.push(i);
        };
    }

    game.setUpSquares = function(){
        // set me random color
        $('.square').addClass('noEvent');
        var colorP = this.randomColor();
        var colorO = this.randomColor();
        $('.player').css('backgroundColor', colorP);
        $('.opponent').css('backgroundColor', colorO);
        game.myColor = colorP;
        game.opponentColor = colorO;
        // set action on click
        $('.player').click(function() {
            var color = game.randomColor();
            $('.player').css('backgroundColor', color);
            game.myColor = color;
            game.changeColor(game.myPoints, color);
        });

        $('.square').on('click', function(){
           var idx = game.squares.index($(this));
           console.log('You clicked on square with index ' + idx + '!')
           $(this).css('backgroundColor', game.myColor);
           game.ws.send('{"status": 2, "point": ' + idx + '}');
           game.myPoints.push(idx);
           // here comes removing idx from free points
           game.freePoints.splice($(game.freePoints).index(idx), 1);
           $(this).addClass('noEvent');
           game.toggleFreeSquares();

           game.changeHeading("Your opponent is on the move");
        });
    }

    game.markPoint = function(idx){
        console.log('Marking square of opponent!');
        $(game.squares.get(idx)).css('backgroundColor', game.opponentColor);
        $(game.squares.get(idx)).addClass('noEvent');
    }

    game.toggleFreeSquares = function(){
        $.each(game.freePoints, function(idx, value){
            $($(game.squares).get(value)).toggleClass('noEvent');
        });
    }

    game.manageJson = function(json){
        console.log('I am here');
        console.log(json);
        if('point' in json){
            console.log('Prisiel bod');
            this.markPoint(json['point']);
            this.opponentPoints.push(json['point']);
            this.freePoints.splice($(game.freePoints).index(json['point']), 1);
        }else if('go' in json){
            game.changeHeading("It's your turn!");
            this.toggleFreeSquares();
        }else if('connection_drop' in json){
            game.changeHeading("Opponent went away!");
        }else if('color' in json){
            game.opponentColor = json['color'];
            $('.opponent').css('backgroundColor', json['color']);
            game.changeColor(game.opponentPoints, json['color']);
        }
    }

    //window.onbeforeunload = function(){
    //    $.ajax({
    //        type: 'GET',
    //        url: '/ttt/menu/dropConnection/'
    //    });
    //    return null;
    //}

    window.onbeforeunload = function (e) {
        var e = e || window.event;
           $.ajax({
            type: 'GET',
            url: '/ttt/menu/dropConnection/'
        });
        // For IE and Firefox prior to version 4
        if (e) {
            e.returnValue = 'Do you really want to end the game?';
        }
    };

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
    }

    game.ws.onmessage = function(msg){
        try{
            var json = JSON.parse(msg.data);
            game.manageJson(json);
        }catch (e){
            console.log('Huhuuuu');
            console.log(msg);
        }
    }