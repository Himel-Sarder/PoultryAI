// Auto-dismiss alerts
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        document.querySelectorAll('.alert:not(.alert-permanent)').forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
});

// CSRF Token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrfToken = getCookie('csrftoken');

// Like post functionality
function likePost(postId) {
    fetch(`/social/post/${postId}/like/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrfToken, 'Content-Type': 'application/json' },
    })
    .then(r => r.json())
    .then(data => {
        const btn = document.getElementById(`like-btn-${postId}`);
        const count = document.getElementById(`like-count-${postId}`);
        if (btn) btn.classList.toggle('text-success', data.liked);
        if (count) count.textContent = data.count;
    });
}

// Add comment
function addComment(postId) {
    const input = document.getElementById(`comment-input-${postId}`);
    if (!input || !input.value.trim()) return;
    const formData = new FormData();
    formData.append('comment', input.value.trim());
    formData.append('csrfmiddlewaretoken', csrfToken);
    fetch(`/social/post/${postId}/comment/`, { method: 'POST', body: formData })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            const list = document.getElementById(`comments-${postId}`);
            if (list) {
                const div = document.createElement('div');
                div.className = 'comment-item d-flex gap-2 mb-2';
                div.innerHTML = `<small class="fw-bold">${data.user}:</small><small>${data.comment}</small>`;
                list.appendChild(div);
            }
            input.value = '';
            const countEl = document.getElementById(`comment-count-${postId}`);
            if (countEl) countEl.textContent = data.count;
        }
    });
}

// Validate coupon
function validateCoupon() {
    const code = document.getElementById('coupon_code')?.value?.trim();
    const amount = document.getElementById('cart_total')?.value || 0;
    if (!code) return;
    const formData = new FormData();
    formData.append('code', code);
    formData.append('amount', amount);
    formData.append('csrfmiddlewaretoken', csrfToken);
    fetch('/products/validate-coupon/', { method: 'POST', body: formData })
    .then(r => r.json())
    .then(data => {
        const msg = document.getElementById('coupon-message');
        if (msg) {
            msg.textContent = data.message;
            msg.className = data.valid ? 'text-success small mt-1' : 'text-danger small mt-1';
        }
        if (data.valid) {
            const discount = document.getElementById('discount_amount');
            const total = document.getElementById('final_total');
            if (discount) discount.textContent = '৳' + data.discount;
            if (total) {
                const sub = parseFloat(document.getElementById('cart_total')?.value || 0);
                total.textContent = '৳' + (sub - data.discount).toFixed(2);
            }
            const hiddenDiscount = document.getElementById('hidden_discount');
            if (hiddenDiscount) hiddenDiscount.value = data.discount;
        }
    });
}
