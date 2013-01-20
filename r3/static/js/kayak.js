function runKayak() {
var x = require('casper').selectXPath;
var casper = require('casper').create();
casper.options.viewportSize = {width: 1366, height: 643};
casper.start('http://www.kayak.com/');
casper.then(function() {
    this.mouse.click(356, 116);
});
casper.waitForSelector("form[name=flights]",
    function success() {
        this.fill("form[name=flights]", {"oneway": "y"});
    },
    function fail() {
        this.test.assertExists("form[name=flights]");
});
casper.waitForSelector("form[name=flights] input[name='oneway']",
    function success() {
        this.test.assertExists("form[name=flights] input[name='oneway']");
        this.click("form[name=flights] input[name='oneway']");
    },
    function fail() {
        this.test.assertExists("form[name=flights] input[name='oneway']");
});
casper.waitForSelector("form[name=flights] input[name='destination']",
    function success() {
        this.test.assertExists("form[name=flights] input[name='destination']");
        this.click("form[name=flights] input[name='destination']");
    },
    function fail() {
        this.test.assertExists("form[name=flights] input[name='destination']");
});
casper.then(function() {
    this.mouse.click(554, 213);
});
casper.waitForSelector("form[name=flights] input[name='comparetosite']",
    function success() {
        this.test.assertExists("form[name=flights] input[name='comparetosite']");
        this.click("form[name=flights] input[name='comparetosite']");
    },
    function fail() {
        this.test.assertExists("form[name=flights] input[name='comparetosite']");
});
casper.waitForSelector("form[name=flights]",
    function success() {
        this.fill("form[name=flights]", {"comparetosite": "PRICLINE_FDCMP2"});
    },
    function fail() {
        this.test.assertExists("form[name=flights]");
});
casper.waitForSelector("form[name=flights] input[name='comparetosite']",
    function success() {
        this.test.assertExists("form[name=flights] input[name='comparetosite']");
        this.click("form[name=flights] input[name='comparetosite']");
    },
    function fail() {
        this.test.assertExists("form[name=flights] input[name='comparetosite']");
});
casper.then(function() {
    this.mouse.click(342, 600);
});

casper.then(function() {
	var html = this.getHTML());
    
});

casper.run(function() {this.test.renderResults(true);});
}