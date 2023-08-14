// Refer to this link to intall phantomjs: https://www.vultr.com/docs/how-to-install-phantomjs-on-ubuntu-16-04
// Use 'page.injectJs()' to load the script itself in the Page context

// phantomjs main.js "172.16.1.11:3128" "https://dothi.net/ban-nha-biet-thu-lien-ke-xa-me-tri/ban-biet-thu-mat-ho-10ha-vinhomes-green-bay-cam-ket-gia-chinh-xac-va-tot-nhat-85-ty-0902962999-pr13339818.htm"
"use strict";
if (typeof (phantom) !== "undefined") {
    var page = require('webpage').create();
    var fs = require('fs');
    var system = require('system');
    var proxy = system.args[1];
    var link = system.args[2];
    var result = system.args[3];
    var useragent = system.args[4];
    //var cookieFile = system.args[5];
    
    // get proxy
    if ( proxy != "" ) {
        proxy = proxy.split(":")
        phantom.setProxy(proxy[0], proxy[1], 'manual', '', '');
    }
    // get and set cookies
    // if ( ! cookieFile ) {
    //     cookieFile = "cookieFile.json";
    // }
    var pageResponses = {};
    // set userAgent
    page.settings.userAgent = useragent;
    page.settings.resourceTimeout = 100000;
    // console.log(proxy)
    // console.log(link)
    // console.log(result)
    // console.log(useragent)
    // console.log(cookieFile)

    page.onResourceReceived = function (response) {
        pageResponses[response.url] = response.status;
       // fs.write(cookieFile, JSON.stringify(phantom.cookies), "w");
    };
    // if (fs.isFile(cookieFile))
    //     Array.prototype.forEach.call(JSON.parse(fs.read(cookieFile)), function (x) {
    //         phantom.addCookie(x);
    //     });


    page.open(link, function (status) {
        if (status === "success") {
            console.log(status);
            var content = page.content;
            try {
                fs.write(result, content, 'w');
            } catch (e) {
                console.log(e);
            }
        }
        phantom.exit();
    });
} else {
    alert("* Script running in the Page context.");
}



