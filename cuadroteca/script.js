document.addEventListener('DOMContentLoaded', init);

function init() {
    console.log("Iniciando Galería Digital Neon Edition...");

    if (typeof artworkData === 'undefined') {
        console.error("No se han cargado los datos de las obras.");
        document.getElementById('gallery-container').innerHTML = "<p style='color:white; text-align:center; padding:2rem;'>Error: No se encontraron obras.</p>";
        return;
    }

    let dataToLoad = artworkData;

    // Check if there is a category filter in the URL
    const params = new URLSearchParams(window.location.search);
    const catFilter = params.get('category');

    if (catFilter && catFilter !== 'null' && catFilter !== '') {
        console.log("Filtrando galería digital por categoría:", catFilter);

        // Let's decode more safely just in case
        let targetCat = decodeURIComponent(catFilter);
        console.log("Categoría decodificada:", targetCat);

        // Exact match filter
        dataToLoad = artworkData.filter(art => art.category === targetCat);

        console.log("Obras encontradas para esta categoría:", dataToLoad.length);

        if (dataToLoad.length === 0) {
            alert(`No se encontraron obras para la categoría: "${targetCat}". Mostrando todas.`);
            dataToLoad = artworkData; // Fallback to all if category mismatch
        } else {
            // Update title to show collection name only if we found items
            const titleEl = document.querySelector('.neon-title');
            if (titleEl) {
                const cleanTitle = targetCat.replace(/^\d+/, '').replace(/_/g, ' ');
                titleEl.innerHTML = `COLECCIÓN <span class="highlight">${cleanTitle.toUpperCase()}</span>`;
            }
        }
    }

    renderGrid(dataToLoad);
    setupSearch();
    setupMusic();
    setupHero();
}

function renderGrid(data) {
    const container = document.getElementById('gallery-container');
    container.innerHTML = '';

    // Filtrar magic sellos si queremos (o mostrarlos aparte), de momento los incluimos todos o filtramos
    // Usaremos el mismo filtro que antes para coherencia:
    // const regularItems = data.filter(item => item.category !== 'SELLOS_MAGICOS');
    // O mejor, mostramos todo pero ordenado.

    // Group by Category
    const grouped = {};
    data.forEach(item => {
        // Normalizar categoría
        let cat = item.category || 'Otros';
        if (!grouped[cat]) grouped[cat] = [];
        grouped[cat].push(item);
    });

    const sortedCategories = Object.keys(grouped).sort();

    sortedCategories.forEach(category => {
        const items = grouped[category];

        // Section
        const section = document.createElement('section');
        section.className = 'category-section';

        // Title
        const title = document.createElement('h2');
        title.className = 'category-title';
        title.innerText = category;
        section.appendChild(title);

        // Grid
        const grid = document.createElement('div');
        grid.className = 'art-grid';

        items.forEach(item => {
            const card = createCard(item);
            grid.appendChild(card);
        });

        section.appendChild(grid);
        container.appendChild(section);
    });
}

function createCard(item) {
    const card = document.createElement('div');
    card.className = 'art-card';
    card.dataset.title = item.title.toLowerCase();

    // Image container
    const imgWrapper = document.createElement('div');
    imgWrapper.className = 'art-image-wrapper';

    // Lazy load image
    const img = document.createElement('img');
    img.src = `../${item.src}`;
    img.loading = "lazy";
    img.alt = item.title;

    imgWrapper.appendChild(img);

    // Info container
    const info = document.createElement('div');
    info.className = 'art-info';

    const title = document.createElement('div');
    title.className = 'art-title';
    title.innerText = item.title;

    const price = document.createElement('div');
    price.className = 'art-price';
    price.innerText = item.price;

    info.appendChild(title);
    info.appendChild(price);

    card.appendChild(imgWrapper);
    card.appendChild(info);

    // Event Click -> Hero
    card.addEventListener('click', () => openHero(item));

    return card;
}

// --- SEARCH ---
function setupSearch() {
    const input = document.getElementById('search-input');
    input.addEventListener('input', (e) => {
        const term = e.target.value.toLowerCase();
        const cards = document.querySelectorAll('.art-card');

        cards.forEach(card => {
            if (card.dataset.title.includes(term)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
    });
}


// --- HERO MODAL ---
function setupHero() {
    const overlay = document.getElementById('hero-overlay');

    // Also allow closing by clicking the overlay background
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) window.closeHero();
    });
}

