/**
 * CARGADOR DINÁMICO DE GALERÍAS
 * Se encarga de leer 'data.js' y pintar las obras en la web.
 */

document.addEventListener('DOMContentLoaded', () => {
    console.log("Cargando obras...", artworkData);

    // 1. Si estamos en la página de GALERÍA COMPLETA
    const galleryContainer = document.getElementById('gallery-container');
    if (galleryContainer) {
        // Check for URL filter
        const params = new URLSearchParams(window.location.search);
        const catFilter = params.get('category');

        let displayData = artworkData;

        // UPDATE TOTAL COUNT
        const totalCountEl = document.getElementById('total-count');
        if (totalCountEl) {
            totalCountEl.textContent = `(${artworkData.length} obras)`;
        }

        if (catFilter) {
            // Apply Initial Filter
            displayData = artworkData.filter(art => art.category === catFilter);
            console.log(`Filtering gallery by: ${catFilter}`);

            // Update page title and add "Back to Collections" button
            const headerContainer = document.querySelector('.page-header .container');
            if (headerContainer) {
                const title = headerContainer.querySelector('h1');
                // Clean title: Remove leading digits and underscores
                const cleanTitle = catFilter.replace(/^\d+/, '').replace(/_/g, ' ');
                if (title) title.innerHTML = `Colección: ${cleanTitle}`;

                // Create Back Button
                const backLink = document.createElement('div');
                backLink.style.marginTop = '1rem';
                backLink.innerHTML = `<a href="colecciones.html" class="btn-highlight" style="background: transparent; border: 1px solid #fff; color: #fff; text-decoration: none; font-size: 0.9rem;">&larr; Volver a Colecciones</a>`;
                headerContainer.appendChild(backLink);
            }
        }

        displayData.forEach(art => {
            try {
                const card = createArtCard(art);
                galleryContainer.appendChild(card);
            } catch (err) {
                console.warn("Skipping artwork due to error:", art, err);
            }
        });
    }

    // 2. Si estamos en la página de COLECCIONES
    const filtersContainer = document.getElementById('collection-filters');
    const resultsContainer = document.getElementById('collections-results');

    if (filtersContainer && resultsContainer) {
        // Obtenemos categorías únicas
        const categories = [...new Set(artworkData.map(art => art.category))];

        // Limpiar área de filtros
        filtersContainer.innerHTML = '';
        filtersContainer.style.display = 'none';

        // Limpiar solo el mensaje de carga, mantener tarjetas estáticas
        const loadingMsg = resultsContainer.querySelector('p');
        if (loadingMsg) loadingMsg.remove();

        // Renderizar una TARJETA por CATEGORÍA
        if (categories.length === 0) {
            resultsContainer.innerHTML = '<p style="text-align:center; width:100%;">No hay colecciones disponibles.</p>';
        } else {
            categories.forEach(cat => {
                // Find cover: check specific cover first, then fallback to first artwork
                let coverImage = '';
                if (typeof categoryCovers !== 'undefined') {
                    coverImage = categoryCovers[cat] || categoryCovers[cat.replace(/ /g, '_')] || '';
                }

                if (coverImage) {
                    // Found cover in map
                } else {
                    const coverArt = artworkData.find(art => art.category === cat);
                    coverImage = coverArt ? coverArt.src : '';
                }

                const card = document.createElement('div');
                card.className = 'category-card';

                // Clean category for display
                const displayCat = cat.replace(/^\d+/, '').replace(/_/g, ' ');

                // Custom Badge and Link for Fursona
                let badgeText = displayCat;
                let badgeStyle = "background: rgba(0,0,0,0.5);";
                let clickAction = () => window.location.href = `cuadroteca/index.html?category=${encodeURIComponent(cat)}`;

                if (cat === "00FURSONA GENESIS") {
                    badgeText = "TOP NFT";
                    badgeStyle = "background: rgba(160, 32, 240, 0.7);";
                    clickAction = () => window.location.href = "fursona-genesis.html";
                }

                card.onclick = clickAction;

                card.innerHTML = `
                    <div class="placeholder-cover" style="background-image: url('${coverImage}'); background-size: cover; background-position: center; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">
                        <span style="${badgeStyle} padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem;">${badgeText}</span>
                    </div>
                    <h3>${displayCat}</h3>
                `;
                resultsContainer.appendChild(card);
            });
        }
    }

    // 3. Si estamos en el HOME (Obras destacadas) - Opcional
    const featuredContainer = document.querySelector('.grid-placeholder');
    if (featuredContainer) {
        // Limpiamos el placeholder
        featuredContainer.innerHTML = '';
        featuredContainer.className = 'collections-grid';

        // Mostramos las 3 primeras
        artworkData.slice(0, 3).forEach(art => {
            try {
                const card = createArtCard(art);
                featuredContainer.appendChild(card);
            } catch (err) {
                console.warn("Skipping featured artwork due to error:", art, err);
            }
        });
    }
});

