// =============================================
// CoffeeTrack - JavaScript Principal
// =============================================

document.addEventListener('DOMContentLoaded', function() {
    // Auto-cerrar toasts después de 4 segundos
    const toasts = document.querySelectorAll('.toast');
    toasts.forEach(toast => {
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    });

    // Confirmación de eliminación
    document.querySelectorAll('[data-confirm]').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Formateo de precios
    document.querySelectorAll('.format-price').forEach(el => {
        const val = parseFloat(el.textContent);
        if (!isNaN(val)) {
            el.textContent = '$' + val.toFixed(2);
        }
    });
});