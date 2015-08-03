
function ShowTables(selectors) {
	var checked = selectors.filter(function() {
		return $(this).is(":checked")
	}).get();
	var myvalues = checked.map(function(entry) { return(entry.value); });
	var showid = myvalues.join('_');
	var summaryid = showid + '_summary';
	var divs = document.getElementsByClassName("AbedTable");
	var showdiv = 'div_' + showid;
	var summdiv = 'div_' + summaryid;
	for (i=0; i<divs.length; i++) {
		if (divs[i].id != showdiv && divs[i] != summdiv) {
			$(divs[i]).hide();
		}
	}
	$('#' + showdiv).show();
	var t1 = $('#tbl_' + showid).dataTable( {
		"dom": "lrtp",
		"retrieve": true,
		"searching": true,
		"scrollY": "45vh",
		"scrollX": "100%",
		"scrollCollapse": true,
		"paging": false,
		"ajax": 'ABED_' + showid + '_ajax.txt',
		initComplete: function() {
			this.api().columns().every(function() {
				var column = this;
				var select = $('<select><option value=""></option></select>')
					.appendTo( $(column.footer()).empty() )
					.on( 'change', function() {
						var val = $.fn.dataTable.util.escapeRegex(
								$(this).val()
								);
						column
							.search( val ? '^'+val+'$' : '', true, false)
							.draw();
					});
				column.data().unique().sort().each( function(d, j) {
					select.append('<option value="'+d+'">'+d+'</option>')
				} );
			});
		}
	} );
	$('#' + summdiv).show();
	var t2 = $('#tbl_' + summaryid).dataTable( {
		"retrieve": true,
		"ajax": 'ABED_' + summaryid + '_ajax.txt',
		"paging": false,
		"info": false,
		"ordering": false,
		"searching": false
	});
}
