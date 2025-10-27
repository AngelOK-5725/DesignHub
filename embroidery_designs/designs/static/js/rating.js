document.addEventListener('DOMContentLoaded', function() {
    // Обработка кликов по звездам
    document.querySelectorAll('.star-rating .star').forEach(star => {
        star.addEventListener('click', function() {
            const rating = this.getAttribute('data-rating');
            const designId = this.closest('.star-rating').getAttribute('data-design-id');
            
            // Отправляем оценку на сервер
            rateDesign(designId, rating);
        });
    });
    
    // Обработка наведения на звезды
    document.querySelectorAll('.star-rating').forEach(ratingContainer => {
        ratingContainer.addEventListener('mouseover', function(e) {
            if (e.target.classList.contains('star')) {
                const rating = e.target.getAttribute('data-rating');
                highlightStars(this, rating);
            }
        });
        
        ratingContainer.addEventListener('mouseout', function() {
            resetStars(this);
        });
    });
});

function rateDesign(designId, rating) {
    const formData = new FormData();
    formData.append('rating', rating);
    formData.append('csrfmiddlewaretoken', getCookie('csrftoken'));
    
    fetch(`/design/${designId}/rate/`, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateRatingDisplay(designId, data);
            showNotification('Спасибо за вашу оценку!', 'success');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showNotification('Ошибка при оценке', 'error');
    });
}

function highlightStars(container, rating) {
    container.querySelectorAll('.star').forEach((star, index) => {
        if (index < rating) {
            star.classList.add('hover');
        } else {
            star.classList.remove('hover');
        }
    });
}

function resetStars(container) {
    container.querySelectorAll('.star').forEach(star => {
        star.classList.remove('hover');
    });
}

function updateRatingDisplay(designId, data) {
    const ratingContainer = document.querySelector(`.star-rating[data-design-id="${designId}"]`);
    if (ratingContainer) {
        // Обновляем отображение звезд
        ratingContainer.querySelectorAll('.star').forEach((star, index) => {
            if (index < data.average_rating) {
                star.classList.add('filled');
            } else {
                star.classList.remove('filled');
            }
        });
        
        // Обновляем текстовую информацию
        const textElement = ratingContainer.nextElementSibling;
        if (textElement) {
            textElement.textContent = `${data.average_rating} (${data.rating_count} оценок)`;
        }
    }
}

// Вспомогательная функция для получения CSRF токена
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

function showNotification(message, type) {
    // Простая реализация уведомления
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}