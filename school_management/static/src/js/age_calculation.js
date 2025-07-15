/** @odoo-module **/


$(document).ready(function () {
    $('#dob').on('change', function () {
        const dob = new Date($(this).val());
        const today = new Date();
        if (!isNaN(dob)) {
            let age = today.getFullYear() - dob.getFullYear();
            const monthDiff = today.getMonth() - dob.getMonth();

            if (
                monthDiff < 0 ||
                (monthDiff === 0 && today.getDate() < dob.getDate())
            ) {
                age--;
            }

            age = age >= 0 ? age : 0;
            $('#age').val(age);
            $('#age_hidden').val(age); // important for form submission
        } else {
            $('#age').val('');
            $('#age_hidden').val('');
        }
    });
});
