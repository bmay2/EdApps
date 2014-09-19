<link href="{{ STATIC_URL }}egorkhmelev-jslider-012b599/css/jslider.css" type="text/css" rel="Stylesheet" />
<link href="{{ STATIC_URL }}egorkhmelev-jslider-012b599/css/jslider.blue.css" type="text/css" rel="Stylesheet" />
<link href="{{ STATIC_URL }}egorkhmelev-jslider-012b599/css/jslider.plastic.css" type="text/css" rel="Stylesheet" />
<link href="{{ STATIC_URL }}egorkhmelev-jslider-012b599/css/jslider.round.css" type="text/css" rel="Stylesheet" />
<link href="{{ STATIC_URL }}egorkhmelev-jslider-012b599/css/jslider.round.plastic.css" type="text/css" rel="Stylesheet" />

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.8.0/jquery.min.js" type="text/javascript"></script>
<script src="//ajax.googleapis.com/ajax/libs/jqueryui/1.8.23/jquery-ui.min.js" type="text/javascript"></script>

<script src="{{ STATIC_URL }}egorkhmelev-jslider-012b599/js/jshashtable-2.1_src.js" type="text/javascript"></script>
<script src="{{ STATIC_URL }}egorkhmelev-jslider-012b599/js/jquery.numberformatter-1.2.3.js" type="text/javascript"></script>
<script src="{{ STATIC_URL }}egorkhmelev-jslider-012b599/js/tmpl.js" type="text/javascript"></script>
<script src="{{ STATIC_URL }}egorkhmelev-jslider-012b599/js/jquery.dependClass-0.1.js" type="text/javascript"></script>
<script src="{{ STATIC_URL }}egorkhmelev-jslider-012b599/js/draggable-0.1.js" type="text/javascript"></script>
<script src="{{ STATIC_URL }}egorkhmelev-jslider-012b599/js/jquery.slider.js" type="text/javascript"></script>

<script language="javascript" type="text/javascript">
$(document).ready(function() {
	$('form > ul').css({'font-size': '15px', 'list-style-type': 'none', 'float': 'left'});
	$("#price_slide").slider(
    {
	    from: 0,
	    to: 300,
	    heterogeneity: ['50/20', '75/50'],
	    scale: [0, '|', 10, '|', 20, '|' , 50, '|', 300],
	    limits: false,
	    step: 1,
	    dimension: '&nbsp;$'
    });
    var values = $("#price_slide").slider("value").split(';');
    var lower = values[0];
    var upper = values[1];
    var values_list = [];
	console.log(lower);
	console.log(upper);
});
</script>

