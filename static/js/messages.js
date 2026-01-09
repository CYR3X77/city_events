document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');

    alerts.forEach(alert => {
        // Появление
        setTimeout(() => {
            alert.classList.add('show-alert');
        }, 100);

        // Автоскрытие
        setTimeout(() => {
            alert.classList.add('hide-alert');
            setTimeout(() => alert.remove(), 400);
        }, 4000);

        // Закрытие по крестику
        const closeBtn = alert.querySelector('.btn-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.classList.add('hide-alert');
                setTimeout(() => alert.remove(), 400);
            });
        }
    });
});
