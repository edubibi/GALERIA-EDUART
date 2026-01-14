// Referencias al DOM
const shelfContainer = document.getElementById('shelf-container');
const resetBtn = document.getElementById('reset-view-btn');
const searchInput = document.getElementById('search-input');
const libraryContainer = document.querySelector('.library-container');
const scene = document.querySelector('.scene');
const heroOverlay = document.getElementById('hero-overlay');

// Estado
let isDragging = false;
let startX, startY;
let currentX = 0;
let currentY = 0;
let activeBookOriginal = null; // Referencia al libro original oculto
let isHeroMode = false;

function init() {
    console.log("Iniciando Biblioteca 3D V9 (Hero Overlay)...");

    if (typeof artworkData === 'undefined') {
        console.error("No se han cargado los datos de las obras.");
        shelfContainer.innerHTML = "<p style='color:white; text-align:center;'>Error: No se encontraron obras.</p>";
        return;
    }

    renderMagicDesk(artworkData);
    renderLibraryByCategories(artworkData);
    setupEvents();
    setupPanNavigation();
    setupHeroOverlayParams();
    setupMusic();
}

function renderLibraryByCategories(data) {
    shelfContainer.innerHTML = '';
    const booksPerShelf = 20;

    // exclude sellos magic from shelves
    const regularItems = data.filter(item => item.category !== 'SELLOS_MAGICOS');

    const groupedData = {};
    regularItems.forEach(item => {
        const cat = item.category || 'Otros';
        if (!groupedData[cat]) groupedData[cat] = [];
        groupedData[cat].push(item);
    });

    Object.keys(groupedData).sort().forEach(category => {
        const items = groupedData[category];
        let currentShelf = createShelf();

        const label = document.createElement('div');
        label.className = 'shelf-label';
        label.innerText = category;
        currentShelf.appendChild(label);

        const spacer = document.createElement('div');
        spacer.style.width = '100px';
        currentShelf.appendChild(spacer);

        shelfContainer.appendChild(currentShelf);

        let countOnShelf = 0;

        items.forEach((artwork) => {
            if (countOnShelf >= booksPerShelf) {
                currentShelf = createShelf();
                shelfContainer.appendChild(currentShelf);
                countOnShelf = 0;

                const spacerSmall = document.createElement('div');
                spacerSmall.style.width = '40px';
                currentShelf.appendChild(spacerSmall);
            }

            const book = createBook(artwork);
            currentShelf.appendChild(book);
            countOnShelf++;
        });
    });
}

function createShelf() {
    const shelf = document.createElement('div');
    shelf.className = 'shelf';
    return shelf;
}

function createBook(artwork) {
    const wrapper = document.createElement('div');
    wrapper.className = 'book-wrapper';
    wrapper.dataset.id = artwork.id;
    wrapper.dataset.title = artwork.title.toLowerCase();

    // Guardamos datos para reconstruir en modo héroe
    wrapper.dataset.src = artwork.src;
    wrapper.dataset.price = artwork.price;
    wrapper.dataset.fullTitle = artwork.title;

    const spine = document.createElement('div');
    spine.className = 'spine';
    spine.innerText = artwork.title.substring(0, 20) + (artwork.title.length > 20 ? '...' : '');
    const hue = Math.floor(Math.random() * 40) + 10;
    spine.style.backgroundColor = `hsl(${hue}, 40%, 30%)`;

    const cover = document.createElement('div');
    cover.className = 'cover';
    const imagePath = `../${artwork.src}`;
    cover.style.backgroundImage = `url('${imagePath}')`;

    // Info oculta en el cover (se verá al abrir)
    const info = document.createElement('div');
    info.className = 'cover-info';
    info.innerHTML = `<strong>${artwork.title}</strong><br>${artwork.price} €`;

    cover.appendChild(info);
    wrapper.appendChild(spine);
    wrapper.appendChild(cover);

    wrapper.addEventListener('click', (e) => {
        e.stopPropagation();
        if (!isDragging && !isHeroMode) {
            activateHeroMode(wrapper);
        }
    });

    return wrapper;
}

// --- MAGICAL BOOK LOGIC ---
// --- MAGIC DESK & BOOK LOGIC ---
function renderMagicDesk(data) {
    // Filtrar los sellos
    const sellosItems = data.filter(item => item.category === 'SELLOS_MAGICOS');
    if (sellosItems.length === 0) return;

    // Crear el contenedor de "Escritorio" fijo en pantalla
    const deskContainer = document.createElement('div');
    deskContainer.id = 'magic-desk';
    document.body.appendChild(deskContainer);

    // Crear el Libro Mágico
    const magicBook = createMagicBook3D(sellosItems);
    deskContainer.appendChild(magicBook);
}

