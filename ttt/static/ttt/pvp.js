/**
 * Created by Patrik on 18. 3. 2016.
 */

    var game = {};

    game.user = '';
    game.myColor = '';
    game.opponentColor = '';
    game.squares = $('.square');
    game.size = 4;
    game.length = 4;
    game.board = [];
    game.myPoints = [];
    game.opponentPoints = [];

    game.init = function(){
        this.setUpSquares();
        this.setUpBoard(game.size);
    }

    game.randomColor = function(){
        return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
    }

    //game.getUser = function(){
    //    $.ajax({
    //       type: 'GET',
    //       url: '/ttt/getUser/',
    //       success: function(json){
    //           console.log('Posielma svoje meno');
    //           game.user = json.name;
    //           game.ws.send('{"status": 2, "name": ' + '"' + json.name + '"' + '}');
    //       },
    //       dataType: 'json'
    //    });
    //}

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

    game.checkCount = function(points, point_idx, direction){
        num1 = point_idx;
        num2 = point_idx;
        count = 0;
        while(points.indexOf(num1) != -1){
            count++;
            num1 -= direction;
        }
        while(points.indexOf(num2) != -1){
            count++;
            num2 += direction;
        }
        count--;
        return count;
    }

    game.checkWin = function(points, point_idx){
        for(var d = 1; d < 6; d++){
            count = game.checkCount(points, point_idx, d);
            if(count == game.length){
                console.log('You won!');
            }
        }
    }

    game.setUpSquares = function(){
        // set me random color
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
            game.ws.send('{"status": 2, "color": ' + '"' + game.myColor + '"' + '}');
        });

        $('.square').on('click', function(){
           var idx = game.squares.index($(this));
           console.log('You clicked on square with index ' + idx + '!')
           $(this).css('backgroundColor', game.myColor);
           game.ws.send('{"status": 2, "point": ' + idx + '}');
           game.myPoints.push(idx);
           game.checkWin(game.myPoints, idx);
           // here comes removing idx from free points
           $(this).addClass('noEvent');
           $('#container').addClass('noEvent');

           game.changeHeading("Your opponent is on the move");
        });
    }

    game.markPoint = function(idx){
        console.log('Marking square of opponent!');
        $(game.squares.get(idx)).css('backgroundColor', game.opponentColor);
        $(game.squares.get(idx)).addClass('noEvent');
    }

    game.manageJson = function(json){
        console.log('I am here');
        console.log(json);
        if('point' in json){
            console.log('Prisiel bod');
            this.markPoint(json['point']);
            this.opponentPoints.push(json['point']);
        }else if('go' in json){
            game.changeHeading("It's your turn!");
            $('#container').removeClass('noEvent');
        }else if('connection_drop' in json){
            game.changeHeading("Opponent went away!");
            $('body').addClass('noEvent');
            window.location.replace('/ttt/menu/');
        }else if('color' in json){
            game.opponentColor = json['color'];
            $('.opponent').css('backgroundColor', json['color']);
            game.changeColor(game.opponentPoints, json['color']);
        }
    }

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
game.init();

    // Connection to the server
    game.ws = new WebSocket('ws://localhost:8889/ws');

    game.getUser = function(){
        $.ajax({
           type: 'GET',
           url: '/ttt/getUser/',
           success: function(json){
               console.log('Posielam svoje meno');
               console.log(json.name);
               game.user = json.name;
               game.ws.send('{"status": 2, "name": ' + '"' + json.name + '"' + '}');
           },
           dataType: 'json'
        });
    }

    game.ws.onopen = function(){
        game.getUser();
        game.setUpConnection();
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