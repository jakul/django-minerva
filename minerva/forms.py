from minerva.models import SurveyQuestion
from django import forms
import json
from django.core.validators import EMPTY_VALUES
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

_TYPE_OF_ANSWER_CHOICES = (
    ('', '---------'),
    ('multiple_choice_single_answer', 'Multiple Choice (single answer)'),
)


class SurveyQuestionForm(forms.ModelForm):
    type_of_answer = forms.ChoiceField(choices=_TYPE_OF_ANSWER_CHOICES)
    answer_1 = forms.CharField(required=False)
    answer_2 = forms.CharField(required=False)
    answer_3 = forms.CharField(required=False)
    answer_4 = forms.CharField(required=False)
    answer_5 = forms.CharField(required=False)
    answer_6 = forms.CharField(required=False)
    answer_7 = forms.CharField(required=False)
    answer_8 = forms.CharField(required=False)
    answer_9 = forms.CharField(required=False)
    answer_10 = forms.CharField(required=False)
    answer_11 = forms.CharField(required=False)
    answer_12 = forms.CharField(required=False)
    answer_13 = forms.CharField(required=False)
    answer_14 = forms.CharField(required=False)
    answer_15 = forms.CharField(required=False)

    class Meta:
        model = SurveyQuestion
        exclude = ['allowed_answers',]
    
    def __init__(self, *args, **kwargs):    
        super(SurveyQuestionForm, self).__init__(*args, **kwargs)
        answers = self._decode_answers()
        for i in range(len(answers)):
            self.initial['answer_%d' % (i+1)] = answers[i]

    def _decode_answers(self):
        if self.instance and self.instance.allowed_answers not in EMPTY_VALUES:
            answers = json.loads(self.instance.allowed_answers)
            return answers
        return []
            
    def _encode_answers(self):
        answers = [
            (key, val) for key, val in self.cleaned_data.items() 
            if key.startswith('answer') and val != ''
        ]
        
        # sort by key
        answers = sorted(answers, key=lambda (key, val): key)
        
        # remove the keys
        answers = [val for (key, val) in answers]
        
        # encode to JSON        
        return json.dumps(answers)

    def save(self, *args, **kwargs):
        self.instance.allowed_answers = self._encode_answers()
        return super(SurveyQuestionForm, self).save(*args, **kwargs)       
    
    
class GroupSurveyQuestionAnswerForm(forms.ModelForm):
    default_error_messages = {
        'invalid': _(u'Enter a valid value.'),
    }
    
    def __init__(self, *args, **kwargs):
        super(GroupSurveyQuestionAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs['class'] += ' autocomplete'
        
    def clean_name(self):
        raise ValidationError('no')

    def clean(self):
        # Ensure that the entered answer is valid
        if not self.cleaned_data['survey_question'].is_valid_answer(
        self.cleaned_data['answer']):
            if 'answer' not in self._errors:
                self._errors['answer'] = self.error_class()
                
            msg = self.default_error_messages['invalid']
            self._errors['answer'].append(msg)
            del self.cleaned_data['answer']
            
        return self.cleaned_data