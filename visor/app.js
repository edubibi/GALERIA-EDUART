const state = {
    photos: (typeof artworkData !== 'undefined') ? artworkData : [],
    currentGlobalFrame: 'classic',
    frameStyles: [
        { id: 'classic', name: 'Clásico' },
        { id: 'modern', name: 'Moderno' },
        { id: 'vintage', name: 'Vintage' },
        { id: 'minimalist', name: 'Minimalista' },
        { id: 'ornate', name: 'Ornado' },
        { id: 'wood', name: 'Madera' },
        { id: 'metallic', name: 'Metálico' },
        { id: 'shadow', name: 'Sombra' },
        { id: 'custom-gray', name: 'Gris Antiguo' }
    ]
};

// Init
document.addEventListener('DOMContentLoaded', () => {
    // Landing Page & Splash Screen Logic
    const params = new URLSearchParams(window.location.search);
    const hasCategory = params.get('category');
    const hasImg = params.get('img');

    const splash = document.getElementById('splashScreen');
    const landing = document.getElementById('landingPage');
    const app = document.getElementById('appContainer');

    // Si venimos de colecciones (con categoría) o con una imagen directa,
    // saltamos la pantalla de inicio directamente.
    if (hasCategory || hasImg) {
        if (splash) splash.style.display = 'none';
        if (landing) landing.style.display = 'none';
        if (app) {
            app.style.display = 'flex';
            app.style.opacity = '1';
        }
    } else {
        // Lógica original (por si entran 'a pelo' a la url)
        if (splash) {
            splash.addEventListener('click', () => {
                splash.style.opacity = '0';
                setTimeout(() => {
                    splash.style.visibility = 'hidden';
                }, 800);
            });
        }
        const enterBtn = document.getElementById('enterBtn');
        if (enterBtn) {
            enterBtn.addEventListener('click', () => {
                if (landing) {
                    landing.style.opacity = '0';
                    landing.style.visibility = 'hidden';
                }
                if (app) {
                    app.style.display = 'flex';
                    setTimeout(() => {
                        app.style.opacity = '1';
                    }, 50);
                }
            });
        }
    }

    loadPreferences();
    initApp();
});

function initApp() {
    // ALERT REMOVED FOR FINAL PRODUCTION - BUT KEEP IF DEBUGGING IS REQUESTED
    // alert("VISOR INICIADO - CONTROL 1");

    // Ensure data is loaded
    if (typeof artworkData !== 'undefined') {
        // Fix: Map flat data to expected structure with metadata
        state.photos = artworkData.map(art => ({
            id: art.id,
            url: art.src,
            name: art.title,
            frame: 'classic',
            metadata: art
        }));
        console.log("Loaded " + state.photos.length + " artworks.");
    } else {
        console.error("Critical: artworkData not found.");
        // alert("Error: No se han podido cargar los datos de las obras.");
    }

    renderFrameSelector();
    loadDynamicImages();
    setupEventListeners();
    updatePhotoCount();

    // Home Button Logic
    document.getElementById('homeBtn').addEventListener('click', () => {
        try {
            window.location.href = '../index.html';
        } catch (e) { console.error(e); }
    });

    // Back Button Logic
    const backBtn = document.getElementById('backBtn');
    if (backBtn) {
        backBtn.addEventListener('click', () => {
            if (window.history.length > 2) {
                window.history.back();
            } else {
                window.location.href = '../colecciones.html';
            }
        });
    }
}

