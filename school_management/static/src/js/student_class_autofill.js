/** @odoo-module **/
import publicWidget from "@web/legacy/js/public/public_widget";


publicWidget.registry.StudentClassAutofill = publicWidget.Widget.extend({
    selector: 'form[action="/school_management/leave/submit"]',

    start: function () {
        var self = this;
        this.$el.find('#student_id').on('change', function () {
            const studentId = $(this).val();
            if (studentId) {
                self._fetchClassId(studentId);
            } else {
                $('#class_id').val('');
            }
        });
    },

    _fetchClassId: function (studentId) {
        var self = this;
        const $classInput = $('#class_id');
        $classInput.prop('disabled', true);

        $.ajax({
            url: '/school_management/get_class',
            type: 'POST',
            contentType: 'application/json',
            dataType: 'json',
            data: JSON.stringify({
                jsonrpc: "2.0",
                method: "call",
                params: { student_id: studentId },
                id: new Date().getTime(),
            }),
            success: function (response) {
                $classInput.prop('disabled', false);
                var className = response.result && response.result.class_name;
                if (className) {
                    $classInput.val(className);
                } else {
                    $classInput.val('');
                }
            },
            error: function (xhr, status, error) {
                $classInput.prop('disabled', false);
                console.error('Failed to fetch class:', status, error);
            }
        });
    },
});