function createMagicBook3D(items) {
    const container = document.createElement('div');
    container.className = 'magic-book-container';

    // Structure
    const book = document.createElement('div');
    book.className = 'magic-book-3d';

    // Parts
    const front = document.createElement('div');
    front.className = 'magic-cover front';
    front.innerHTML = `<div class="magic-cover-title">GRIMOIRE</div>`;
    // Cover image background is in CSS or set here:
    front.style.backgroundImage = 'url("../assets/SELLOS_MAGICOS/cover_book.png")';

    const back = document.createElement('div');
    back.className = 'magic-cover back';

    const spine = document.createElement('div');
    spine.className = 'magic-spine-3d';

    const pages = document.createElement('div');
    pages.className = 'magic-pages';

    // Assemble
    book.appendChild(back);
    book.appendChild(pages);
    book.appendChild(spine);
    book.appendChild(front);
    container.appendChild(book);

    // Interaction
    container.addEventListener('click', (e) => {
        console.log("Magic Book Clicked!");
        e.stopPropagation(); // Prevent affecting scenes behind

        if (container.classList.contains('open')) {
            console.log("Book is already open, ignoring.");
            return;
        }

        container.classList.add('open');

        // Timer to show content matching CSS transition
        setTimeout(() => {
            openMagicGrimoireContent(items);
        }, 1000);
    });

    return container;
}

// --- OPEN BOOK UI LOGIC ---

function openMagicGrimoireContent(items) {
    const overlay = document.getElementById('hero-overlay');
    overlay.innerHTML = '';
    overlay.classList.add('active');

    // Container for the Open Book View
    const bookView = document.createElement('div');
    bookView.className = 'open-book-view';

    // The Book Spread (Left and Right Pages)
    const spread = document.createElement('div');
    spread.className = 'book-spread';

    const leftPage = document.createElement('div');
    leftPage.className = 'book-page left';

    const rightPage = document.createElement('div');
    rightPage.className = 'book-page right';

    spread.appendChild(leftPage);
    spread.appendChild(rightPage);
    bookView.appendChild(spread);

    // Close Button (Outside the book)
    const closeBtn = document.createElement('button');
    closeBtn.className = 'book-close-btn';
    closeBtn.innerText = 'Cerrar Libro';
    closeBtn.onclick = () => {
        overlay.classList.remove('active');
        setTimeout(() => overlay.innerHTML = '', 500);
        document.querySelector('#magic-desk .magic-book-container')?.classList.remove('open');
    };
    bookView.appendChild(closeBtn);

    overlay.appendChild(bookView);

    // Initialize with Index
    renderBookIndex(items, leftPage, rightPage);
}

function renderBookIndex(items, leftPage, rightPage) {
    // 1. Categorizar items
    const categories = {
        "Reyes y Personajes": [],
        "Monumentos": [],
        "Arte y Cultura": [],
        "Ciencia y Técnica": [],
        "España y América": [],
        "Otros": []
    };

    items.forEach((item, originalIndex) => {
        const cat = getStampCategory(item.title);
        // Guardamos el índice original para el onclick
        categories[cat].push({ ...item, originalIndex });
    });

    // LEFT PAGE: Title / Frontispiece
    leftPage.innerHTML = `
        <div class="page-content frontispiece">
            <h1 class="book-main-title">Grimorio<br>de<br>Sellos</h1>
            <div class="decorative-line"></div>
            <p class="book-subtitle">Colección Mágica</p>
            <div class="decorative-line"></div>
            <p style="text-align:center; font-style:italic; font-size:0.9rem; margin-top:20px;">
                "Un viaje a través de la historia,<br>el arte y el alma de España."
            </p>
        </div>
    `;

    // RIGHT PAGE: The Categorized Index List
    let indexHtml = `<div class="page-content index-page">
        <h2>ÍNDICE TEMÁTICO</h2>
        <div class="index-scroll-container">`;

    // Renderizar por orden de categorías definido
    for (const [catName, catItems] of Object.entries(categories)) {
        if (catItems.length === 0) continue;

        indexHtml += `<h3 class="index-category-title">${catName}</h3>`;
        indexHtml += `<ul class="chapter-list">`;

        catItems.forEach(item => {
            indexHtml += `<li data-idx="${item.originalIndex}">${item.title}</li>`;
        });

        indexHtml += `</ul>`;
    }

    indexHtml += `</div></div>`;
    rightPage.innerHTML = indexHtml;

    // Add Click Events
    const listItems = rightPage.querySelectorAll('li');
    listItems.forEach(li => {
        li.addEventListener('click', () => {
            const idx = parseInt(li.dataset.idx);
            renderStampPage(items[idx], items, leftPage, rightPage);
        });
    });
}

