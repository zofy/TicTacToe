/**
 * Created by Patrik on 20. 2. 2016.
 */
var squares = document.querySelectorAll('.square');
var colors = []; // colors of squares
var nums = []; // array for nums in rgb color

function generateColors(){
    for(i = 0; i < squares.length; i++){
        for(j = 0; j < 3; j++){
            nums.push(Math.round(256*Math.random()));
        }
        colors[i] = 'rgb(' + nums[0] + ', ' + nums[1] + ', ' + nums[2] + ')';
        nums.length = 0;
    }
}

function randomColor(){
    return 'rgb(' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ', ' + Math.round(256*Math.random()) + ')';
}

function changeColor(square){
    square.style.background = randomColor();
}

function setUpSquares(){
    for(i = 0; i < squares.length; i++){
        squares[i].style.background = colors[i];
        squares[i].addEventListener('click', function(){
            changeColor(this);
        })
    }
}

generateColors();
setUpSquares();