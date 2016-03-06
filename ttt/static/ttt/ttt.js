/**
 * Created by Patrik on 20. 2. 2016.
 */


var game = {};

    game.ws = new WebSocket('ws://localhost:9001/');
    game.squares = [];
    game.playerSquare = document.querySelector('.player'); // square color of the player
    game.playerColor = ''; //color of player
    game.compColor = 'hotpink'; // color of computer
    game.squaresOfPlayer = []; // squares that have already been clicked by the player
    game.boardSize = 3; // size of the board
    game.boardPoints = [];
    game.computer = document.querySelector('.hidden').textContent;
    game.status = -1;



    game.init = function(){
        this.reset();
        this.setUpBoard();
        this.setUpGame();
    }

    game.setUpBoard = function(){
        for(var i = 1; i < this.boardSize + 1; i++){
            for(var j = 1; j < this.boardSize + 1; j++) {
                this.boardPoints.push([i, j]);
            }
        }
    }

    game.idxOfPoint = function(point){
        for(var i=0; i< this.boardPoints.length; i++) {
            if (this.boardPoints[i][0] == point[1] && this.boardPoints[i][1] == point[4]) {
                console.log(this.boardPoints[i][0]);
                return i;
            }
        }
        return -1;
    }

    // server sends msg what move comp makes
    game.ws.onmessage = function(msg){
        if(msg.data.length > 6){
            console.log(msg.data);
        }else {
            console.log(msg.data);
            var point = msg.data.toString();
            var idx = game.idxOfPoint(point); // index of point in boardPoints
            console.log(idx);
            game.squares[idx].style.background = game.compColor;
            game.squares[idx].classList.add('noEvent');
            game.boardPoints.splice(idx, 1);
            game.squares.splice(idx, 1);
        }
    }

    game.randomColor = function(){
        return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
    }

    game.stylePlayersSquares = function(color){
        this.squaresOfPlayer.forEach(function(square){
            square.style.background = color;
        });
    }

    game.checkSquaresColor = function(color){
        this.squares.forEach(function(square){
            if(square.classList[0] !== 'player') {
                while (square.style.background === color) {
                    square.style.background = game.randomColor();
                }
            }
        });
    }

    game.changeColor = function(square){
        if(square.classList[0] === 'player') {
            var color = this.randomColor();
            this.playerColor = color;
            square.style.background = color;
            this.stylePlayersSquares(color);
            this.checkSquaresColor(color);
        }else{
            this.checkSquaresColor(this.playerColor);
            square.style.background = this.playerColor;
            this.squaresOfPlayer.push(square);
            this.squares.splice(game.squares.indexOf(square), 1);
            square.classList.add('noEvent');
        }
    }

    // msg is sent only when it is user's turn
    game.msgToServer = function(square, event){
        if(event !== 'change' && square !== this.playerSquare){
            var idx = this.squares.indexOf(square);
            if(game.ws.readyState === 1) {
                console.log('sme tu');
                var msg = '{"status": ' + game.status + ', "point": ' + '"' + this.boardPoints[idx] + '"' + '}';
                console.log(msg);
                game.ws.send(msg);
            }
            this.boardPoints.splice(idx, 1);
        }
    }

    game.reset = function(){
        this.squares = [].slice.call(document.querySelectorAll('.square'));
        this.boardPoints = [];
        this.setUpBoard();
        this.squaresOfPlayer = [];
        this.squares.forEach(function(square){
            square.style.background = game.randomColor();
            square.classList.remove('noEvent');
        });
        var color = this.randomColor();
        while(color == this.compColor) {
            color = this.randomColor();
        }
        this.playerColor = color;
        this.playerSquare.style.background = color;
    }

    game.setUpGame = function(){
        this.squares.push(this.playerSquare);
        this.squares.forEach(function(square){
            ('click change').split(' ').forEach(function(event) {
                square.addEventListener(event, function () {
                    game.msgToServer(square, event);
                    game.changeColor(this);
                });
            });
        });
        document.querySelector('#stripe button').addEventListener('click', function(){
            game.reset();
            game.ws.send('{"status": 1, "refresh": 1}');
        });
        if(this.computer){
            game.status = 1;
        }else{
            game.status = 2;
        }
    }


game.init();