/**
 * Created by Patrik on 20. 2. 2016.
 */

var game = {};

    game.ws = new WebSocket('ws://localhost:9001/');
    game.squares = [].slice.call(document.querySelectorAll('.square'));
    game.colors = []; // colors of squares
    game.nums = []; // array for nums in rgb color
    game.playerSquare = document.querySelector('.player'); // square color of the player
    game.playerColor = ''; //color of player
    game.squaresOfPlayer = [];


    game.init = function(){
        this.setUpSquares();
    }

    game.ws.onmessage = function(msg){
        console.log(msg.data);
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

    game.setUpSquares = function(){
        this.squares.push(this.playerSquare);
        this.squares.forEach(function(square){
            square.style.background = game.randomColor();
            square.addEventListener('click', function(){
                game.ws.send(game.squares.indexOf(square));
                game.changeColor(this);
            });
        });
        this.playerColor = this.playerSquare.style.background;
    }


game.init();