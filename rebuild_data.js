const fs = require('fs');
const path = require('path');

const dataPath = path.join(__dirname, 'js', 'data.js');
const stampsSnippetPath = path.join(__dirname, 'stamps_metadata_snippet.json');
const stampsDir = path.join(__dirname, 'assets', 'SELLOS_MAGICOS');

console.log("Starting rebuild of data.js...");

// 1. Read data.js
let contentSync;
try {
    contentSync = fs.readFileSync(dataPath, 'utf8');
} catch (e) {
    console.error("Error reading data.js:", e);
    process.exit(1);
}

// 2. Separate categoryCovers and artworkData
const splitMarker = 'const artworkData =';
const parts = contentSync.split(splitMarker);

if (parts.length < 2) {
    console.error("Could not find 'const artworkData =' in data.js");
    process.exit(1);
}

const header = parts[0];
let dataPart = parts[1].trim();

// Remove trailing semicolon if present
if (dataPart.endsWith(';')) {
    dataPart = dataPart.slice(0, -1);
}

// 3. Parse existing data using eval (handles unquoted keys)
let currentData;
try {
    currentData = eval(dataPart);
} catch (e) {
    console.error("Error parsing existing artworkData:", e);
    process.exit(1);
}

console.log(`Loaded ${currentData.length} existing items.`);

// 4. Filter out old SELLOS
const filteredData = currentData.filter(item => item.category !== 'SELLOS_MAGICOS');
console.log(`After filtering old stamps: ${filteredData.length} items.`);

// 5. Load new stamps metadata
let stampsMeta;
try {
    stampsMeta = JSON.parse(fs.readFileSync(stampsSnippetPath, 'utf8'));
} catch (e) {
    console.error("Error reading stamps metadata:", e);
    process.exit(1);
}

// 6. List actual files
let files;
try {
    files = fs.readdirSync(stampsDir);
} catch (e) {
    console.error("Error reading stamps directory:", e);
    process.exit(1);
}

const fileMap = {};
files.forEach(f => {
    // cover_book.png excluded?
    if (f.includes("cover_book")) return;
    const name = path.parse(f).name;
    fileMap[name] = f;
});

// 7. Create new stamp items
const newStamps = [];
Object.entries(stampsMeta).forEach(([id, info]) => {
    const filename = fileMap[id];
    if (!filename) {
        console.warn(`Warning: File for ID ${id} not found in directory.`);
        return;
    }

    newStamps.push({
        id: id,
        title: info.title,
        category: "SELLOS_MAGICOS",
        src: `assets/SELLOS_MAGICOS/${filename}`,
        description: "Obra de la colección SELLOS_MAGICOS",
        size: "Consultar",
        price: "19,99",
        tech_info: "",
        sold: false
    });
});

console.log(`Adding ${newStamps.length} new stamps.`);

// 8. Combine
const finalData = [...filteredData, ...newStamps];

// 9. Serialize
// We use JSON.stringify. It produces quoted keys, which is valid JS.
const jsonStr = JSON.stringify(finalData, null, 4);

// 10. Reconstruct file
const newContent = header + 'const artworkData = ' + jsonStr + ';';

try {
    fs.writeFileSync(dataPath, newContent, 'utf8');
    console.log("Successfully rebuilt data.js");
} catch (e) {
    console.error("Error writing data.js:", e);
    process.exit(1);
}
