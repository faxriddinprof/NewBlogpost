document.addEventListener('DOMContentLoaded', () => {
    const input     = document.getElementById('search-input');
    const clearBtn  = document.getElementById('clear-search');
    const container = document.getElementById('article-container');

    const ajaxUrl = "/articles/";

    if (!input || !container || !clearBtn) return;

    let timer = null;

    const performSearch = (query = '') => {
        fetch(`${ajaxUrl}?q=${encodeURIComponent(query)}`, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            container.innerHTML = data.html;
        })
        .catch(err => console.error('❌ Qidiruv xatosi:', err));
    };

    input.addEventListener('input', () => {
        clearBtn.style.display = input.value ? 'block' : 'none';

        clearTimeout(timer);
        timer = setTimeout(() => {
            const query = input.value.trim();
            performSearch(query);
        }, 300);
    });

    clearBtn.addEventListener('click', () => {
        input.value = '';
        clearBtn.style.display = 'none';
        performSearch('');
    });
});
