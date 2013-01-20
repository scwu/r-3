var x = require('casper').selectXPath;
var casper = require('casper').create();
casper.options.viewportSize = {width: 1029, height: 622};
casper.start('http://www.amtrak.com/home');
casper.waitForSelector("form[name=form] input[name='wdf_origin']",
    function success() {
        this.test.assertExists("form[name=form] input[name='wdf_origin']");
        this.click("form[name=form] input[name='wdf_origin']");
    },
    function fail() {
        this.test.assertExists("form[name=form] input[name='wdf_origin']");
});
casper.waitForSelector("form[name=form]",
    function success() {
        this.fill("form[name=form]", {"wdf_origin": "philadelphia"});
    },
    function fail() {
        this.test.assertExists("form[name=form]");
});
casper.waitForSelector("form[name=form] input[name='wdf_destination']",
    function success() {
        this.test.assertExists("form[name=form] input[name='wdf_destination']");
        this.click("form[name=form] input[name='wdf_destination']");
    },
    function fail() {
        this.test.assertExists("form[name=form] input[name='wdf_destination']");
});
casper.waitForSelector("form[name=form]",
    function success() {
        this.fill("form[name=form]", {"wdf_destination": "chicago"});
    },
    function fail() {
        this.test.assertExists("form[name=form]");
});

casper.waitForSelector("form[name=form] input[id='wdf_date1']",
    function success() {
        this.test.assertExists("form[name=form] input[id='wdf_date1']");
        this.click("form[name=form] input[name='wdf_date']");
    },
    function fail() {
        this.test.assertExists("form[name=form] input[id='wdf_date1']");
});

casper.waitForSelector("form[name=form]",
    function success() {
        this.fill("form[name=form]", {"/sessionWorkflow/productWorkflow[@product=\'Rail\']/tripRequirements/journeyRequirements[1]/departDate.date": "Tues, Jan 31, 2013"});
    },
    function fail() {
        this.test.assertExists("form[name=form]");
});



casper.thenClick(x('//div[4]/input'), function() {
	this.echo(this.getHTML());
});
// submit form

casper.run(function() {this.test.renderResults(true);});