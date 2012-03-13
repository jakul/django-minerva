from django.db import models
from django.template.defaultfilters import slugify
import json

class Fact(models.Model):
    id = models.SlugField(
        primary_key=True, max_length=60, blank=False, editable=False
    )
    display_text = models.CharField(max_length=60)
    
    def __unicode__(self):
        return self.display_text
    
    def save(self, *args, **kwargs):
        if self.id in (None, ''):
            self.id = slugify(self.display_text)
        return super(Fact, self).save(*args, **kwargs)
    

class SurveyQuestion(models.Model):
    id = models.SlugField(
        primary_key=True, max_length=60, blank=False, editable=False
    )
    display_text = models.CharField(max_length=60)
    type_of_answer = models.CharField(max_length=60)
    allowed_answers = models.CharField(max_length=8000)
    
    def __unicode__(self):
        return self.id
    
    def save(self, *args, **kwargs):
        if self.id in (None, ''):
            self.id = slugify(self.display_text)
        return super(SurveyQuestion, self).save(*args, **kwargs)
    
    @property
    def _allowed_answers_list(self):
        return json.loads(self.allowed_answers)
    
    def is_valid_answer(self, answer):
        """
        Check if the given answer is valid
        """
        return answer in self._allowed_answers_list
    
    
class GroupFactValue(models.Model):
    group = models.ForeignKey(to='Group')
    fact = models.ForeignKey(to=Fact)
    value = models.CharField(max_length=60)
    
    class Meta:
        unique_together = ('group', 'fact')
        
    def __unicode__(self):
        return '%s: %s: %s' % (
             self.group.name, self.fact.display_text, self.value
        )
    
    
class GroupSurveyQuestionAnswer(models.Model):
    group = models.ForeignKey(to='Group')
    survey_question = models.ForeignKey(to=SurveyQuestion)
    answer = models.CharField(max_length=60)
    
    class Meta:
        unique_together = ('group', 'survey_question', 'answer')
        
    def __unicode__(self):
        return '%s: %s: %s' % (
             self.group.name, self.survey_question.display_text, self.answer
        )
        
    
class Group(models.Model):
    name = models.CharField(max_length=60, primary_key=True)
    facts = models.ManyToManyField(Fact, through='GroupFactValue')
    survey_answers = models.ManyToManyField(
        SurveyQuestion, through='GroupSurveyQuestionAnswer'
    )
    
    def __unicode__(self):
        return self.name
    