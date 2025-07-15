/** @odoo-module **/


$(document).ready(function() {
    $('#current_department_id').on('change', function() {
        var department_id = $(this).val();
        var $classSelect = $('#current_class_id');
        $classSelect.empty();
        $classSelect.append($('<option>', { value: '', text: 'Select Class' }));
        if (!department_id) {
            return;
        }
        $.getJSON('/getclasses/' + department_id).done(function(data) {
            if (data.classes && data.classes.length) {
                data.classes.forEach(function(cls) {
                    $classSelect.append($('<option>', { value: cls.id, text: cls.name }));
                });
            }
        }).fail(function() {
            alert('Failed to load classes for the selected department.');
        });
    });
});




