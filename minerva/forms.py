from minerva.models import SurveyQuestion
from django import forms
import json
from django.core.validators import EMPTY_VALUES
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

_TYPE_OF_ANSWER_CHOICES = (
    ('', '---------'),
    ('multiple_choice_single_answer', 'Multiple Choice (single answer)'),
    ('multiple_choice_multiple_answer', 'Multiple Choice (multiple answer)'),
    ('boolean', 'Yes or No'),
    ('integer_range', 'Integer Range'),
)

class _MyModelForm(forms.ModelForm):
        
    def add_error(self, field, msg):
        if field not in self._errors:
            self._errors[field] = self.error_class()
            
        self._errors[field].append(msg)
        try:
            del self.cleaned_data[field]
        except KeyError:
            # item not in cleaned_data yet
            pass

class SurveyQuestionForm(_MyModelForm):
    type_of_answer = forms.ChoiceField(choices=_TYPE_OF_ANSWER_CHOICES)

    class Meta:
        model = SurveyQuestion
        
    def integer_range_valid(self, min_value, max_value):
        if max_value <= min_value:
            return False
        return True
    
    def fields_have_value(self, *fieldnames):
        missing_field = False
        for fieldname in fieldnames:
            value = self.cleaned_data.get(fieldname, '')
            if value in EMPTY_VALUES:
                self.add_error(
                    fieldname, self.fields[fieldname].error_messages['required']
                )
                missing_field = True
        return not missing_field
    
    def clean(self):
        type_of_answer = self.cleaned_data.get('type_of_answer', '')
        if type_of_answer.startswith('multiple_choice'):
            
            # Check that the minimum number of values has been provided
            for field in ('answer_1', 'answer_2'):
                value = self.cleaned_data.get(field, '')
                # Check that a value has been provided
                if value in EMPTY_VALUES:
                    self.add_error(
                        field, self.fields[field].error_messages['required']
                    )
            
        elif type_of_answer == 'integer_range':
            # Check that a value has been provided
            all_fields_present = self.fields_have_value('min_value', 'max_value')
            if not all_fields_present:
                return self.cleaned_data
                    
            # Ensure a valid range has been entered
            # TODO: validate min value is >= 0
            min_value = self.cleaned_data.get('min_value', '')
            max_value = self.cleaned_data.get('max_value', '')
            if not self.integer_range_valid(min_value, max_value):
                self.add_error('min_value', 'Enter a valid range')
                self.add_error('max_value', 'Enter a valid range')
                
        return self.cleaned_data

    def save(self, *args, **kwargs):
        return super(SurveyQuestionForm, self).save(*args, **kwargs)       
    
    
class GroupSurveyQuestionAnswerForm(_MyModelForm):
    default_error_messages = {
        'invalid': _(u'Enter a valid value.'),
    }
    
    def __init__(self, *args, **kwargs):
        super(GroupSurveyQuestionAnswerForm, self).__init__(*args, **kwargs)
        self.fields['answer'].widget.attrs['class'] += ' autocomplete'
    
    def clean(self):
        # Ensure that the entered answer is valid
        if not self.cleaned_data['survey_question'].is_valid_answer(
        self.cleaned_data['answer']):
            msg = self.default_error_messages['invalid']
            self.add_error('answer', msg)
            
        return self.cleaned_data