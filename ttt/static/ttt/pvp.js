/**
 * Created by Patrik on 18. 3. 2016.
 */

    var game = {};

    game.user = '';
    game.myColor = '';
    game.opponentColor = '';
    game.squares = $('.square');
    game.size = 9;
    game.length = 5;
    game.myPoints = [];
    game.opponentPoints = [];

    game.directions = [[[0, 1], [0, -1]], [[1, 0], [-1, 0]], [[1, 1], [-1, -1]], [[1, -1], [-1, 1]]];

    game.init = function(){
        game.changeHeading("Your opponent is on the move");
        $('#squares').addClass('noEvent');
        this.setUpSquares();
        this.setUpChat();
    }

    game.randomColor = function(){
        return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
    }

    game.setUpChat = function(){
        $('#chat').val('');
        $('#chat').keypress(function(event){
           if(event.shiftKey != 1 && event.which == 13){
               var message = $(this).val().toString().replace(/^\s+|\s+$/g, '');
               console.log('Sending message to opponent...');
               console.log('Message is: ' + message);
               game.ws.send(message);
               $(this).val('');
               $('#myBubble .chatText').text(message);
               $('#myBubble').removeClass('hidden');
           }
        });
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

    game.getIndex = function(point){
        if(point[0] < 1 || point[1] < 1 || point[0] > game.size || point[1] > game.size){
            return -1;
        }
        return (point[0] - 1)*game.size + point[1] - 1;
    }

    game.getPoint = function(index){
        var a = Math.floor(index / game.size) + 1;
        var b = index % game.size + 1;
        return [a, b];
    }

    game.checkCount = function(points, point_idx, d){
        var count = 0;
        var idx = point_idx;
        var point = [];
        game.directions[d].forEach(function(direction){
            idx = point_idx;
            point = game.getPoint(point_idx);
            while(points.indexOf(idx) != -1){
                count++;
                point[0] += direction[0];
                point[1] += direction[1];
                idx = game.getIndex(point);
            }
        });
        count--;
        return count;
    }

    game.checkWin = function(points, point_idx){
        for(var d = 0; d < game.directions.length; d++){
            var count = game.checkCount(points, point_idx, d);
            console.log('Pocet pri sebe: ' + count);
            if(count >= game.length){
                console.log('You won!');
                $('h2').text('You won!');
                $('#header div').removeClass('hidden');
                game.ws.send('{"status": 2, "end": ' + '"' + game.user + '"' + '}');
                game.saveScore('winner');
                return true;
            }
        }
        return false;
    }

    game.setUpSquares = function(){
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
           game.myPoints.push(idx);
           game.ws.send('{"status": 2, "point": ' + idx + '}');
           if (!(game.checkWin(game.myPoints, idx))) {
               game.changeHeading("Your opponent is on the move");
           }
           $(this).addClass('noEvent');
           $('#squares').addClass('noEvent');
        });

        $('#header div').on('click', function(){
           console.log('Refresh...');
           game.ws.send('{"status": 2, "refresh": 1}');
           game.refresh();
           game.changeHeading("Your opponent is on the move");
        });
    }

    game.refresh = function(){
       $('.square').css('background', 'hotpink');
       $('.square').removeClass('noEvent');
       game.myPoints = [];
       game.opponentPoints = [];
       $('#header div').addClass('hidden');
    }

    game.markPoint = function(idx){
        console.log('Marking square of opponent!');
        $(game.squares.get(idx)).css('backgroundColor', game.opponentColor);
        $(game.squares.get(idx)).addClass('noEvent');
    }

    game.manageJson = function(json){
        console.log(json);
        if('point' in json){
            this.markPoint(json['point']);
            this.opponentPoints.push(json['point']);
            $(game.squares.get(json['point'])).addClass('noEvent');
        }else if('go' in json){
            game.changeHeading("It's your turn!");
            $('#squares').removeClass('noEvent');
        }else if('connection_drop' in json){
            game.changeHeading("Opponent went away!");
            $('body').addClass('noEvent');
            window.location.replace('/ttt/menu/');
        }else if('color' in json){
            game.opponentColor = json['color'];
            $('.opponent').css('backgroundColor', json['color']);
            game.changeColor(game.opponentPoints, json['color']);
        }else if('message' in json) {
            console.log(json['message']);
            $('#opBubble .chatText').text(json['message']);
            $('#opBubble').removeClass('hidden');
        }else if('end' in json){
            $('#squares').addClass('noEvent');
            $('h2').text(json['end'] + ' has won!');
            $('.fa-refresh').removeClass('hidden');
            game.saveScore('looser');
        }else if('me' in json){
            $('.player').css('backgroundColor', json['me']);
            $('.opponent').css('backgroundColor', json['opponent']);
            game.myColor = json['me'];
            game.opponentColor = json['opponent'];
        }else if('refresh' in json){
            game.refresh();
            game.changeHeading("It's your turn!");
            $('#squares').removeClass('noEvent');
        }
    }

    game.saveScore = function(result){
        $.ajax({
            type: 'POST',
            url: '/ttt/saveScore/',
            data: {'result': result, 'name': game.user, 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()}
        });
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
            console.log('Message accepted');
            console.log(msg);
        }
    }