function getStampCategory(title) {
    const t = title.toLowerCase();

    // Reyes y Personajes Históricos
    if (t.includes('rey') || t.includes('reina') || t.includes('isabel') || t.includes('fernando') ||
        t.includes('carlos') || t.includes('franco') || t.includes('cid') || t.includes('pizarro') ||
        t.includes('colon') || t.includes('dictador') || t.includes('sofia') || t.includes('juan carlos') ||
        t.includes('san martin')) {
        return "Reyes y Personajes";
    }

    // Ciencia y Técnica
    if (t.includes('cierva') || t.includes('cajal') || t.includes('inventos') || t.includes('ciencia')) {
        return "Ciencia y Técnica";
    }

    // Arte y Cultura
    if (t.includes('cervantes') || t.includes('velazquez') || t.includes('lope de vega') ||
        t.includes('quijote') || t.includes('goya') || t.includes('arte') || t.includes('pintura')) {
        return "Arte y Cultura";
    }

    // Monumentos
    if (t.includes('catedral') || t.includes('acueducto') || t.includes('arco') || t.includes('monasterio') ||
        t.includes('sagrada') || t.includes('familia') || t.includes('escorial') || t.includes('castillo') ||
        t.includes('compostela')) {
        return "Monumentos";
    }

    // España y América (Si no cayó en personajes)
    if (t.includes('america') || t.includes('hispanidad')) {
        return "España y América";
    }

    // Otros (Fauna, Constitucion, etc.)
    return "Otros";
}

function renderStampPage(item, allItems, leftPage, rightPage) {
    // Animation/Transition effect could go here

    // LEFT PAGE: The Image
    leftPage.innerHTML = `
        <div class="page-content stamp-display">
            <div class="stamp-frame">
                <img src="../${item.src}" alt="${item.title}">
            </div>
            <div class="stamp-caption">${item.title}</div>
        </div>
    `;

    // RIGHT PAGE: Details & Navigation
    rightPage.innerHTML = `
        <div class="page-content stamp-details">
            <h2>${item.title}</h2>
            <p class="stamp-desc">
                ${item.description || "Información detallada no disponible."}
                <br><br>
                <strong>Colección:</strong> ${getStampCategory(item.title)}<br>
                <strong>Estado:</strong> ${item.price === 'Colección' ? 'Pieza de Colección' : (item.price || 'Consultar')}
            </p>
            
            <div class="book-nav-controls">
                <button class="nav-btn back-index">☙ Volver al Índice</button>
            </div>
        </div>
    `;

    // Bind Back Button
    rightPage.querySelector('.back-index').addEventListener('click', () => {
        renderBookIndex(allItems, leftPage, rightPage);
    });
}

// --- LÓGICA HERO OVERLAY ---

function setupHeroOverlayParams() {
    // Cerrar al hacer clic en el fondo del overlay
    heroOverlay.addEventListener('click', closeHeroMode);
}