// Función auxiliar para crear la tarjeta de una obra
function createArtCard(art) {
    const el = document.createElement('div');
    el.className = 'collection-card';

    // Al hacer click, vamos al VISOR con esa imagen
    const viewerPath = '../' + art.src;
    const viewerLink = `visor/index.html?img=${encodeURIComponent(viewerPath)}&title=${encodeURIComponent(art.title)}&category=${encodeURIComponent(art.category)}&id=${art.id}`;

    // Make the whole card clickable safely
    el.addEventListener('click', () => {
        window.location.href = viewerLink;
    });
    el.style.cursor = 'pointer';

    // Safe Price Check to avoid crash on null/undefined
    let priceDisplay = '';

    if (false) { // Disabled as per user request
        priceDisplay = '<span style="color: #d9534f; font-weight: bold; letter-spacing: 1px;">🔴 VENDIDO</span>';
    } else if (art.price && typeof art.price === 'string' && !isNaN(art.price.replace('.', '').replace(',', ''))) {
        priceDisplay = art.price + ' &euro;';
    } else if (art.price && art.price !== 'Consultar') {
        // If it is 'Consultar' or other string
        priceDisplay = art.price;
    }

    // Safe URL encoding (fix for "Grey Boxes")
    // We escape single quotes by replacing them, or just use encodeURI if the path is standard.
    // Ideally, we replicate strict CSS url() syntax.
    const safeUrl = encodeURI(art.src).replace(/'/g, "%27");


    const isNFT = art.category === "00FURSONA GENESIS";

    el.innerHTML = `
        <div class="card-image" style="background-image: url('${safeUrl}'); background-color: ${art.placeholderColor || '#ccc'};">
        </div>
        <div class="card-info">
            ${isNFT ? '' : '<div class="promo-badge" style="background:#e67e22; color:white; padding:4px 8px; border-radius:4px; font-size:0.75rem; font-weight:bold; display:inline-block; margin-bottom:0.8rem;">PROMOCIÓN 3+1</div>'}
            <h3>${art.title || 'Sin Título'}</h3>
            <p title="${art.description || ''}">${art.description || ''}</p>
            <p style="font-size: 0.85rem; color: #666; margin-top: 0.5rem;">📏 ${art.size || 'Tamaño no disp.'}</p>
            <p style="font-weight: bold; color: #000; margin-top: 0.2rem;">${priceDisplay}</p>
            ${isNFT ? '' : `
            <div style="margin-top:1rem; display:flex; gap:0.5rem;">
                <button class="cart-btn" style="flex:1; background:#1a1a1a; color:white; border:none; padding:0.5rem; cursor:pointer; font-weight:bold; font-size:0.8rem; border-radius:4px;">🛒 Comprar el Cuadro</button>
                <span class="btn-highlight" style="font-size:0.8rem; padding:0.5rem; border:1px solid #ccc; border-radius:4px;">Ver Detalles</span>
            </div>
            `}
        </div>
    `;

    // Add To Cart logic (only if button exists)
    const buyBtn = el.querySelector('.cart-btn');
    if (buyBtn) {
        buyBtn.addEventListener('click', (e) => {
            e.stopPropagation(); // Don't open visor
            if (typeof addToCart === 'function') {
                const added = addToCart(art);
                if (added) {
                    buyBtn.innerText = '✅ ¡Añadido!';
                    buyBtn.style.background = '#28a745';
                    setTimeout(() => {
                        buyBtn.innerText = '🛒 Comprar el Cuadro';
                        buyBtn.style.background = '#1a1a1a';
                    }, 2000);
                } else {
                    alert('Esta obra ya está en tu carrito.');
                }
            }
        });
    }

    return el;
}
