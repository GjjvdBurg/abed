jQuery(document).ready(function ($) {
	divs = document.querySelectorAll(".AbedRanks");
	var chart;
	var chartdata;
	for (i=0; i<divs.length; i++) {
		var selector = divs[i].id;
		d3.json(divs[i].id + ".json", json_callback_fn(selector));
	}
});

// found this beautiful trick here:
// https://groups.google.com/forum/#!topic/d3-js/9dvJ8PLEcd4
function json_callback_fn(selector)
{
	var chartdata;
	var cb = function(error, json) {
		if (error) return console.warn(error);
		chartdata = json;
		chart = createRankChart(selector, chartdata.length);
		chart.data(chartdata);
	}
	return cb;
}

function createRankChart(selector, len) {
	var colorScale = d3.scale.category10();

	function color(d) {
		return colorScale(d.name);
	}

	var chart = new d3Kit.Timeline('#' + selector, {
		direction: 'up',
		initialWidth: 804,
		initialHeight: 120,
		scale: d3.scale.linear(),
		domain: [1.0, len],
		margin: {left: 20, right: 20, top: 20, bottom: 20},
		textFn: function(d) { return d.name; },
		layerGap: 40,
		dotColor: color,
		labelBgColor: color,
		linkColor: color,
		labella: {
			maxPos: 764,
			algorithm: 'simple'
		}
	});

	return chart;
}
