<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js" type="text/javascript"></script>

<script language="javascript" type="text/javascript">
	var g_numRows;
	var g_numCells;

	$(document).ready(function () {
	    $('#inputNumRowsSubmit').click(function() {
	        var inputNumRows = $('#inputNumRows').val();
	        if (isValidNumber(inputNumRows)) {
	        	numRowsPromptFadeOut();
		        setNumRows(inputNumRows);
		        numCellsPromptFadeIn();
	        }
	        else {
	        	alert('That is not a valid number!');
	        }
	    });
	    
	    $('#inputNumCellsSubmit').click(function() {
	        var inputNumCells = $('#inputNumCells').val();
	        if (isValidNumber(inputNumCells)) {
		        numCellsPromptFadeOut();
		        setNumCells(inputNumCells);
	        	generateHtmlTable(g_numRows, g_numCells);
	        }
	        else {
	        	alert('That is not a valid number!');
	        }
	    });
	    
	    numRowsPromptFadeIn();
	});

	function isValidNumber(input) {
	    var regExpr = new RegExp("^([1-9]|[1-2][0-5])$");
	    return regExpr.test(input);
	}

	function setNumRows(numRows) {
	    g_numRows = numRows;
	}

	function setNumCells(numCells) {
	    g_numCells = numCells;
	}

	function numRowsPromptFadeIn(numRows) {
		$('#inputNumRowsLabel').fadeIn('slow');
	    $('#inputNumRows').fadeIn('slow');
	    $('#inputNumRowsSubmit').fadeIn('slow');
	}

	function numRowsPromptFadeOut() {
	    $('#inputNumRowsLabel').fadeOut('slow');
	    $('#inputNumRows').fadeOut('slow');
	    $('#inputNumRowsSubmit').fadeOut('slow');
	}

	function numCellsPromptFadeIn() {
		$('#inputNumCellsLabel').fadeIn('slow');
	    $('#inputNumCells').fadeIn('slow');
	    $('#inputNumCellsSubmit').fadeIn('slow');
	}

	function numCellsPromptFadeOut() {
		$('#inputNumCellsLabel').fadeOut('slow');
	    $('#inputNumCells').fadeOut('slow');
	    $('#inputNumCellsSubmit').fadeOut('slow');
	}

	function generateHtmlTable(numRows, numCells) {
	    $('div#content').append($('<table></table>',{'id':'table1'}));
	    generateRows(numRows, numCells);
	}

	function generateRows(numRows, numCells) {
	    for (var row_index = 0; row_index < numRows; row_index++) {
	        $('#table1').append($('<tr></tr>',{'id':'row'+row_index}));
	        generateCells(row_index, numCells);
	    }
	}

	function generateCells(row_index, numCells) {
	    for (var cell_index = 0; cell_index < numCells; cell_index++) {
	        $('#row'+row_index).append($('<td></td>',{'id':'row'+row_index+'_cell'+cell_index}));
	        $('#row'+row_index+'_cell'+cell_index).append($('<input/>',{'id':'row'+row_index+'_input'+cell_index}));
	    }
	}
</script>

