$(function(){
	$('#disciplina').select(function(){
		
		$.ajax({
			type:"POST",
			url:"/aulas/professores_set/",
			data:{
				'disciplina' : $('#disciplina').val(),
				'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
			}
			success: searchPofessores,
			dataType: 'html'
		});
		
	});
	
});

function get_vehicle_color(){
    new Ajax.Request('/auto/ajax_purpose_staff/', { 
    	method: 'post',
    	parameters: $H({'type':$('id_type').getValue()}),
	    onSuccess: function(transport) {
	        var e = $('id_color')
	        if(transport.responseText)
	            e.update(transport.responseText)
	    }
    }); // end new Ajax.Request
}


function get_professor_set() {
	console.log('Teste-_______________________________-');
    new Ajax.Request('/aulas/get_professor_set/', { 
    	method: 'post',
    	parameters: $H({'disciplina':$('id_disciplina').getValue()}),
	    onSuccess: function(transport) {
	        var e = $('id_professor')
	        if(transport.responseText)
	            e.update(transport.responseText)
	    }
    }); // end new Ajax.Request
	
	
	$('#id_professor').html(data);
}
		
function searchPofessores(data,textStatus,jqXHR) {
	$('id_professor').html(data);
}