document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather icons
    feather.replace();

    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Add ripple effect to buttons
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            let x = e.clientX - e.target.offsetLeft;
            let y = e.clientY - e.target.offsetTop;

            let ripple = document.createElement('span');
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.className = 'ripple';

            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });

    // Animate icons on hover
    document.querySelectorAll('[data-feather]').forEach(icon => {
        icon.addEventListener('mouseover', function() {
            this.style.transform = 'scale(1.2)';
        });
        icon.addEventListener('mouseout', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // Add page transition effects
    document.body.classList.add('fade-enter');
    requestAnimationFrame(() => {
        document.body.classList.add('fade-enter-active');
    });

    // Auto-dismiss alerts with animation
    var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            alert.style.animation = 'slideUp 0.5s ease forwards';
            setTimeout(() => {
                var bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 500);
        }, 5000);
    });

    // Form validation animation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();

                // Animate invalid fields
                form.querySelectorAll(':invalid').forEach(input => {
                    input.style.animation = 'shake 0.5s ease';
                    setTimeout(() => input.style.animation = '', 500);
                });
            }
            form.classList.add('was-validated');
        });
    });

    // Success message animation
    const showSuccess = () => {
        const successMessages = document.querySelectorAll('.alert-success');
        successMessages.forEach(message => {
            const checkmark = document.createElement('div');
            checkmark.className = 'success-checkmark';
            message.prepend(checkmark);
        });
    };

    // Call success animation if there are success messages
    if (document.querySelector('.alert-success')) {
        showSuccess();
    }
});