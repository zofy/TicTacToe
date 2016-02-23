/**
 * Created by Patrik on 20. 2. 2016.
 */
var game = {};

    game.squares = document.querySelectorAll('.square');
    game.colors = []; // colors of squares
    game.nums = []; // array for nums in rgb color
    game.playerSquare = document.querySelector('.player'); // color of the player


    game.init = function(){
        this.generateColors();
        this.setUpSquares();
    }

    game.generateColors = function(){
        for(i = 0; i < this.squares.length; i++){
            for(j = 0; j < 3; j++){
                this.nums.push(Math.round(256*Math.random()));
            }
            this.colors[i] = 'rgb(' + this.nums[0] + ', ' + this.nums[1] + ', ' + this.nums[2] + ')';
            this.nums.length = 0;
        }
    }

    game.randomColor = function(){
        return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
    }

    game.playerColor = function(){
        return this.playerSquare.style.background;
    }

    game.changeColor = function(square){
        if(square.classList[0] === 'player') {
            square.style.background = this.randomColor();
        }else{
            square.style.background = this.playerColor();
        }
    }

    game.setUpSquares = function(){
        this.squares[this.squares.length] = this.playerSquare;
        for(i = 0; i < this.squares.length + 1; i++){
            this.squares[i].style.background = this.randomColor();
            this.squares[i].addEventListener('click', function(){
                game.changeColor(this);
            })
        }
    }


game.init();