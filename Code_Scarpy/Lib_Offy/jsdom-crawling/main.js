const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const randomUA = require('modern-random-ua');
const fs = require('fs');
const { Script } = require("vm");

//node main.js url="https://whatismyipaddress.com/ip-lookup" proxy="ykgjbdff-rotate:qrhyeh11wwmp@p.webshare.io:80" saved_file="test.html"

const args = process.argv.slice(2)

//default value
let url = '';
let cus_proxy = '';
let saved_file = '';

args.forEach((val, index) => {
    // console.log(`${index}: ${val}`)

    if(val.startsWith("url=")){
        url = val.replace("url=",""); 
    }
    else if(val.startsWith("proxy=")){
      cus_proxy = 'http://' + val.replace("proxy=","").replace("http://",""); 
    }
    else if(val.startsWith("saved_file=")){
        saved_file = val.replace("saved_file=","");
    }

});

if ( url.length == 0 ) {
    console.log("Error: Url is missed.")
    process.exit(1)
}

const resourceLoader = new jsdom.ResourceLoader({
    proxy: cus_proxy,
    strictSSL: false,
    userAgent: randomUA.generate()
  });

const options={
	resources: resourceLoader,
  includeNodeLocations: true,
  pretendToBeVisual: true,
  // resources: "usable",
  runScripts: "dangerously"

}

JSDOM.fromURL(url, options ).then(dom => {
    content = dom.serialize();
    try {
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
      dom.window.close()
    }

}).catch((err) => {
  console.log('Exception program:' + err);
  process.exit(1);
});

