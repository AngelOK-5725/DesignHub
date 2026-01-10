document.addEventListener('DOMContentLoaded', () => {
    const likeBtns = document.querySelectorAll('.like-btn');

    if (!likeBtns.length) {
        console.warn('Like button not found');
        return;
    }

    likeBtns.forEach(likeBtn => {
        likeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const designId = likeBtn.dataset.id;
            const containerCount = likeBtn.closest('.design-like');
            const countEl = containerCount ? containerCount.querySelector('.favorites-count') : document.querySelector('.favorites-count');

            console.log('Toggling favorite for design:', designId);

            // previous state and count for rollback
            const prevState = (likeBtn.classList.contains('active') || likeBtn.dataset.isFavorite === 'true');
            const prevCount = countEl ? (parseInt(countEl.textContent) || 0) : 0;
            const icon = likeBtn.querySelector('.heart-icon');
            const prevIconClass = icon ? (icon.classList.contains('fas') ? 'fas' : 'far') : null;

            // optimistic update
            const optimisticState = !prevState;
            likeBtn.dataset.isFavorite = optimisticState ? 'true' : 'false';
            likeBtn.setAttribute('aria-pressed', optimisticState ? 'true' : 'false');
            if (optimisticState) {
                likeBtn.classList.add('active');
                if (icon) { icon.classList.remove('far'); icon.classList.add('fas'); }
            } else {
                likeBtn.classList.remove('active');
                if (icon) { icon.classList.remove('fas'); icon.classList.add('far'); }
            }
            if (countEl) {
                countEl.textContent = optimisticState ? prevCount + 1 : Math.max(prevCount - 1, 0);
            }

            fetch(`/design/${designId}/toggle-favorite/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest',
                },
            })
            .then(response => {
                console.log('Response status:', response.status);
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                console.log('Response data:', data);
                // sync state with server
                likeBtn.dataset.isFavorite = data.is_favorite ? 'true' : 'false';
                likeBtn.setAttribute('aria-pressed', data.is_favorite ? 'true' : 'false');
                const iconAfter = likeBtn.querySelector('.heart-icon');
                if (data.is_favorite) {
                    likeBtn.classList.add('active');
                    if (iconAfter) { iconAfter.classList.remove('far'); iconAfter.classList.add('fas'); }
                } else {
                    likeBtn.classList.remove('active');
                    if (iconAfter) { iconAfter.classList.remove('fas'); iconAfter.classList.add('far'); }
                }
                if (countEl) countEl.textContent = data.favorites_count;
            })
            .catch(err => {
                // rollback optimistic UI
                console.error('Error toggling favorite:', err);
                likeBtn.dataset.isFavorite = prevState ? 'true' : 'false';
                likeBtn.setAttribute('aria-pressed', prevState ? 'true' : 'false');
                if (prevState) {
                    likeBtn.classList.add('active');
                } else {
                    likeBtn.classList.remove('active');
                }
                // restore icon class
                const iconRollback = likeBtn.querySelector('.heart-icon');
                if (iconRollback && prevIconClass) {
                    iconRollback.classList.remove(prevIconClass === 'fas' ? 'far' : 'fas');
                    iconRollback.classList.add(prevIconClass);
                }
                if (countEl) countEl.textContent = prevCount;
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            }
        });
    }
    return cookieValue;
}
