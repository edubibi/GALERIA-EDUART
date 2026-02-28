const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    page.on('console', msg => console.log('PAGE LOG:', msg.text()));
    await page.goto('http://localhost:8000/visor/index.html?img=..%2Fassets%2Fphotos%2FAMARILLO-GIRASOL_02.jpg&title=Amarillo%20Girasol%2002&category=03_LUMINISCENTE&id=203', {waitUntil: 'networkidle0'});
    await browser.close();
})();
