$(document).ready(function() {
	$('.button').click(function() {
		e.preventDefault();
		var origin = $('#origin').val();
		var destination = $('#destination').val();
		var leave_date = $('#inputField').val();
		var return_date = $('inputField2').val();
		var own_car = $('input#car').is(':checked');
		var can_drive = $('input#drive').is(':checked');
	
		$.getJSON($SCRIPT_ROOT + '/_find', {
            ori : origin,
            dest : destination,
            leave : leave_date,
            return_d : return_date,
            own : own_car,
            can : can_drive
         }, function(data) {
              $.each(data, function(k, v) {
                  try {
                    var img = v[0].img;
                    var name = v[0].name;
                    var url = v[0].url;
                    $('#searchresults').html('<p id = "' + k + '"><a href="' + url + '">' + '<img src="' + img + '&s=50"></img>' 
                           + '<span>' + name + '</span></a>');
                    var content = $('div#searchresults').height();
                    $('#ajaxresults').height(content);
                    console.log(content);
                  }
                  catch (err) {
                    $('#ajaxresults').height(25);
                    $('#searchresults').html('<p>Sorry, no results found.</p>');
                  }
              });
         });

	});

	
};