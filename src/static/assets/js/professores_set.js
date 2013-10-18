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
		
function searchPofessores(data,textStatus,jqXHR) {
	$('#id_professor').html(data);
}