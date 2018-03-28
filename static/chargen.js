function updateCharacterData(character) {
	$("#charid").val(character['charid']);
    $("#strength").text(character['stats'][0]);
    $("#dexterity").text(character['stats'][1]);
    $("#endurance").text(character['stats'][2]);
    $("#intelligence").text(character['stats'][3]);
    $("#education").text(character['stats'][4]);
    $("#social").text(character['stats'][5]);
    $("#age").text(character['age']);
    if (character['career']) {
    	$("#careerrow").show();
    	$("#career").text(character['career']);
    } else {
    	$("#careerrow").hide();
    }
    if (character['rank']) {
    	$("#rankrow").show();
    	$("#rank").text(character['rank']);
    } else {
    	$("#rankrow").hide();
    }
    if (character['terms']) {
    	$("#termsrow").show();
    	$("#terms").text(character['terms']);
    } else {
    	$("#termsrow").hide();
    }
    if (character['skills']) {
    	$("#skillsrow").show();
    	$("#skills").text(character['skills']);
    } else {
    	$("#skillsrow").hide();
    }
    if (character['possessions']) {
    	$("#possessionsrow").show();
    	$("#possessions").text(character['possessions']);
    } else {
    	$("#possessionsrow").hide();
    }
    if (character['credits']) {
    	$("#creditsrow").show();
    	$("#credits").text(character['credits']);
    } else {
    	$("#creditsrow").hide();
    }
    historytext = $('#historytext');
    historytext.empty();
    $.each(character['history'], function (index, value) {
    	historytext.append(value + '<br />');
    	});
    dierollhistory = $('#dierollhistory');
    dierollhistory.empty();
    $.each(character['dierolls'], function (index, value) {
    	dierollhistory.append(value + '<br />');
    	});   	
}

function openSheet() {
	window.open($SCRIPT_ROOT + '/sheet/' + $("#charid").val(), '_blank');
}

function readyNextStep(data) {
	config = data['next_step'];
	if (config[0] == 'select') {
		inputarea = $("#inputarea");
		inputarea.empty();
		inputarea.append('<select id="inputareaselect"></select>');
        $.each(config[3], function (index, value) {
            var listItem = $("<option></option>").val(value).html(value);
            $("#inputareaselect").append(listItem);
        });
        //inputarea.append('<input type="button" id="inputareabutton" value="' + config[2] + '" />');
        inputarea.append('<input type="button" class="button" id="inputareabutton" value="' + config[2] + '" />');
		$('#inputareabutton').bind('click', function() {
      		$.getJSON($SCRIPT_ROOT + '/' + config[1], {
      		'charid': $("#charid").val(),
        	'selection': $('#inputareaselect').val(),
      		}, function(data) {
      		updateCharacterData(data);
      		readyNextStep(data);
      	});
    });
	} else if (config[0] == 'finished') {
		$("#newcharacter").show();
		$("#randomcharacter").show();
		$("#newcharacter").prop("disabled", false);
		$("#randomcharacter").prop("disabled", false);

		inputarea = $("#inputarea");
		inputarea.empty();
		//inputarea.append('<a target="_blank" href="' + $SCRIPT_ROOT + '/sheet/' + data['charid'] + '">Get Sheet</a>');
		inputarea.append('<input type="button" class="button" value="Get Sheet" onclick="openSheet()" />');
	}
}

function newCharacter() {
	  $("#newcharacter").prop("disabled", true);
	  $("#randomcharacter").prop("disabled", true);
      $.getJSON($SCRIPT_ROOT + '/new_character', {}, function(data) {
		updateCharacterData(data);
        $("#newcharacter").hide();
        $("#randomcharacter").hide();
        $("#history").show();
        $("#character_sheet").show();
        readyNextStep(data);
      });
      return true;
  }

function randomCharacter() {
	  $("#newcharacter").prop("disabled", true);
	  $("#randomcharacter").prop("disabled", true);
      $.getJSON($SCRIPT_ROOT + '/random_character', {}, function(data) {
		updateCharacterData(data);
        $("#newcharacter").hide();
        $("#randomcharacter").hide();
        $("#history").show();
        $("#character_sheet").show();
        readyNextStep(data);
      });
      return true;
}
  $(document).ready(function(){
  		charid = $("#charid").val();
  		if (charid) {
  			$("#newcharacter").prop("disabled", true);
  			$.getJSON($SCRIPT_ROOT + '/load_character', {
  			'charid': charid,
  			}, function(data) {
  			updateCharacterData(data);
	  		$("#newcharacter").hide();
	        $("#history").show();
	        $("#character_sheet").show();
  			readyNextStep(data);
  			});
  		}
  });