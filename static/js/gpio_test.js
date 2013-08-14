<script type='application/javascript'>
	      $(document).ready(
			function() {
			      websocket = '%(scheme)s://%(host)s:%(port)s/ws';
			      if (window.WebSocket) {
			      	ws = new WebSocket(websocket);
			      }
			      else if (window.MozWebSocket) {
			      	ws = MozWebSocket(websocket);
			      }
			      else {
            			console.log('WebSocket Not Supported');
            			return;
			      }

          		window.onbeforeunload = function(e) {
            			$('#chat').val($('#chat').val() + 'Bye bye...\\n');
           			ws.close(1000, '%(username)s left the room');

            			if(!e) e = window.event;
           	 			e.stopPropagation();
            				e.preventDefault();
			};

          		ws.onmessage = function (evt) {

	     			if (evt.data.split(":")[0] == "Ana1"){
					$('#progressbar').progressbar("option", "value", parseInt(evt.data.split(":")[1].trim()), 10);}
				else if (evt.data.split(":")[0] == "Ana2"){
					$('#progressbar2').progressbar("option", "value", parseInt(evt.data.split(":")[1].trim()), 10);}
				else if (evt.data.split(":")[0] == "PWM"){
					$('#progressbar3').progressbar("option", "value", parseInt(evt.data.split(":")[1].trim()), 10);}
				else if (evt.data.split(":")[0] == "Servo"){
					$('#progressbar4').progressbar("option", "value", parseInt(evt.data.split(":")[1].trim()), 10);}
				else if (evt.data.split(":")[0] == "clearText"){
					$('#chat').val("");}
				else if (evt.data.split(":")[0] == "Stat"){
					x = evt.data.split(":");
					btnm = 'mode'.concat(x[1]);
					btnp = 'pin'.concat(x[1]);
					imgm = '/img/'.concat(x[2]).concat('.gif');
					imgp = '/img/'.concat(x[3]).concat('.gif');
					document.getElementById(btnm).src=imgm;
					document.getElementById(btnp).src=imgp;
					}
				else {  $('#chat').val($('#chat').val() + evt.data + '\\n');}
			};

          		ws.onopen = function() {
             			ws.send("%(username)s entered the room");
				$(this).statusCall();
				$(this).analogCall();
			};

         	 	ws.onclose = function(evt) {
             			$('#chat').val($('#chat').val() + 'Connection closed by server: ' + evt.code + ' \"' + evt.reason + '\"\\n');
          		};

          		$('#send').click(function() {
             			console.log($('#message').val());
            			ws.send('TextBox: ' + $('#message').val());
             			$('#message').val("");
             			return false;
          		});
		

		$(function() {
			$( "#slider-vertical1" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 255,
			value: 0,
			slide: function( event, ui ) {
				$( "#amount1" ).val( ui.value );
				ws.send("Slider1: " + ui.value);
				}
			});

			$( "#amount1" ).val( $( "#slider-vertical1" ).slider( "value" ) );

		});

		$(function() {
			$( "#slider-vertical2" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 255,
			value: 0,
			slide: function( event, ui ) {
				$( "#amount2" ).val( ui.value );
				ws.send("Slider2: " + ui.value);
				}
			});

			$( "#amount2" ).val( $( "#slider-vertical2" ).slider( "value" ) );

		});

		$(function() {
			$( "#slider-vertical3" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 1023,
			value: 0,
			slide: function( event, ui ) {
				$( "#amount3" ).val( ui.value );
				ws.send("PWM: " + ui.value);
				}
			});

			$( "#amount3" ).val( $( "#slider-vertical3" ).slider( "value" ) );

		});

		$(function() {
			$( "#slider-vertical4" ).slider({
			orientation: "vertical",
			range: "min",
			min: 0,
			max: 180,
			value: 0,
			slide: function( event, ui ) {
				$( "#amount4" ).val( ui.value );
				ws.send("Servo: " + ui.value);
				}
			});

			$( "#amount4" ).val( $( "#slider-vertical4" ).slider( "value" ) );

		});

		$(function() {
			$(".pin").click(function () {
				ws.send($(this).attr("value"));
			});
		
		});

		$(function() {
			var progressbar = $( "#progressbar" ),
			progressLabel = $( ".progress-label" );
			progressbar.progressbar({
				value: 0,
				max: 1023,
				change: function() {
					progressLabel.text( "ADC_1: " + (progressbar.progressbar( "value" ) + 1) );
				},
				complete: function() {
					progressLabel.text( "ADC_1: Max!" );
				}
			});
		});

		$(function() {
			var progressbar = $( "#progressbar2" ),
			progressLabel = $( ".progress-label2" );
			progressbar.progressbar({
				value: 0,
				max: 1023,
				change: function() {
					progressLabel.text( "ADC_2: " + (progressbar.progressbar( "value" ) + 1) );
				},
				complete: function() {
					progressLabel.text( "ADC_2: Max!" );
				}
			});
		});

		$(function() {
			var progressbar = $( "#progressbar3" ),
			progressLabel = $( ".progress-label3" );
			progressbar.progressbar({
				value: 0,
				max: 1023,
				change: function() {
					progressLabel.text( "PWM_1: " + (progressbar.progressbar( "value" ) + 1) );
				},
				complete: function() {
					progressLabel.text( "PWM_1: Max!" );
				}
			});
		});

		$(function() {
			var progressbar = $( "#progressbar4" ),
			progressLabel = $( ".progress-label4" );
			progressbar.progressbar({
				value: 0,
				max: 180,
				change: function() {
					progressLabel.text( "Servo: " + (progressbar.progressbar( "value" ) + 1) );
				},
				complete: function() {
					progressLabel.text( "Servo: Max!" );
				}
			});
		});

		$.fn.statusCall = function() {
			ws.send("Status:");
			setTimeout($(this).statusCall, 1000);
			};

		$.fn.analogCall = function() {
			ws.send("Analog:");
			setTimeout($(this).analogCall, 100);
			};

		});

		$('.chg1').click(function() {
                	$('#mode').val('Hi')
                	return false;
            	});

            	$('.chg2').click(function() {
                	$('#pin').val('Lo')
                	return false;
            	});


      </script>
