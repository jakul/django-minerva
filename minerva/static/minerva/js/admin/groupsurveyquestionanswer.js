/**
 * We add another click handler to the 'Add another Group Survey Question Answer' link,
 * which must be executed after the existing handler (which creates the row).
 * 
 * We have to bind to a custom event, because the existing handler (created by
 * `django.jQuery.formset`) returns `false`, which prevents this handler from
 * executing if this handler is bound to the `click` event.
 * 
 */


(function($) {
    $(document).ready(function($) {
    	
    	function setupAutocomplete(selector) {
    		$(selector).each(function(i, el){
    			var $tr = $(el);
    			var $answer = $('td.answer input', $tr)
    			var $question = $('td.survey_question select', $tr)
    			var autocompleteOptions = [];
    			var selectedQuestionId = $('td.survey_question select', $tr).val();

    			if (selectedQuestionId != "") {
    				autocompleteOptions = Onzo.GroupSurveyQuestionAnswer.autoCompleteChoices[selectedQuestionId]	
    			}
    			
    			$answer.autocomplete({
            		source: autocompleteOptions,
            		minLength: 0
            	});
            	$answer.bind('dblclick.custom', function(event, ui) {
                    $(event.target).autocomplete('search', '')
                });
            	$question.bind('change', function(event, ui) {
            		$answer.autocomplete('destroy')
            		setupAutocomplete($tr);
                });
    			
    		});
    	}
    	
    	// add the autocomplete to the existing rows
    	setupAutocomplete('#groupsurveyquestionanswer_set-group tr.dynamic-groupsurveyquestionanswer_set');
    	
    	// ensure any new rows have the autocomplete
        $('#groupsurveyquestionanswer_set-group tr.add-row a').bind(
    	    'click.custom', //custom click event
    	    function(event) {
    	    	setupAutocomplete('#groupsurveyquestionanswer_set-group tr.dynamic-groupsurveyquestionanswer_set:visible:last');
	    	}
	    );
    });
})(django.jQuery);
