// Use 'page.injectJs()' to load the script itself in the Page context

"use strict";
if ( typeof(phantom) !== "undefined" ) {
    var page = require('webpage').create();
    var fs = require('fs');
    var system = require('system');
    var args = require('system').args;

    var link = system.args[1];
    var result = system.args[2];
    
    page.open(link, function(status) {
        if ( status === "success" ) {
            console.log(status); 
            var content = page.content; 
            //console.log('Content: ' + content); 

            try {
                fs.write(result, content,{
                    mode: 'w',
                    charset: 'UTF-8'
                });
               
            } catch(e) {
                console.log(e);
            }
        }
        phantom.exit();
    });
} else {
    alert("* Script running in the Page context.");
}


