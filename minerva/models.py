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
    answer_1 = models.CharField(max_length=60, blank=True, null=True)
    answer_2 = models.CharField(max_length=60, blank=True, null=True)
    answer_3 = models.CharField(max_length=60, blank=True, null=True)
    answer_4 = models.CharField(max_length=60, blank=True, null=True)
    answer_5 = models.CharField(max_length=60, blank=True, null=True)
    answer_6 = models.CharField(max_length=60, blank=True, null=True)
    answer_7 = models.CharField(max_length=60, blank=True, null=True)
    answer_8 = models.CharField(max_length=60, blank=True, null=True)
    answer_9 = models.CharField(max_length=60, blank=True, null=True)
    answer_10 = models.CharField(max_length=60, blank=True, null=True)
    answer_11 = models.CharField(max_length=60, blank=True, null=True)
    answer_12 = models.CharField(max_length=60, blank=True, null=True)
    answer_13 = models.CharField(max_length=60, blank=True, null=True)
    answer_14 = models.CharField(max_length=60, blank=True, null=True)
    answer_15 = models.CharField(max_length=60, blank=True, null=True)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return self.display_text
    
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
             self.group.display_name, self.fact.display_text, self.value
        )
    
    
class GroupSurveyQuestionAnswer(models.Model):
    group = models.ForeignKey(to='Group')
    survey_question = models.ForeignKey(to=SurveyQuestion)
    answer = models.CharField(max_length=60)
    
    class Meta:
        unique_together = ('group', 'survey_question', 'answer')
        
    def __unicode__(self):
        return '%s: %s: %s' % (
             self.group.display_name, self.survey_question.display_text, self.answer
        )
        
    
class Group(models.Model):
    id = models.SlugField(
        primary_key=True, max_length=60, blank=False, editable=False
    )
    display_name = models.CharField(max_length=60)
    facts = models.ManyToManyField(Fact, through='GroupFactValue')
    survey_answers = models.ManyToManyField(
        SurveyQuestion, through='GroupSurveyQuestionAnswer'
    )
    
    def __unicode__(self):
        return self.display_name
    
    def save(self, *args, **kwargs):
        if self.id in (None, ''):
            self.id = slugify(self.display_name)
        return super(Group, self).save(*args, **kwargs)
    