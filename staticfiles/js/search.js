document.addEventListener('DOMContentLoaded', () => {
    const input     = document.getElementById('search-input');
    const clearBtn  = document.getElementById('clear-search');
    const container = document.getElementById('article-container');

    const ajaxUrl = "/articles/";

    if (!input || !container || !clearBtn) return;

    let timer = null;

    input.addEventListener('input', () => {
        clearBtn.style.display = input.value ? 'block' : 'none';

        clearTimeout(timer);
        timer = setTimeout(() => {
            const query = input.value.trim();
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
        }, 300);
    });

    clearBtn.addEventListener('click', () => {
        input.value = '';
        clearBtn.style.display = 'none';

        fetch(ajaxUrl, {
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        })
        .then(res => res.json())
        .then(data => {
            container.innerHTML = data.html;
        })
        .catch(err => console.error('❌ Qayta yuklash xatosi:', err));
    });
});
