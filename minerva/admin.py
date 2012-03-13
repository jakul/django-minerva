from django.contrib import admin
from minerva.models import Fact, GroupFactValue, SurveyQuestion,\
    GroupSurveyQuestionAnswer, Group
from minerva.forms import SurveyQuestionForm, GroupSurveyQuestionAnswerForm


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

    
#    def get_media(self):
#        from django.conf import settings
#        static_url = getattr(settings, 'STATIC_URL')
#        form_media = self._media()
##        import ipdb
##        ipdb.set_trace()
#        form_media.add_js((static_url + '/minerva/js/admin/group.js',))
#        return form_media
#    media = property(get_media)
    
    
admin.site.register(Fact, FactAdmin)
admin.site.register(SurveyQuestion, SurveyQuestionAdmin)
#admin.site.register(GroupFactValue, GroupFactValueAdmin)
#admin.site.register(GroupSurveyQuestionAnswer, GroupSurveyQuestionAnswerAdmin)
admin.site.register(Group, GroupAdmin)