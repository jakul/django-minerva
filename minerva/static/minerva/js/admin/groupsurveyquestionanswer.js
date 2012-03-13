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
    	var availableTags = ['True', 'False']
    	                     
    	function setupAutocomplete(selector) {
    		var $inputs = $(selector);
    		console.log($inputs)
        	$inputs.autocomplete({
        		source: availableTags,
        		minLength: 0
        	});

        	$inputs.bind('dblclick.custom', function(event, ui) {
        		console.log('a', event.target)
                $(event.target).autocomplete('search', '')
            });
    	}
    	
    	// add the autocomplete to the existing rows
    	setupAutocomplete('#groupsurveyquestionanswer_set-group .dynamic-groupsurveyquestionanswer_set td.answer input');
    	
    	// ensure any new rows have the autocomplete
        $('#groupsurveyquestionanswer_set-group tr.add-row a').bind(
    	    'click.custom', //custom click event
    	    function(event) {
    	    	setupAutocomplete('#groupsurveyquestionanswer_set-group .dynamic-groupsurveyquestionanswer_set:last td.answer input');

	    	}
	    );
    });
})(django.jQuery);
