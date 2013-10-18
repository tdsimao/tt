from django import forms
from models import Aula
from professores.models import Professor
from disciplinas.models import Disciplina


class AulaForm(forms.ModelForm):
    
    professor = forms.ModelChoiceField(
        widget=forms.Select,
        queryset= Professor.objects.none(),
        required=True , empty_label=None
        )
    disciplina = forms.ModelChoiceField(
        widget=forms.Select(attrs={'onchange':'get_professor_set();','onload':'get_professor_set();', 'autofocus' : ''}),
        queryset= Disciplina.objects.none(),
        required=True , empty_label=None,
        
        )
    
    def __init__(self,*args, **kwargs):
        usuario = kwargs.pop('usuario',None)      
        turma = kwargs.pop('turma',None)     
        super(AulaForm,self).__init__(*args, **kwargs)
        
        
        #Remove disciplinas cadastradas para a turma
        disciplinasCadastradas =  Disciplina.objects.filter(id__in = Aula.objects.values_list('disciplina', flat=True).filter(turma = turma).all()).all()
        disciplinasNaoCadastradas =  Disciplina.objects.filter(user=usuario).exclude(id__in = disciplinasCadastradas)
        self.fields['disciplina'].queryset = Disciplina.objects.filter(user=usuario)
        
        
        self.fields['disciplina'].choices = [ (disciplina.id, str(disciplina)) for disciplina in disciplinasNaoCadastradas.all()]
        
        self.fields['professor'].queryset = Professor.objects.filter(user=usuario)
        
        instance = kwargs.pop('instance',None)   
        
        if instance:
            idDisciplina = instance.disciplina.id
            print instance
            self.fields['professor'].choices = [ (professor.id, str(professor)) for professor in Disciplina.objects.get(id=idDisciplina).professor_set.all()]
        else:
            idDisciplina = disciplinasNaoCadastradas.all()[0].id
            self.fields['professor'].choices = [ (professor.id, str(professor)) for professor in Disciplina.objects.get(id=idDisciplina).professor_set.all()]
        
    class Meta:
        model = Aula
        fields = ('disciplina','professor','quantidade',)