function setupEventListeners() {
    // Sidebar Frame Selector Delegate
    document.getElementById('frameSelector').addEventListener('click', (e) => {
        const option = e.target.closest('.frame-option');
        if (option) {
            setGlobalFrame(option.dataset.frame);
        }
    });

    // Modal Close
    const modal = document.getElementById('imageModal');
    const closeBtn = document.querySelector('.close-modal');
    closeBtn.onclick = () => closeModal();
    window.onclick = (e) => { if (e.target == modal) closeModal(); }

    // Customization Listeners
    const thicknessInput = document.getElementById('frameThickness');
    thicknessInput.addEventListener('input', (e) => {
        updateFrameThickness(e.target.value);
        savePreferences();
    });

    const titleInput = document.getElementById('appTitleInput');
    titleInput.addEventListener('input', (e) => {
        document.querySelector('.brand h1').innerText = e.target.value;
        savePreferences();
    });

    const subtitleInput = document.getElementById('appSubtitleInput');
    subtitleInput.addEventListener('input', (e) => {
        document.querySelector('.brand p').innerText = e.target.value;
        savePreferences();
    });

    // Logo Upload
    const logoInput = document.getElementById('logoInput');
    logoInput.addEventListener('change', handleLogoUpload);

    // Remove Logo
    document.getElementById('removeLogo').addEventListener('click', () => {
        document.getElementById('brandLogo').src = '';
        document.getElementById('brandLogo').style.display = 'none';
        document.getElementById('removeLogo').style.display = 'none';
        savePreferences();
    });

    // Background Upload
    const bgInput = document.getElementById('bgInput');
    bgInput.addEventListener('change', handleBgUpload);

    // Background Size
    const bgSizeInput = document.getElementById('bgSizeInput');
    bgSizeInput.addEventListener('input', (e) => {
        const val = e.target.value;
        document.body.style.backgroundSize = `${val}%`;
        savePreferences();
    });

    // Remove Background
    document.getElementById('removeBg').addEventListener('click', () => {
        document.body.style.backgroundImage = '';
        document.getElementById('removeBg').style.display = 'none';
        savePreferences();
    });

    // Admin Toggle
    document.getElementById('adminToggle').addEventListener('click', () => {
        const panel = document.getElementById('customizationPanel');
        if (panel.style.display === 'none') {
            const password = prompt("Introduce la contraseña de administrador:");
            if (password === "admin") {
                panel.style.display = 'block';
            } else if (password !== null) {
                alert("Contraseña incorrecta.");
            }
        } else {
            panel.style.display = 'none';
        }
    });

    // Scale Reference Toggle
    const scaleCheckbox = document.getElementById('showScaleRef');
    if (scaleCheckbox) {
        scaleCheckbox.addEventListener('change', (e) => {
            const ref = document.getElementById('scaleReference');
            if (e.target.checked) {
                ref.style.display = 'flex';
                setTimeout(() => ref.classList.add('visible'), 10);
            } else {
                ref.classList.remove('visible');
                setTimeout(() => ref.style.display = 'none', 500);
            }
        });
    }
}

function handleLogoUpload(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (readerEvent) => {
            const base64 = readerEvent.target.result;
            if (base64.length > 2000000) {
                alert("La imagen del logo es demasiado grande para guardarse. Intenta con una más pequeña.");
                return;
            }
            const logoImg = document.getElementById('brandLogo');
            logoImg.src = base64;
            logoImg.style.display = 'block';
            document.getElementById('removeLogo').style.display = 'block';
            savePreferences();
        };
        reader.readAsDataURL(file);
    }
    e.target.value = '';
}

function handleBgUpload(e) {
    const file = e.target.files[0];
    if (file && file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onload = (readerEvent) => {
            const base64 = readerEvent.target.result;
            if (base64.length > 5000000) {
                alert("La imagen es demasiado pesada (>5MB).");
                return;
            }
            document.body.style.backgroundImage = `url('${base64}')`;
            document.getElementById('removeBg').style.display = 'inline';
            savePreferences();
        };
        reader.readAsDataURL(file);
    }
    e.target.value = '';
}

function updateFrameThickness(value) {
    document.documentElement.style.setProperty('--frame-thickness', value);
}

function savePreferences() {
    const prefs = {
        thickness: document.getElementById('frameThickness').value,
        title: document.getElementById('appTitleInput').value,
        subtitle: document.getElementById('appSubtitleInput').value,
        globalFrame: state.currentGlobalFrame,
        logoData: document.getElementById('brandLogo').getAttribute('src'),
        bgData: document.body.style.backgroundImage,
        bgSize: document.getElementById('bgSizeInput').value
    };
    localStorage.setItem('lumiere_prefs', JSON.stringify(prefs));
}

