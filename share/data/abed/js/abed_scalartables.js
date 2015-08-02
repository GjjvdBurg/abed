
jQuery(document).ready(function ($) {
	var selectors = $("input[name=target], input[name=type]");
	ShowTables(selectors);
	selectors.on("change", function(e) {
		ShowTables(selectors);
	})
});
