const fs = require('fs');
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

function read_cookies(filePath, cookieType) {
  try {
    const data = fs.readFileSync(filePath, 'utf8');
    const cookies = JSON.parse(data);
    return cookies[cookieType];
  } catch (err) {
    console.error(err);
  }
}

function delay(time) {
  return new Promise(resolve => setTimeout(resolve, time));
}

async function getRecaptchaPic(cookies, start,times) {
  const browser = await chromium.launch({ headless: true });

  try {
    const page = await browser.newPage();
    await page.context().addCookies(cookies);
  
    await page.goto("https://sys.ndhu.edu.tw/gc/sportcenter/SportsFields/Default.aspx", { waitUntil: 'networkidle' });
    await page.click('#MainContent_Button2');
    await page.waitForTimeout(1000);
    await page.selectOption('#MainContent_drpkind', '6');
    await page.waitForTimeout(1000);
    await page.selectOption('#MainContent_DropDownList1', 'BSK02');
    await page.waitForTimeout(1000);
    await page.click('#MainContent_Button1');
    await page.waitForTimeout(1000);
    await page.click('button:has-text("[申請]06~08")');
    await page.waitForTimeout(1000);

    for(iter = start;iter < start+times;iter += 1)
    {
      const base64Image = await page.evaluate(() => {
        const img = document.getElementById('imgCaptcha');
        return img.src.split(',')[1]; // Extract the base64 part after 'data:image/jpeg;base64,'
      });

      // Decode the base64 string and save it as an image file
      fs.writeFileSync(`./Data/Pics/Ndhu/captcha${iter}.jpg`, Buffer.from(base64Image, 'base64'));
      await delay(200);
      await page.click('button[onclick="refreshCaptcha()"]');
      await delay(300);
    }

  } catch (error) {
    console.error("An error occurred:", error);
  } finally {
    await browser.close();
  }
}

const cookies = read_cookies('./Data/Credential/cookies.json', 'ndhu');

(async () => {
  await getRecaptchaPic(cookies, 0, 1000);
  console.log('All done. Have a nice day ✨');
})();