function loadPreferences() {
    const saved = localStorage.getItem('lumiere_prefs');
    if (saved) {
        try {
            const prefs = JSON.parse(saved);
            if (prefs.thickness) {
                document.getElementById('frameThickness').value = prefs.thickness;
                updateFrameThickness(prefs.thickness);
            }
            if (prefs.title) {
                document.getElementById('appTitleInput').value = prefs.title;
                document.querySelector('.brand h1').innerText = prefs.title;
            }
            if (prefs.subtitle) {
                document.getElementById('appSubtitleInput').value = prefs.subtitle;
                document.querySelector('.brand p').innerText = prefs.subtitle;
            }
            if (prefs.globalFrame) {
                state.currentGlobalFrame = prefs.globalFrame;
            }
            if (prefs.logoData && prefs.logoData.length > 10) {
                const logoImg = document.getElementById('brandLogo');
                logoImg.src = prefs.logoData;
                logoImg.style.display = 'block';
                document.getElementById('removeLogo').style.display = 'block';
            }
            if (prefs.bgData && prefs.bgData.length > 5) {
                document.body.style.backgroundImage = prefs.bgData;
                document.getElementById('removeBg').style.display = 'inline';
            }
            if (prefs.bgSize) {
                document.getElementById('bgSizeInput').value = prefs.bgSize;
                document.body.style.backgroundSize = `${prefs.bgSize}%`;
            }
        } catch (e) {
            console.error("Error loading preferences:", e);
            localStorage.removeItem('lumiere_prefs');
        }
    }
}

function loadDynamicImages() {
    const urlParams = new URLSearchParams(window.location.search);
    const categoryFilter = urlParams.get('category');

    // Make sure we have latest data
    if (typeof artworkData !== 'undefined' && (!state.photos || state.photos.length === 0)) {
        state.photos = artworkData;
    }

    if (state.photos.length > 0) {
        let dataToLoad = state.photos;

        if (categoryFilter && categoryFilter !== 'null' && categoryFilter !== '') {
            dataToLoad = state.photos.filter(art => art.category === categoryFilter);

            // CRITICAL FIX: We must update the source of truth for the renderer
            state.photos = dataToLoad;

            const headerTitle = document.querySelector('.top-bar h2');
            if (headerTitle) {
                const cleanTitle = categoryFilter.replace(/^\d+/, '').replace(/_/g, ' ');
                headerTitle.innerText = `Colección: ${cleanTitle}`;
            }
        }

        // Ensure all have default frame if missing
        state.photos.forEach(p => {
            if (!p.frame) p.frame = state.currentGlobalFrame;
        });

        renderGallery();
    }

    const directImg = urlParams.get('img');
    const directTitle = urlParams.get('title');
    const directIdParam = urlParams.get('id');

    if (directImg) {
        console.log(`[VISOR INIT START]`);
        console.log(`- ID parametro: ${directIdParam}`);
        console.log(`- Categoria parametro: ${categoryFilter}`);
        console.log(`- Titulo parametro: ${directTitle}`);
        console.log(`- Img buscada (directImg): ${directImg}`);
        console.log(`- Total obras en state.photos: ${state.photos.length}`);

        const directId = 'direct_' + Date.now();
        let targetId = null;

        // Try to find by ID first, then by URL
        let existing = null;
        if (directIdParam) {
            existing = state.photos.find(p => p.id === directIdParam);
        }
        if (!existing) {
            existing = state.photos.find(p => p.url === directImg);
        }
        if (!existing) {
            existing = state.photos.find(p => p.src === directImg); // Try .src
        }
        // Try fuzzy match on filename
        if (!existing) {
            const justName = directImg.split('/').pop();
            existing = state.photos.find(p => p.src && p.src.endsWith(justName));
        }

        if (existing) {
            targetId = existing.id;
            console.log(`[VISOR ID MATCHED] existing.id =`, existing.id, existing.src);
        } else {
            console.warn(`[VISOR ID NO MATCH] Creando entrada temporal para:`, directImg);
            
            // Normalize the directImg path to ensure it starts with '../' for the Visor HTML location
            let visorPath = directImg;
            if (!visorPath.startsWith('../') && !visorPath.startsWith('http')) {
                visorPath = '../' + visorPath;
            }

            // Create temporary entry for this view session
            addPhoto(visorPath, directTitle || 'Obra Seleccionada', directId, {
                description: 'Obra personalizada',
                price: 'Consultar',
                size: 'Consultar'
            });
            targetId = directId;
        }

        const landing = document.getElementById('landingPage');
        const app = document.getElementById('appContainer');
        const splash = document.getElementById('splashScreen');

        if (splash) splash.style.display = 'none';
        landing.style.display = 'none';
        app.style.display = 'flex';
        app.style.opacity = '1';

        setTimeout(() => {
            openModal(targetId);
        }, 100);
    }
}

function addPhoto(url, name, specificId = null, metadata = {}) {
    const photo = {
        id: specificId || (Date.now() + Math.random()),
        url: url,
        name: name,
        frame: state.currentGlobalFrame,
        metadata: metadata
    };
    // Only add if not exists (check by ID)
    if (!state.photos.find(p => p.id === photo.id)) {
        state.photos.unshift(photo);
    }
    renderGallery();
    updatePhotoCount();
}

