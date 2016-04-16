/**
 * Created by Patrik on 15. 4. 2016.
 */

    var scores = {};

    scores.getPlayers = function(json){
        var html = $('tbody').html('');
        for(var i = 0; i < json['scores'].length; i++){
           html = $('tbody').html();
           $('tbody').html( html +
               '<tr>' +
                    '<td>' + json['scores'][i][0] + '</td> <td>' +json['scores'][i][1] + '</td> <td>' + json['scores'][i][2] + '</td>' +
               '</tr>');
           if(i == 7){
               break;
           }
        };
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