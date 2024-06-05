document.addEventListener('DOMContentLoaded', function () {
    const icons = document.querySelectorAll('.sidebar-icon');

    function loadContent(tabId) {
        fetch(`/${tabId}`)
            .then(response => response.text())
            .then(html => {
                document.getElementById('main-content').innerHTML = html;
            })
            .catch(error => console.warn('Error loading tab content:', error));
    }

    function activateTab(tabId) {
        icons.forEach(i => {
            i.classList.remove('active');
            const lordIcon = i.querySelector('lord-icon');
            const label = i.querySelector('.icon-label');
            if (lordIcon) {
                lordIcon.setAttribute('colors', 'primary:#121331,secondary:#08a88a');
            }
            if (label) {
                label.classList.remove('active');
                label.style.color = '#6b7280'; // Tailwind's gray-600
            }
        });

        const activeIcon = document.querySelector(`#${tabId}-tab`);
        if (activeIcon) {
            activeIcon.classList.add('active');
            const activeLordIcon = activeIcon.querySelector('lord-icon');
            const activeLabel = activeIcon.querySelector('.icon-label');
            if (activeLordIcon) {
                activeLordIcon.setAttribute('colors', 'primary:#1d4ed8,secondary:#e0f2fe');
            }
            if (activeLabel) {
                activeLabel.classList.add('active');
                activeLabel.style.color = '#1d4ed8'; // Tailwind's blue-700
            }
        }

        loadContent(tabId);
    }

    icons.forEach(icon => {
        icon.addEventListener('click', function () {
            const tabId = this.getAttribute('data-tab');
            activateTab(tabId);
        });
    });

    // Activate the first tab by default
    activateTab('summary');
});