function activateHeroMode(originalWrapper) {
    if (isHeroMode) return;
    isHeroMode = true;
    activeBookOriginal = originalWrapper;

    // 1. Obtener coordenadas iniciales (donde está el libro ahora)
    const rect = originalWrapper.getBoundingClientRect();

    // 2. Clonar el libro para el overlay
    // No usamos cloneNode directamente para evitar coger eventos o estados raros,
    // mejor reconstruimos una "versión héroe" limpia.
    const heroBook = document.createElement('div');
    heroBook.className = 'hero-book book-wrapper'; // book-wrapper para heredar estilos básicos
    // Necesitamos dimensions iguales al inicio
    heroBook.style.width = rect.width + 'px';
    heroBook.style.height = rect.height + 'px';
    heroBook.style.position = 'absolute';
    heroBook.style.left = rect.left + 'px';
    heroBook.style.top = rect.top + 'px';
    heroBook.style.margin = '0'; // Quitar margen de lista

    // Recreamos estructura interna para que se vea igual
    // Copiamos el HTML interno es más rápido
    heroBook.innerHTML = originalWrapper.innerHTML;

    // Ajustes visuales iniciales para que coincida con el libro cerrado/spine
    // Ojo: originalWrapper tiene un rotateY y translateZ por CSS.
    // Al ponerlo en overlay (flat), perderemos esa perspectiva inmediata.
    // Para que la transición sea suave, deberíamos empezar con transformaciones similares?
    // Simplificación: Empezamos "plano" en la posición de pantalla del spine.

    heroOverlay.appendChild(heroBook);

    // 3. Ocultar original (para que no se vea duplicado detrás)
    originalWrapper.classList.add('hidden');

    // 4. Activar Overlay (fondo oscuro)
    heroOverlay.classList.add('active');

    // 5. ANIMACIÓN REDIMENSIONADO REAL (Resolution Independence)
    // En lugar de scale(), cambiamos width/height reales para que el browser renderice full quality.

    // Dimensiones iniciales (coinciden con el CSS actual para suavidad)
    // Asumimos que la portada empieza siendo de 250px x 250px (aprox, cuadrado contenedor)
    // Importante: Si empezamos con 40px (spine), al poner width:100% en cover se aplastaría.
    // Hack visual: Empezamos la animación asumiendo que ya "somos" la portada.
    heroBook.style.width = '250px';
    heroBook.style.height = '250px';

    requestAnimationFrame(() => {
        // CÁLCULO DE TAMAÑO OBJETIVO (85% del alto de pantalla)
        const vh = window.innerHeight;
        const targetHeight = Math.floor(vh * 0.85);
        const targetWidth = targetHeight; // Mantenemos relación 1:1 del contenedor (la imagen se ajusta con contain)

        heroBook.style.transition = 'all 0.8s cubic-bezier(0.25, 1, 0.5, 1)';

        // Aplicamos tamaño físico (píxeles reales)
        heroBook.style.width = targetWidth + 'px';
        heroBook.style.height = targetHeight + 'px';

        // Centramos y rotamos (SIN SCALE)
        heroBook.style.left = '50%';
        heroBook.style.top = '50%';
        heroBook.style.transform = 'translate(-50%, -50%) rotateY(0deg)';

        // Asegurar que la portada se ve con info
        const info = heroBook.querySelector('.cover-info');
        if (info) info.style.opacity = '1';
    });
}

function closeHeroMode() {
    if (!isHeroMode) return;

    const heroBook = heroOverlay.querySelector('.hero-book');
    if (!heroBook || !activeBookOriginal) {
        resetHeroState();
        return;
    }

    // 1. Calcular rect destino (el libro original original)
    // Ojo: si hemos hecho scroll mientras estaba abierto (aunque deberíamos bloquear scroll?)
    // el original puede haberse movido o estar fuera.
    // Asumimos que no se mueve el fondo.

    // Quitamos 'hidden' un momento para medirlo? No, ya tenemos su posición si no se movió el container.
    // Si permitimos pan/scroll detrás, necesitamos medir de nuevo.
    activeBookOriginal.classList.remove('hidden');
    const rect = activeBookOriginal.getBoundingClientRect();
    activeBookOriginal.classList.add('hidden'); // Ocultar de nuevo hasta que llegue

    // 2. Animar de vuelta
    // Importante: rotateY(0deg) y scale(1)
    heroBook.style.transform = 'translate(0, 0) rotateY(0deg) scale(1)';
    // Pero necesitamos mover left/top también
    heroBook.style.left = rect.left + 'px';
    heroBook.style.top = rect.top + 'px';
    heroBook.style.width = rect.width + 'px';
    heroBook.style.height = rect.height + 'px';

    // Ocultar info
    const info = heroBook.querySelector('.cover-info');
    if (info) info.style.opacity = '0';

    // 3. Al terminar transición, limpiar
    heroOverlay.classList.remove('active'); // Fondo transparente

    setTimeout(() => {
        resetHeroState();
    }, 500); // 0.5s coincide con transición de overlay opacity, libro tarda 0.8s
    // Mejor esperar los 0.8s del libro para que llegue a su sitio visualmente.
    // Pero el usuario quiere rapidez. 0.5s está bien para el fade out del fondo.
    // El libro seguirá moviéndose un poco más hasta "encajar".

    setTimeout(() => {
        if (activeBookOriginal) activeBookOriginal.classList.remove('hidden');
        if (heroBook) heroBook.remove();
        isHeroMode = false;
        activeBookOriginal = null;
    }, 800);
}

