# Configuración
$assetsDir = "assets"
$outputFile = "js/data.js"

Write-Host "Generando catálogo..." -ForegroundColor Cyan

# 1. CARGAR METADATOS
$metadata = @{}
if (Test-Path "metadata.json") {
    try {
        $json = Get-Content "metadata.json" -Raw -Encoding UTF8 | ConvertFrom-Json
        foreach ($prop in $json.PSObject.Properties) {
            $metadata[$prop.Name] = $prop.Value
        }
        Write-Host "Metadatos cargados ($($metadata.Count) entradas)" -ForegroundColor Yellow
    }
    catch {
        Write-Host "Error al leer metadata.json: $_" -ForegroundColor Red
    }
}

# 2. ESCANEAR ARCHIVOS Y GENERAR NUEVO CATALOGO
$artworks = @()
$folders = Get-ChildItem -Path $assetsDir -Directory

foreach ($folder in $folders) {
    $folderName = $folder.Name
    
    # EXCLUSIONES DE CARPETAS
    $excludedDirs = @("bg", "icons", "css", "js", "img", ".git", "assets", "PORTADILLAS_ESTILOS")
    if ($excludedDirs -contains $folderName) {
        continue
    }
    
    Write-Host "Procesando carpeta: $folderName" -ForegroundColor DarkGray
    
    $files = Get-ChildItem -Path $folder.FullName -Include *.jpg, *.png, *.jpeg, *.webp -Recurse

    foreach ($file in $files) {
        # EXCLUSIONES DE ARCHIVOS
        if ($file.Name -match "VISOR|custom_|portafotos|sketch_|room_|RELOJ_PALI_cubesse_2|29BARCO_PESQUERO_EN_ALTAMAR_menor") {
            continue
        }

        # ID Único (Basado en nombre de archivo para permitir movimientos)
        $cleanId = $file.BaseName.ToLower()
        
        # Ruta Relativa Segura
        # .\assets\folder\file.jpg -> assets/folder/file.jpg
        $relPathRaw = (Resolve-Path -Path $file.FullName -Relative)
        $relPath = $relPathRaw -replace "^\.\\", "" 
        $relPath = $relPath.Replace("\", "/")
        # FIX: Retain 'assets/' prefix for correct linking in HTML
        # $relPath = $relPath -replace "^assets/", ""
        
        # FIX: Github Specific Path Mismatches
        # 1. IDE Classic has space on GitHub, underscore locally
        # $relPath = $relPath -replace "06IDE_CLASSIC", "06IDE CLASSIC"
        # 2. SAGA CUBESSEPLUS is in root on GitHub, not inside 02CUBESSE stilo
        # 2. SAGA CUBESSEPLUS path fix (Removed incorrect replacement)
        # $relPath = $relPath -replace "02CUBESSE stilo/SAGA CUBESSEPLUS", "SAGA CUBESSEPLUS"
        
        # Valores por defecto
        # FIX: Limpieza agresiva de números iniciales, guiones y palabras clave internas
        # Palabras a eliminar (case-insensitive)
        $keywordsToRemove = "EDUSSE|CUBESSE|NEOCIRC|EXPNEO|APLICC|PLUMINK|NEOINK|BORACARBON|FRACNEO|OLEOCUBBO|URBANSPHERIC|RECTESSE|TEREXSE|FUZZTESS|FUZZLINE"
        
        $rawTitle = $file.BaseName -replace '^[\d\s\-_]+', '' -replace '_', ' ' `
            -replace "(?i)\b($keywordsToRemove)\b", "" `
            -replace '\s+', ' '
        $rawTitle = $rawTitle.Trim()
        $lower = $rawTitle.ToLower()
        if ($lower.Length -gt 0) {
            $title = $lower.Substring(0, 1).ToUpper() + $lower.Substring(1)
        }
        else {
            $title = $rawTitle
        }
        $desc = "Obra de la colecci" + [char]243 + "n $folderName"
        $price = "19,99"
        $size = "Consultar"

        $tech_info = ""
        $sold = "false"

        # Sobrescribir con metadatos si existen
        # 1. Intentar por ID completo
        if ($metadata.ContainsKey($cleanId)) {
            if ($metadata[$cleanId].title) { $title = $metadata[$cleanId].title }
            if ($metadata[$cleanId].description) { $desc = $metadata[$cleanId].description }
            if ($metadata[$cleanId].price) { $price = $metadata[$cleanId].price }
            if ($metadata[$cleanId].size) { $size = $metadata[$cleanId].size }

            if ($metadata[$cleanId].tech_info) { $tech_info = $metadata[$cleanId].tech_info }
            if ($metadata[$cleanId].sold -eq $true) { $sold = "true" }

        }
        # 2. Intentar por Nombre de Archivo (BaseName) si no se encontró por ID
        elseif ($metadata.ContainsKey($file.BaseName)) {
            if ($metadata[$file.BaseName].title) { $title = $metadata[$file.BaseName].title }
            if ($metadata[$file.BaseName].description) { $desc = $metadata[$file.BaseName].description }
            if ($metadata[$file.BaseName].price) { $price = $metadata[$file.BaseName].price }
            if ($metadata[$file.BaseName].size) { $size = $metadata[$file.BaseName].size }

            if ($metadata[$file.BaseName].tech_info) { $tech_info = $metadata[$file.BaseName].tech_info }
            if ($metadata[$file.BaseName].sold -eq $true) { $sold = "true" }

        }

        $artworks += @{
            id          = $cleanId
            title       = $title
            category    = $folderName
            src         = $relPath
            description = $desc
            size        = $size
            price       = $price

            tech_info   = $tech_info
            sold        = $sold
        }
    }
}

# 2. BUSCAR PORTADILLAS (COVERS)
$coversDir = "assets/PORTADILLAS_ESTILOS"
$categoryCovers = @{}

if (Test-Path $coversDir) {
    $coverFiles = Get-ChildItem -Path $coversDir -Include *.jpg, *.png, *.jpeg, *.webp -Recurse
    foreach ($cover in $coverFiles) {
        $catName = $cover.BaseName
        $relPathRaw = (Resolve-Path -Path $cover.FullName -Relative)
        $relPath = $relPathRaw -replace "^\.\\", "" 
        $relPath = $relPath.Replace("\", "/")
        # FIX: Retain 'assets/' prefix for correct linking in HTML
        # $relPath = $relPath -replace "^assets/", ""
        $categoryCovers[$catName] = $relPath
    }
}

# 3. GENERAR ARCHIVO JS
$header = @"
/**
 * BASE DE DATOS DE OBRAS
 * Generada automaticamente el $(Get-Date -Format "yyyy-MM-dd HH:mm")
 */

// Mapa de Portadas por Estilo
const categoryCovers = {
"@

$coverEntries = @()
foreach ($key in $categoryCovers.Keys) {
    if ($categoryCovers[$key]) {
        $path = $categoryCovers[$key]
        $coverEntries += "    `"$key`": `"$path`""
    }
}
$jsHeader = $header + ($coverEntries -join ",`n") + "`n};`n`n"

# Convertir la lista de obras a JSON de forma segura
# Nota: Forzamos el tipo de 'sold' a booleano real si es string "true"/"false"
foreach ($art in $artworks) {
    if ($art.sold -eq "true" -or $art.sold -eq $true) { $art.sold = $true }
    else { $art.sold = $false }
}

$artworksJson = $artworks | ConvertTo-Json -Depth 5

$finalJs = $jsHeader + "const artworkData = " + $artworksJson + ";"

$finalJs | Set-Content -Path "js/data.js" -Encoding UTF8

Write-Host "✅ Catálogo restaurado con éxito en js/data.js" -ForegroundColor Green
