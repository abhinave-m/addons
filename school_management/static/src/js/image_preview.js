/** @odoo-module **/


document.addEventListener('DOMContentLoaded', function () {
    const imageInput = document.querySelector('#student_image');
    const previewImg = document.querySelector('#student_image_preview');

    if (imageInput && previewImg) {
        imageInput.addEventListener('change', function () {
            const file = this.files[0];
            if (file && file.type.startsWith('image/')) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});
