jQuery(document).ready(function ($) {
	var tmp = $("input[name=trainmetricname]");
	var selectors;
	if (tmp.length == 0) {
		selectors = $("input[name=target], input[name=metricname], input[name=type]");
	} else {
		selectors = $("input[name=target], input[name=trainmetricname], input[name=testmetricname], input[name=type]");
	}
	ShowTables(selectors);
	selectors.on("change", function(e) {
		ShowTables(selectors);
	})
});
