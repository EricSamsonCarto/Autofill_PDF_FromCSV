
function CSV_PDF() {
	document.getElementById("Loader").style.display = "inline";
	var df_or_CSV = document.getElementById('input_CSV').value;
	var PDF_template = document.getElementById('PDFtemplate').value;
	var output_filename = document.getElementById('out_filename').value;
	console.log(df_or_CSV);
	
	// Cannot read property value of null
	if (document.getElementById('col_key').value == '') {
		var colkey = 'default';
	} else {
		var colkey = document.getElementById('col_key').value;
		
	}
	
	if (document.getElementById('check_fields').value == '') {
		var checkbox_fields = 'default';
	} else {
		var checkbox_fields = document.getElementById('check_fields').value;
	}
	
	//python
	eel.dataframe_to_PDF(df_or_CSV, PDF_template, output_filename, colkey, checkbox_fields) (finished);
}

function finished() {
	document.getElementById("Loader").style.display = "none";
	document.getElementById("complete").style.display = "inline";
}
