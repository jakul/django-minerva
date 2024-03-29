from django.contrib import admin
from minerva.models import Fact, GroupFactValue, SurveyQuestion,\
    GroupSurveyQuestionAnswer, Group
from minerva.forms import SurveyQuestionForm, GroupSurveyQuestionAnswerForm
import json


class FactAdmin(admin.ModelAdmin):
    pass
#    def get_readonly_fields(self, obj=None):
#        if obj is not None:
#            return ['display_text',]
#        return []


class SurveyQuestionAdmin(admin.ModelAdmin):
    form = SurveyQuestionForm


#class GroupFactValueAdmin(admin.ModelAdmin):
#    pass
#

#class GroupSurveyQuestionAnswerAdmin(admin.ModelAdmin):
#    pass

class GroupFactValueInline(admin.TabularInline):
    model = GroupFactValue
    extra = 0


class GroupSurveyQuestionAnswerInline(admin.TabularInline):
    template = 'admin/minerva/groupsurveyquestionanswer/edit_inline/tabular.html'
    model = GroupSurveyQuestionAnswer
    extra = 0
    form = GroupSurveyQuestionAnswerForm


class GroupAdmin(admin.ModelAdmin):
    inlines = [GroupFactValueInline, GroupSurveyQuestionAnswerInline]
    template = 'admin/minerva/group/change_form.html'
    
    
    def change_view(self, *args, **kwargs):
        autocomplete_choices = {}
        for question_id, allowed_answers in \
        SurveyQuestion.objects.all().values_list('id', 'allowed_answers'):
            # allowed_answers is already encoded in JSON, so we need to decode
            # it to prevent doubled encoding
            autocomplete_choices[question_id] = json.loads(allowed_answers)
        
        extra_context = kwargs.pop('extra_context', {})
        extra_context['autocomplete_choices'] = json.dumps(autocomplete_choices)        
        kwargs['extra_context'] = extra_context
        return super(GroupAdmin, self).change_view(*args, **kwargs)

    
admin.site.register(Fact, FactAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
#admin.site.register(GroupFactValue, GroupFactValueAdmin)
#admin.site.register(GroupSurveyQuestionAnswer, GroupSurveyQuestionAnswerAdmin)
admin.site.register(Group, GroupAdmin)