function get_professor_set() {
	

	$.ajax({
		type:"POST",
		url:"/aulas/get_professor_set/",
		data:{
			'disciplina' : $('#id_disciplina').val(),
			'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
		},
		success: searchPofessores,
		dataType: 'html'
	});
	
	/*
    new Ajax.Request('/aulas/get_professor_set/', { 
    	method: 'post',
    	parameters: $H({'disciplina':$('id_disciplina').getValue()}),
			
	    onSuccess: function(transport) {
	        var e = $('id_professor')
	        if(transport.responseText)
	            e.update(transport.responseText)
	    }
    }); // end new Ajax.Request
	*/
}

function searchPofessores(data,textStatus,jqXHR) {
	$('#id_professor').html(data);
}