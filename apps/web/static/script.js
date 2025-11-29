document.getElementById('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const urlInput = document.getElementById('url-input').value;
    const btn = document.getElementById('login-btn');
    const errorMsg = document.getElementById('error-msg');

    if (!urlInput) {
        errorMsg.innerText = 'Please paste the URL first.';
        errorMsg.style.display = 'block';
        return;
    }

    btn.disabled = true;
    btn.innerText = 'Verifying Token...';
    errorMsg.style.display = 'none';

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: urlInput })
        });

        const data = await response.json();

        if (response.ok) {
            document.getElementById('login-section').classList.add('hidden');
            document.getElementById('store-section').classList.remove('hidden');
            loadStore();
        } else {
            errorMsg.innerText = data.detail || 'Login failed';
            errorMsg.style.display = 'block';
            btn.disabled = false;
            btn.innerText = 'Fetch My Store';
        }
    } catch (err) {
        errorMsg.innerText = 'Network error';
        errorMsg.style.display = 'block';
        btn.disabled = false;
        btn.innerText = 'Fetch My Store';
    }
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
