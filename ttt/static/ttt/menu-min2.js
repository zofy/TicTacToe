var menu={};menu.name='';menu.init=function(){this.findPlayers();this.getName();this.vsComp();this.setActions()}menu.manageJson=function(json){if('name'in json){$('#notifications h2').text(json.name+' wants to play with you!');$('#notifications span').html('<button>Yes</button> <button>No</button>')}else if('connection_drop'in json){$('#notifications h2').text('Connection with '+json.connection_drop+' dropped down!')}}menu.vsComp=function(){$('button').click(function(){location.href='/ttt/comp/3/'})}menu.getPlayers=function(json){$('#search_results').html('');console.log(json.names);json.names.forEach(function(player){console.log(player);$('#search_results').append('<li><span style="cursor: pointer"><i class="fa fa-user-plus"></i></span>'+player+'</li>')})}menu.findPlayers=function(){$('#search').keyup(function(){$.ajax({type:'POST',url:'/ttt/menu/searchPlayer/',data:{'player':$('#search').val(),'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()},success:menu.getPlayers,dataType:'json'})})}menu.refreshPlayers=function(){$.ajax({type:'GET',url:'/ttt/menu/searchPlayer/',success:menu.getPlayers,dataType:'json'})}menu.getName=function(){$.ajax({type:'GET',url:'/ttt/menu/getUser/',success:function(name){console.log(name['name']);menu.name=name['name']},dataType:'json'})}menu.setActions=function(){$('h1 .fa-search').click(function(){$('#container input[type="text"]').fadeToggle()});$('#search_results').on('click','span',function(event){console.log($(this).parent().text());menu.ws.send('{"status": 0, "request": '+'"'+$(this).parent().text()+'"'+'}');$(this).parent().fadeOut(500,function(){$(this).remove()});event.stopPropagation()});$('#notifications span').on('click','button',function(){console.log('You clicked on one of the answer buttons.')})}menu.sendMessage=function(){console.log('posielam spravu');$.ajax({type:'POST',url:'/ttt/menu/sendMsg/',data:{'user':menu.name,'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val()},success:function(msg){console.log(msg);menu.ws.send(msg['msg'])},dataType:'json'})}menu.init();menu.ws=new WebSocket('ws://localhost:9001/');menu.ws.onmessage=function(msg){try{var json=JSON.parse(msg.data);menu.manageJson(json)}catch(e){console.log(msg.data);if(msg.data=='make_request'){menu.refreshPlayers()}}}menu.ws.onopen=function(){console.log('Connection established!');if(menu.name!=''){console.log('posielam status');menu.sendMessage()}}menu.ws.onclose=function(){menu.ws.close()}