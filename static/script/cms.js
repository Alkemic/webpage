$(document).ready(function(){
    $('input[name=from_date], input[name=to_date]').datepicker({format: "yyyy-mm-dd"});
    $('input,select,textarea').not('[type=submit]').jqBootstrapValidation({
        filter: function(){
            return $(this).is(':visible');
        }
    });
});
