document.addEventListener('DOMContentLoaded', init);

function init() {
    console.log("Iniciando Galería Digital Neon Edition...");

    if (typeof artworkData === 'undefined') {
        console.error("No se han cargado los datos de las obras.");
        document.getElementById('gallery-container').innerHTML = "<p style='color:white; text-align:center; padding:2rem;'>Error: No se encontraron obras.</p>";
        return;
    }

    renderGrid(artworkData);
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
    const closeBtn = document.getElementById('close-hero');

    closeBtn.addEventListener('click', closeHero);
    overlay.addEventListener('click', (e) => {
        if (e.target === overlay) closeHero();
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

function closeHero() {
    const overlay = document.getElementById('hero-overlay');
    overlay.classList.remove('active');
    document.body.style.overflow = ''; // Unlock scroll
}

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
