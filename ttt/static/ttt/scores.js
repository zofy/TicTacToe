/**
 * Created by Patrik on 15. 4. 2016.
 */

    var scores = {};

    scores.getPlayers = function(json){
        console.log(json);
    }

    scores.searchPlayer = function(){
        $('#search').keyup(function () {
            $.ajax({
                type: 'POST',
                url: '/ttt/searchScore/',
                data: {'player': $('#search').val(), 'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()},
                success: scores.getPlayers,
                dataType: 'json'
            });
        });
    }

    scores.searchPlayer();