function renderGallery() {
    const grid = document.getElementById('photoGrid');

    // Safety check: Filter out null/undefined photos
    const validPhotos = state.photos.filter(p => p && (p.url || p.src));

    grid.innerHTML = validPhotos.map(photo => {
        try {
            // Normalize URL: Use src if url is missing (legacy compat)
            let rawUrl = photo.url || photo.src;
            if (rawUrl && !rawUrl.startsWith('../') && !rawUrl.startsWith('data:') && !rawUrl.startsWith('http')) {
                rawUrl = '../' + rawUrl;
            }

            const safeUrl = encodeURI(rawUrl).replace(/'/g, "%27");

            return `
        <div class="photo-card frame-${photo.frame || 'classic'}" onclick="openModal('${photo.id}')">
            <img src="${safeUrl}" alt="${photo.name}" loading="lazy">
            <div class="card-overlay" style="position:absolute; bottom:0; left:0; right:0; background:rgba(255,255,255,0.9); padding:5px; display:flex; justify-content:center;">
                <button onclick="event.stopPropagation(); cartFromVisor('${photo.id}')" style="background:#000; color:#fff; border:none; padding:4px 8px; font-size:0.7rem; cursor:pointer; border-radius:3px;">🛒 Comprar el Cuadro</button>
            </div>
        </div>
            `;
        } catch (e) {
            console.warn("Error rendering photo in visor:", photo, e);
            return '';
        }
    }).join('');
}

// Global helper for visor grid
window.cartFromVisor = function (id) {
    let rawUrl = photo.url || photo.src || '';
    // If it starts with ../ it's relative to visor/, we need it relative to root for the cart
    let thumbPath = rawUrl.startsWith('../') ? rawUrl.replace('../', '') : rawUrl;

    const item = {
        id: photo.id,
        title: photo.name || photo.title,
        price: photo.metadata?.price || 'Consultar',
        thumb: thumbPath
    };
    if (typeof addToCart === 'function') {
        addToCart(item);
        alert('Obra añadida al carrito.');
    }
};

function updatePhotoCount() {
    const count = state.photos ? state.photos.length : 0;
    document.getElementById('photoCount').innerText = `${count} fotos en colección`;
}

let currentModalPhotoId = null;

function openModal(id) {
    const photo = state.photos.find(p => p.id == id);
    if (!photo) return;

    currentModalPhotoId = id;
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalControls = document.getElementById('modalFrameSelector');

    // Normalize URL for modal
    let rawUrl = photo.url || photo.src;
    if (rawUrl && !rawUrl.startsWith('../') && !rawUrl.startsWith('data:') && !rawUrl.startsWith('http')) {
        rawUrl = '../' + rawUrl;
    }
    modalImg.src = rawUrl;

    modalImg.className = '';
    const frameClass = photo.frame || 'classic';
    modalImg.classList.add(`frame-${frameClass}`);

    const container = document.getElementById('modalFrameContainer');
    container.className = `modal-frame-container frame-${frameClass}`;

    // Reset Environment to Neutral on open
    changeEnvironment('neutral');
    changePreviewSize('large');

    modalControls.innerHTML = state.frameStyles.map(style => `
        <div class="frame-option ${frameClass === style.id ? 'active' : ''}" 
             onclick="changeSinglePhotoFrame('${style.id}')">
            <span>${style.name}</span>
        </div>
    `).join('');

    document.getElementById('artTitle').innerText = photo.name || photo.title || 'Sin Título';
    document.getElementById('artCatalog').innerText = photo.metadata?.catalogo || photo.category || '';
    document.getElementById('artDesc').innerText = photo.metadata?.description || 'Sin descripción';

    let priceVal = photo.metadata?.price || '';
    // Format price if just a number
    if (priceVal && !isNaN(priceVal.replace('.', '').replace(',', ''))) {
        priceVal += ' €';
    }
    // If it has digits but no currency symbol and not 'consultar', add €
    else if (priceVal && !priceVal.includes('€') && !priceVal.toLowerCase().includes('consultar')) {
        if (/\d/.test(priceVal)) priceVal += ' €';
    }

    const priceText = priceVal ? `Precio: ${priceVal}` : '';
    const sizeText = photo.metadata?.size ? `📏 Tamaño Real: ${photo.metadata.size}` : '';
    const techText = photo.metadata?.tech_info || '';

    document.getElementById('artPrice').innerText = priceText;
    document.getElementById('artSize').innerText = sizeText;
    document.getElementById('artSize').style.display = sizeText ? 'block' : 'none';

    // Update Tech Info
    const techEl = document.getElementById('artTechInfo');
    if (techEl) {
        techEl.innerText = techText;
        techEl.style.display = techText ? 'block' : 'none';
    }

    // CART LOGIC
    const cartBtn = document.getElementById('addToCartBtn');
    const cartMsg = document.getElementById('cartMsg');

    if (cartBtn) {
        cartBtn.onclick = () => {
            const item = {
                id: photo.id,
                title: photo.name || photo.title,
                price: priceVal || 'Consultar',
                // Store path relative to ROOT (remove ../)
                thumb: rawUrl.replace('../', '')
            };

            if (typeof addToCart === 'function') {
                addToCart(item);
                // Immediately redirect to cart upon purchase to improve flow
                window.location.href = '../carrito.html';
            } else {
                console.error('Cart logic not loaded');
                alert('Error interno: El carrito no está cargado.');
            }
        };
    }

    modal.classList.add('active');
}

function closeModal() {
    if (window.history.length > 2) {
        window.history.back();
    } else {
        window.location.href = '../colecciones.html';
    }
}

window.changeSinglePhotoFrame = function (styleId) {
    const photo = state.photos.find(p => p.id === currentModalPhotoId);
    if (photo) {
        photo.frame = styleId;
        document.getElementById('modalFrameContainer').className = `modal-frame-container frame-${styleId}`;
        const buttons = document.getElementById('modalFrameSelector').getElementsByClassName('frame-option');
        Array.from(buttons).forEach(btn => {
            const styleName = state.frameStyles.find(f => f.id === styleId).name;
            if (btn.innerText === styleName) btn.classList.add('active');
            else btn.classList.remove('active');
        });
        renderGallery();
    }
};

let currentSize = 'large';

window.changePreviewSize = function (size) {
    currentSize = size;
    const container = document.getElementById('modalFrameContainer');

    container.classList.remove('preview-small', 'preview-medium', 'preview-large');
    container.classList.add(`preview-${size}`);

    const buttons = document.querySelectorAll('.btn-size');
    buttons.forEach(btn => {
        const map = { 'small': 'S', 'medium': 'M', 'large': 'L' };
        if (btn.innerText.trim() === map[size]) btn.classList.add('active');
        else if (btn.classList.contains('active') && ['S', 'M', 'L'].includes(btn.innerText.trim())) btn.classList.remove('active');
    });
};


window.changeEnvironment = function (mode) {
    const container = document.getElementById('modalFrameContainer');
    const btnNeutral = document.getElementById('btnEnvNeutral');
    const btnRoom = document.getElementById('btnEnvRoom');
    const btnClassic = document.getElementById('btnEnvClassic');
    const btnTable = document.getElementById('btnEnvTable');

    const img = container.querySelector('img');

    // Reset all
    container.classList.remove('env-room', 'env-bedroom', 'env-table');
    if (btnNeutral) btnNeutral.classList.remove('active');
    if (btnRoom) btnRoom.classList.remove('active');
    if (btnClassic) btnClassic.classList.remove('active');
    if (btnTable) btnTable.classList.remove('active');

    // Remove forced styles
    if (img) {
        img.style.transform = '';
        img.style.boxShadow = '';
        img.style.maxHeight = '';
        img.style.transformOrigin = '';
    }

    if (mode === 'room') {
        container.classList.add('env-room');
        if (btnRoom) btnRoom.classList.add('active');
    } else if (mode === 'bedroom') {
        container.classList.add('env-bedroom');
        if (btnNeutral) btnNeutral.classList.add('active');
    } else if (mode === 'table') {
        container.classList.add('env-table');
        if (btnTable) btnTable.classList.add('active');
    } else {
        if (btnClassic) btnClassic.classList.add('active');
        changePreviewSize(currentSize || 'large');
    }
};

function renderFrameSelector() {
    const container = document.getElementById('frameSelector');
    container.innerHTML = state.frameStyles.map(style => `
        <div class="frame-option ${state.currentGlobalFrame === style.id ? 'active' : ''}" 
             data-frame="${style.id}">
             <span>${style.name}</span>
             <div style="width: 20px; height: 20px; background: #ddd; border-radius: 50%;"></div>
        </div>
    `).join('');
}
