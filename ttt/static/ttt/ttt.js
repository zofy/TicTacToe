/**
 * Created by Patrik on 20. 2. 2016.
 */

var game = {};

    game.squares = document.querySelectorAll('.square');
    game.colors = []; // colors of squares
    game.nums = []; // array for nums in rgb color


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

    game.changeColor = function(square){
        square.style.background = this.randomColor();
    }

    game.setUpSquares = function(){
        for(i = 0; i < this.squares.length; i++){
            this.squares[i].style.background = this.colors[i];
            this.squares[i].addEventListener('click', function(){
                game.changeColor(this);
            })
        }
    }


game.init();