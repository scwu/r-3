$(document).ready(function() {
	$('.button').click(function(event) {
		var origin = $('#origin').val();
		var destination = $('#destination').val();
		var leave_date = $('#inputField').val();
		var return_date = $('#inputField2').val();
		var own_car = $('input#car').is(':checked');
		var can_drive = $('input#drive').is(':checked');
	  var cost = $("#cost_value").val();
    console.log("hi");

    $.ajax({
      type: 'POST',
      url: '/_find/',
      data: {
        'ori' : origin,
        'dest' : destination,
        'leave' : leave_date,
        'returnd' : return_date,
        'own' : own_car,
        'can' : can_drive
      }, 
      success: function(data) {
        alert(data);
      },
      error: function() {
        alert("Error");
      },
    });
    return false;
	});
});