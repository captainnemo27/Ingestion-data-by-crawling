const Apify = require('apify');
const randomUA = require('modern-random-ua');
const fs = require('fs');

//node main.js url="https://www.coches.net/segunda-mano/" proxy="172.16.1.11:3128" delay="3" saved_file="test.html"

const args = process.argv.slice(2)

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
    console.log("Error: Url is missed.")
    process.exit(1)
}

(async () => {

    const browser = await Apify.launchPuppeteer({
        headless: true, 
        userAgent: randomUA.generate(),
        slowMo: 250,
        proxyUrl: proxy,
        launchPuppeteerOptions:{
            stealth:true,
        },
    });
    
    // console.log('proxy:' + proxy);
    // console.log('delay:' + delay);
    // console.log('url:' + url);

    
    const page = await browser.newPage();
    await page.setViewport({  
        width: 1024 + Math.floor(Math.random() * 100),
        height: 768 + Math.floor(Math.random() * 100) 
    });
    
    await Apify.utils.puppeteer.hideWebDriver(page);

    // Get current cookies from the page for certain URL
    const cookies = await page.cookies(url);
    // And remove them
    await page.deleteCookie(...cookies);
    
    try {
        await page.goto(url);
        await Apify.utils.sleep(delay * 1000);

        const content = await page.content();

        if (saved_file.length == 0){ // None providing parameter saved_file => display console.log
            console.log(content);

        }else{

            // write content to saved_file
            fs.writeFile(saved_file, content, 'utf8' ,(err) => {
                // throws an error, you could also catch it here
                if (err) throw err;
            });
        }
     

    } catch (err) {
        console.log('ERR:', err.message);
    } finally {
        await browser.close();
    }

   
  })().catch((err) => {
    console.log('Exception program:' + err);
    process.exit(1);
  });
