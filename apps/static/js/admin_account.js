document.addEventListener('DOMContentLoaded', (event) => {
    let addButtons = document.querySelectorAll('.btn__add');
    let subButtons = document.querySelectorAll('.btn__sub');
    let selectElements = document.querySelectorAll('.role');

    addButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            let userId = this.getAttribute('data-user-id');
            let selectElement = Array.from(selectElements).find(select => select.getAttribute('data-user-id') === userId);

            if (selectElement) {
                let selectedRole = selectElement.value;
                let href = this.getAttribute('href');
                let finalUrl = href.replace('ROLE_NAME', encodeURIComponent(selectedRole));

                this.setAttribute('href', finalUrl);
            }
        });
    });
    subButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            let userId = this.getAttribute('data-user-id');
            let selectElement = Array.from(selectElements).find(select => select.getAttribute('data-user-id') === userId);

            if (selectElement) {
                let selectedRole = selectElement.value;
                let href = this.getAttribute('href');
                let finalUrl = href.replace('ROLE_NAME', encodeURIComponent(selectedRole));

                this.setAttribute('href', finalUrl);
            }
        });
    });
});