function resetHeroState() {
    heroOverlay.innerHTML = '';
    heroOverlay.classList.remove('active');
    if (activeBookOriginal) activeBookOriginal.classList.remove('hidden');
    activeBookOriginal = null;
    isHeroMode = false;
}

// --- NAVEGACIÓN (PAN) ---

function setupPanNavigation() {
    document.addEventListener('mousedown', (e) => {
        if (isHeroMode) return; // No mover si estamos viendo un libro
        if (e.target.closest('.controls') || e.target.closest('.book-wrapper')) return;

        isDragging = true;
        startX = e.clientX - currentX;
        startY = e.clientY - currentY;
        document.body.style.cursor = 'grabbing';
        // EVITAR SELECCIÓN DE TEXTO / TEMBLOR
        document.body.style.userSelect = 'none';
        libraryContainer.style.transition = 'none';

        // Asegurar estilos en libraryContainer también si es necesario
        // Para que el drag sea fluido y no pille hijos
        libraryContainer.style.pointerEvents = 'none';
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        if (isHeroMode) return;

        e.preventDefault(); // Crítico para evitar selección nativa del browser

        currentX = e.clientX - startX;
        currentY = e.clientY - startY;

        libraryContainer.style.transform = `translate(${currentX}px, ${currentY}px)`;
    });

    document.addEventListener('mouseup', () => {
        isDragging = false;
        document.body.style.cursor = 'grab';
        document.body.style.userSelect = ''; // Restaurar
        libraryContainer.style.pointerEvents = ''; // Restaurar
    });

    document.addEventListener('wheel', (e) => {
        if (isHeroMode) return;

        // Evitar comportamiento nativo (zoom, scroll pagina, etc)
        // e.preventDefault(); 

        const scrollSpeed = 2.5; // Aumentado para que "baje" más rápido
        currentY -= e.deltaY * scrollSpeed;

        // Quitar transición para respuesta instantánea, o muy rápida
        libraryContainer.style.transition = 'none';
        libraryContainer.style.transform = `translate(${currentX}px, ${currentY}px)`;
    }, { passive: false });
}

function setupEvents() {
    resetBtn.addEventListener('click', () => {
        if (isHeroMode) closeHeroMode();

        currentX = 0;
        currentY = 0;
        libraryContainer.style.transition = 'transform 0.8s ease';
        libraryContainer.style.transform = `translate(0px, 0px)`;

        searchInput.value = '';
        clearHighlights();
    });

    searchInput.addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase();
        clearHighlights();

        if (query.length < 2) return;

        const books = document.querySelectorAll('.book-wrapper');
        let firstMatch = null;

        books.forEach(book => {
            if (book.dataset.title.includes(query)) {
                book.querySelector('.spine').classList.add('highlight');
                if (!firstMatch) firstMatch = book;
            }
        });

        // Auto-centrar en el primero encontrado?
        if (firstMatch) {
            // centerOnElement(firstMatch); // Implementar si se desea
        }
    });
}

function clearHighlights() {
    document.querySelectorAll('.spine.highlight').forEach(el => el.classList.remove('highlight'));
}




function setupMusic() {
    const audio = document.getElementById('bgMusic');
    const musicBtn = document.getElementById('musicBtn');

    // Lista completa del álbum "MIS DISCOS"
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

    let currentTrackIndex = 0;
    const basePath = "../assets/music/";

    if (musicBtn && audio) {
        // Inicializar primera canción
        audio.src = basePath + playlist[0];

        musicBtn.addEventListener('click', () => {
            if (audio.paused) {
                audio.play().catch(e => console.log("Audio play error:", e));
                musicBtn.innerText = "⏸ Pause"; // "Pause" más universal
                musicBtn.style.background = "#ff4757";
            } else {
                audio.pause();
                musicBtn.innerText = "🎵 Play Album";
                musicBtn.style.background = "#e6b800";
            }
        });

        // Al terminar una, pasar a la siguiente (Bucle del álbum)
        audio.addEventListener('ended', () => {
            currentTrackIndex = (currentTrackIndex + 1) % playlist.length;
            audio.src = basePath + playlist[currentTrackIndex];
            audio.play().catch(e => console.log("Auto-next error:", e));
            console.log("Playing next:", playlist[currentTrackIndex]);
        });
    }
}

window.onload = init;

