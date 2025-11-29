function startLogin() {
    const btn = document.getElementById('login-btn');
    const errorMsg = document.getElementById('error-msg');

    btn.disabled = true;
    btn.innerText = 'Waiting for Login...';
    errorMsg.style.display = 'none';

    // Call Python backend via pywebview
    if (window.pywebview) {
        window.pywebview.api.start_login().catch(err => {
            errorMsg.innerText = "Error starting login: " + err;
            errorMsg.style.display = 'block';
            btn.disabled = false;
            btn.innerText = 'Login with Riot';
        });
    } else {
        errorMsg.innerText = "Desktop API not found. Are you running in the app?";
        errorMsg.style.display = 'block';
        btn.disabled = false;
        btn.innerText = 'Login with Riot';
    }
}

// Listen for login success from Python
window.addEventListener('pywebviewready', function () {
    // Ready
});

// Custom event dispatched from Python
window.addEventListener('login-success', function () {
    document.getElementById('login-section').classList.add('hidden');
    document.getElementById('store-section').classList.remove('hidden');
    loadStore();
});

async function loadStore() {
    const grid = document.getElementById('store-grid');
    grid.innerHTML = '<p>Loading store...</p>';

    try {
        const response = await fetch('/api/store');
        const data = await response.json();

        if (response.ok) {
            grid.innerHTML = '';
            if (data.items.length === 0) {
                grid.innerHTML = '<p>No items found or store is empty.</p>';
                return;
            }
            data.items.forEach(item => {
                const el = document.createElement('div');
                el.className = 'card store-item';
                const img = document.createElement('img');
                img.src = item.icon;
                img.alt = item.name;
                img.className = 'skin-icon';
                el.appendChild(img);

                const nameDiv = document.createElement('div');
                nameDiv.className = 'name';
                nameDiv.textContent = item.name;
                el.appendChild(nameDiv);

                const priceDiv = document.createElement('div');
                priceDiv.className = 'price';

                const vpIcon = document.createElement('img');
                vpIcon.src = "https://media.valorant-api.com/currencies/85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741/displayicon.png";
                vpIcon.className = 'vp-icon';
                vpIcon.alt = "VP";
                priceDiv.appendChild(vpIcon);

                const priceText = document.createTextNode(" " + item.price);
                priceDiv.appendChild(priceText);

                el.appendChild(priceDiv);
                grid.appendChild(el);
            });
        } else {
            grid.innerHTML = '<p>Failed to load store.</p>';
        }
    } catch (err) {
        grid.innerHTML = '<p>Error loading store.</p>';
    }
}