function openHero(item) {
    const overlay = document.getElementById('hero-overlay');
    const heroImg = document.getElementById('hero-img');
    const heroTitle = document.getElementById('hero-title');
    const heroCat = document.getElementById('hero-category');
    const heroPrice = document.getElementById('hero-price');
    const heroDesc = document.getElementById('hero-desc');

    heroImg.src = `../${item.src}`;
    heroTitle.innerText = item.title;
    heroCat.innerText = item.category || 'Galería';
    heroPrice.innerText = item.price || 'Consultar';
    heroDesc.innerText = item.description || "Sin descripción disponible.";

    overlay.classList.add('active');
    document.body.style.overflow = 'hidden'; // Lock scroll
}

window.closeHero = function () {
    const overlay = document.getElementById('hero-overlay');
    if (overlay) overlay.classList.remove('active');
    document.body.style.overflow = ''; // Unlock scroll
    document.body.style.overflowY = 'auto'; // Ensure it can scroll again if needed
};

// --- ADD TO CART ---
document.getElementById('btn-comprar-cuadroteca').addEventListener('click', () => {
    // We already have the item details in the hero panel
    const heroTitle = document.getElementById('hero-title').innerText;
    const heroPrice = document.getElementById('hero-price').innerText;

    // We need the ID and exact path to thumbnail. We can extract it from the image src
    const imgSrc = document.getElementById('hero-img').getAttribute('src');

    // Match the src to artworkData to get the exact ID (since Cuadroteca currently doesn't store the ID cleanly in the DOM)
    const itemData = artworkData.find(art => `../${art.src}` === imgSrc || art.src.endsWith(imgSrc.split('/').pop()));

    if (itemData) {
        const itemObj = {
            id: itemData.id,
            title: heroTitle,
            price: heroPrice,
            thumb: itemData.src // Store path relative to root
        };

        if (typeof addToCart === 'function') {
            const added = addToCart(itemObj);
            if (added) {
                // Instantly redirect to checkout to improve user flow
                window.location.href = '../carrito.html';
            } else {
                alert('Esta obra ya está en tu carrito.');
            }
        } else {
            alert('Error: el sistema de carrito no está disponible.');
        }
    }
});

document.getElementById('btn-probador-cuadroteca').addEventListener('click', () => {
    // We need the ID and exact path to thumbnail for the visor
    const imgSrc = document.getElementById('hero-img').getAttribute('src');

    // Match the src to artworkData to get the exact details needed for the visor link
    const itemData = artworkData.find(art => `../${art.src}` === imgSrc || art.src.endsWith(imgSrc.split('/').pop()));

    if (itemData) {
        // Build the URL to bypass the landing, sending exactly the src expected (e.g. assets/03...)
        const viewerLink = `../visor/index.html?img=${encodeURIComponent(itemData.src)}&title=${encodeURIComponent(itemData.title)}&category=${encodeURIComponent(itemData.category)}&id=${itemData.id}`;
        window.location.href = viewerLink;
    } else {
        alert("Ocurrió un error al intentar abrir esta obra en el probador.");
    }
});

// --- MUSIC ---
function setupMusic() {
    const audio = document.getElementById('bgMusic');
    const musicBtn = document.getElementById('musicBtn');

    if (!audio || !musicBtn) return;

    // Same logic as before roughly
    musicBtn.addEventListener('click', () => {
        if (audio.paused) {
            audio.play().catch(e => console.error(e));
            musicBtn.innerText = "⏸ PAUSE";
            musicBtn.classList.add('playing');
        } else {
            audio.pause();
            musicBtn.innerText = "🎵 MÚSICA";
            musicBtn.classList.remove('playing');
        }
    });

    // Optional: Keep playlist logic if needed, but simplicity first.
    // If playlist is key, we can re-add the array logic.
    // Re-adding simple playlist logic for continuity
    const playlist = [
        "01Medianoche-en-la-Terraza.mp3",
        "All_around_if_you_want.mp3",
        "Black_and_grey_.mp3",
        "Close_Your_Feelings_Extended.mp3",
        "Groove_or_not.mp3",
        "Heaven_s_Glow.mp3",
        "Man_island_beach.mp3",
        "Meanwhile_I_Love_You.mp3",
        "Saxo_by_the_clouds.mp3",
        "Saxophone_Serenade.mp3",
        "Secret-of-Velvet.mp3",
        "Sharp-echoes.mp3",
        "Soft-corners.mp3",
        "Voices_for_dreams.mp3",
        "Woman_on_the_island_beach.mp3"
    ];
    let trackIdx = 0;
    const basePath = "../assets/music/";
    audio.src = basePath + playlist[0];

    audio.addEventListener('ended', () => {
        trackIdx = (trackIdx + 1) % playlist.length;
        audio.src = basePath + playlist[trackIdx];
        audio.play().catch(e => console.log(e));
    });
}
