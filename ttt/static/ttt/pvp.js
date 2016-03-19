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

    game.init = function(){
        this.setUpSquares();
        this.setUpBoard(game.size);
    }

    game.randomColor = function(){
        return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
    }

    game.getUSer = function(){
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
        $('.player').click(function() {
            game.changeColor();
        });
        $('.square').on('click', function(){
           var idx = game.squares.index($(this));
           console.log('You clicked on square with index ' + idx + '!')
           console.log('Color:' + game.myColor);
           $(this).css('backgroundColor', game.myColor);
           game.ws.send('{"status": 2, "point": ' + game.board[idx] + '}');
           game.myPoints.push(idx);
           $(this).addClass('noEvent');
        });
        $('.player').css('backgroundColor', this.randomColor());
        $('.opponent').css('backgroundColor', this.randomColor());
        game.myColor = $('.player').css('backgroundColor');
        game.opponentColor = $('.opponent').css('backgroundColor');
    }

    game.markPoint = function(idx){
        console.log('Marking square of opponent!');
        $(game.squares.get(idx)).css('backgroundColor', game.opponentColor);
    }

    game.manageJson = function(json){
        if('idx' in json){
            this.markPoint(json['idx']);
        }
    }

    // Connection to the server
    game.ws = new WebSocket('ws://localhost:9001/');

    game.ws.onopen = function(){
        //this.send('{"status": 2, "name": ' + '"' + game.user + '"' + '}');
    };

    game.ws.onmessage = function(msg){
        try{
            var json = JSON.parse(msg);
            game.manageJson(json);
        }catch (e){
            console.log(msg);
        }
    }

game.init();