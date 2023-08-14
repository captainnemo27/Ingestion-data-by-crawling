const puppeteer = require('puppeteer-extra')
const UserAgent = require('user-agents');
const fs = require('fs');
//Enable stealth mode
const StealthPlugin = require('puppeteer-extra-plugin-stealth')
puppeteer.use(StealthPlugin())

const USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36';

const args = process.argv.slice(2)

// Run: npm install puppeteer-extra user-agents puppeteer-extra-plugin-stealth fs puppeteer
//   node batdongsancomvn.js url="https://batdongsan.com.vn/" proxy="172.16.1.11:3128" delay="5" saved_file="test.html" 
//default value
let url = '';
let delay = 3;
let proxy = '';
let saved_file = '';

args.forEach((val, index) => {
    // console.log(`${index}: ${val}`)

    if(val.startsWith("url=")){
        url = val.replace("url=",""); 
    }
    else if(val.startsWith("proxy=")){
        proxy = 'http://' + val.replace("proxy=","").replace("http://",""); 
    }
    else if(val.startsWith("delay=")){
        delay = val.replace("delay=",""); 
    }
    else if(val.startsWith("saved_file=")){
        saved_file = val.replace("saved_file=","");
    }
});

if ( url.length == 0 ) {
    console.log("Error: id_client is missed.")
    process.exit(1)
}

async function createPage (browser,url) {
    //Randomize User agent or Set a valid one
    const userAgent = new UserAgent();
    const UA = userAgent.toString() || USER_AGENT;
    const [page] = await browser.pages()

    //Randomize viewport size
    page.setViewport({
        width: 1920 + Math.floor(Math.random() * 100),
        height: 3000 + Math.floor(Math.random() * 100),
        deviceScaleFactor: 1,
        hasTouch: false,
        isLandscape: false,
        isMobile: false,
    });
    page.setUserAgent(UA);
    page.setJavaScriptEnabled(false);
    page.setDefaultNavigationTimeout(0);


    await page.setRequestInterception(true);
    //Skip images/styles/fonts loading for performance
    page.on('request', (req) => {
        if(req.resourceType() == 'stylesheet' || req.resourceType() == 'font' || req.resourceType() == 'image'){
            req.abort();
        } else {
            req.continue();
        }
    });

    await page.evaluateOnNewDocument(() => {
        // Pass webdriver check
        Object.defineProperty(navigator, 'webdriver', {
            get: () => false,
        });
    });

    await page.evaluateOnNewDocument(() => {
        // Pass chrome check
        window.chrome = {
            runtime: {},
            // etc.
        };
    });

    await page.evaluateOnNewDocument(() => {
        //Pass notifications check
        const originalQuery = window.navigator.permissions.query;
        return window.navigator.permissions.query = (parameters) => (
            parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
        );
    });

    await page.evaluateOnNewDocument(() => {
        // Overwrite the `plugins` property to use a custom getter.
        Object.defineProperty(navigator, 'plugins', {
            // This just needs to have `length > 0` for the current test,
            // but we could mock the plugins too if necessary.
            get: () => [1, 2, 3, 4, 5],
        });
    });

    // await page.evaluateOnNewDocument(() => {
    //     // Overwrite the `languages` property to use a custom getter.
    //     Object.defineProperty(navigator, 'languages', {
    //         get: () => ['en-US', 'en'],
    //     });
    // });
    
    // networkidle0 - consider navigation to be finished when there are no more than 0 network connections for at least 500 ms
    await page.goto(url);
    await page.waitForTimeout(delay * 1000);
    return page;
}
(async () => {

    const browser = await puppeteer.launch({
        headless: true, 
        userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36",
        //slowMo: 88,
       // proxyUrl: proxy,
        args: [ '--no-sandbox',
             '--disable-setuid-sandbox',
             '--start-maximized',
             '--disable-web-security', 
             '--disable-features=IsolateOrigins,site-per-process', 
             `--proxy-server=${proxy}`,
             '--user-data-dir=./.config/google-chrome'], 
        ignoreHTTPSErrors: true,
    });


    try {
	  //  console.log(proxy);
        const page = await createPage(browser,url)
        const content = await page.content();
        

        if (saved_file.length == 0){ // None providing parameter saved_file => display console.log
            console.log(content);

        }else{

            // write content to saved_file
            await fs.writeFile(saved_file, content, 'utf8' ,(err) => {
                // throws an error, you could also catch it here
                if (err) throw err;
            });
        }
        

    } catch (err) {
        console.log('ERR:', err.message);
    } finally {
        await browser.close();
        process.exit(0);
    }

    
    })().catch((err) => {
    console.log('Exception program:' + err);
    process.exit(0);
    });
