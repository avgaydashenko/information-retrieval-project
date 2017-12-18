var sys = arbor.ParticleSystem();
sys.parameters({
	repulsion: 10,
	stiffness:0.1,
	dt:0.1,
    precision:0
});
$(document).ready(function () {
	var t = document.getElementById('viewport');
	t.height = $(window).height() - 80;
	t.width = $(window).width() - 20;
    sys.eachNode(function(node) { node._mass = sys.getEdgesFrom(node).concat(sys.getEdgesTo(node)).length});

});
sys.renderer = Renderer("#viewport") ;
sys.graft(data);

(function () {

})();

var canvas = $('#viewport');
var selectedNode = null;

canvas.mousemove(handleMouseMoveAndDown);
canvas.mousedown(handleMouseMoveAndDown);
$('#searchForm').submit(search);

function search(e) {	
	e.preventDefault();
	var searchString = $('#searchInput').val();
	var searchResult = sys.getNode(searchString);
	if (searchResult !== undefined) {
		focusOnNode(searchResult);
	} else {
		alert('Nothing found');
	}
}


function handleMouseMoveAndDown(e) {
    //e.originalEvent.type to differ current event
    var pos = canvas.offset();
    var s = arbor.Point(e.pageX-pos.left, e.pageY-pos.top);
    var selectedVertex = sys.nearest(s);
    if (selectedVertex !== null) {
    	var node = selectedVertex.node;
    	focusOnNode(node);
    }
};


function focusOnNode(node) {
	unfocusOnNode(selectedNode);
	if (node === null) {
		return;
	}
	var edges = sys.getEdgesFrom(node).concat(sys.getEdgesTo(node));
	edges.forEach(function (edge) {
		if (edge.source !== node) {
			colorNode(edge.source, 'orange');
		} else {
            colorNode(edge.target, 'orange');
        }
	});
	edges.forEach(focusOnEdge);
    colorNode(node, 'red');
	selectedNode = node;
}

function unfocusOnNode(node) {
	if (node === null) {
		return;
	}
	var edges = sys.getEdgesFrom(node).concat(sys.getEdgesTo(node));
	edges.forEach(unfocusOnEdge);
}

function colorNode(node, color) {
    sys.tweenNode(node, 0, {
        'label':'  ' + node.name + '  ',
        'color' : color
    });
}

function uncolorNode(node) {
    sys.tweenNode(node, 0, {
        'label':'',
        'color': 'rgba(0,0,0,.2)'
    });
}

function focusOnEdge(edge) {
	sys.tweenEdge(edge, 0, {'color':'red', 'weight': 3});
}

function unfocusOnEdge(edge) {
	uncolorNode(edge.source);
	uncolorNode(edge.target);
	sys.tweenEdge(edge, 0, {'color':'rgba(230, 230, 230, 0.1)'});
}

function generateGraph(vertexCount) {
    for (var nodeName = 0; nodeName < vertexCount; nodeName++) {
        sys.addNode(nodeName.toString(), {'shape':'dot', 'color':getRandomColor()});
    }
    var edgesCount = getRandomInt(vertexCount, vertexCount);
    var edges = new Set([]);
    for (var i = 0; i < edgesCount; i++) {
    	var n1 = getRandomInt(0, vertexCount - 1);
    	var n2 = getRandomInt(0, vertexCount - 1);
    	var from = Math.min(n1, n2).toString();
    	var to = Math.max(n1, n2).toString()
    	var edge = {
            from:from,
            to:to,
			data: {
            	directed: false
			}
    	};
    	if (!edges.has(edge) && !(from == to)) {
    		edges.add(edge);
    		sys.addEdge(from, to, {'color':'#e6e6e6'});
    	}

    }
}

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min)) + min;
}

function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++) {
        color += letters[Math.round(Math.random() * 15)];
    }
    return color;
}