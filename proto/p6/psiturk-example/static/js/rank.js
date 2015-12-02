/*global d3, $, window*/
/*global PsiTurk, uniqueId, adServerLoc, mode, replaceBody*/
/*jslint unparam:true */

/* GLOBALS */

var OPTIMIZATION_MODE = 'BayesOpt';
var DIM_MODE = '2D';
var ABORT_ITERATIONS = 10;
var iterationIndex = 1;
var exampleIndex = 1;

var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);
var pages = [
    "instructions/instruct-1.html",
    "instructions/instruct-2.html",
    "instructions/instruct-3.html",
    "instructions/instruct-ready.html",
    "stage.html",
    "aborted.html",
    "success.html",
    "postquestionnaire.html",
];
var instructionPages = [
    "instructions/instruct-1.html",
    "instructions/instruct-2.html",
    "instructions/instruct-3.html",
    "instructions/instruct-ready.html"
];
psiTurk.preloadPages(pages);

/* HELPERS */

// REUSE: http://stackoverflow.com/questions/14167863/how-can-i-bring-a-circle-to-the-front-with-d3
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

function appearance(selection) {
    selection
      .style('fill-opacity', 0)
      .style('stroke', 'black')
      .style('stroke-width', 2);
    d3.select('svg').selectAll('text')
      .data(selection.data())
      .enter()
        .append('text')
        .attr('transform', 'translate(10,25)')
        .style('stroke-width', 1)
        .style('font-size', 20)
        .style('stroke', 'black')
        .style('fill', 'white')
        .style('font-family', 'Helvetica')
        .text(function(d) { return d.index; });
    d3.select('svg').selectAll('image')
      .data(selection.data())
      .enter()
        .append('image')
        .attr('xlink:href', function(d) { console.log(d); return d.img; })
        .attr('width', 100)
        .attr('height', 100)
        .on('click', function() {
            d3.event.preventDefault();
        });
}

function move(selection, x, y) {

    selection.attr('x', x);
    if (y !== undefined) {
        selection.attr('y', y);
    }

    function getMatchingElement(box, type) {
        var element;
        d3.selectAll('#rank_panel ' + type).each(function(d) {
          if (d.index === box.datum().index) {
              element = d3.select(this);   
          }
        });
        return element;
    }

    selection.each(function() {
      var box = d3.select(this);
      var text = getMatchingElement(d3.select(this), 'text');
      var image = getMatchingElement(d3.select(this), 'image');
      image
        .attr('x', box.attr('x'))
        .attr('y', box.attr('y'))
        .moveToFront();
      text
        .attr('x', box.attr('x'))
        .attr('y', box.attr('y'))
        .moveToFront();
    });
    
    selection.moveToFront();

}

/* DISPLAY THE GOAL */

/* MANIPULATE THE EXAMPLES */

function getDisplacedNeighbor(sel) {
    var displaced = d3.selectAll('.nothing');
    d3.selectAll('#rank_bar rect').each(function() {
      var neighbor = d3.select(this);
      if (neighbor.node() !== sel.node()) {
        if (Math.abs(neighbor.attr('x') - sel.attr('x')) < 50) {
           displaced = neighbor;
        }
      }
    });
    return displaced;
}

/* Drag and snap boxes within a line */
// REUSE: Based on drag behavior from
// stackoverflow.com/questions/19931307/d3-differentiate-between-click-and-drag-for-an-element-which-has-a-drag-behavior
var drag = d3.behavior.drag()
  .on('drag', function() {

    // Move the box
    var selection = d3.select(this);
    selection.call(move,
        d3.event.x - d3.select(this).attr('width') / 2,
        d3.event.y - d3.select(this).attr('height') / 2);

    // Highlight nearby box it will replace
    var displaced = getDisplacedNeighbor(selection);
    d3.selectAll('#rank_bar rect')
      .style('stroke', 'black')
      .style('stroke-width', 2);
    displaced
      .style('stroke-width', 3)
      .style('stroke', 'rgb(166, 166, 255)');

  }).on('dragend', function() {
    
    // Rearrange the boxes based on where the current selection is dragged
    var selection = d3.select(this);
    var displaced = getDisplacedNeighbor(selection);
    var newX = displaced.attr('x') - 10;
    selection.call(move, newX);

    var boxes = d3.selectAll('#rank_bar rect');
    boxes.each(function(d, i) {
      d.x = $(this).attr('x');
    });
    boxes.sort(function(a, b) {
      return a.x - b.x;
    });
    boxes
      .call(move, function(d, i) { return i * 100; }, 0)
      .datum(function(d, i) { 
        d.origX = d3.select(this).attr('x');
        d.rank = i;
        return d; 
      })
      .style('stroke', 'black')
      .style('stroke-width', 2);

  });

/* LOAD THE EXAMPLES */

function makeData(points) {
    var i, p, highestRank = 0;
    for (i = 0; i < points.length; i++) {
        p = points[i];
        if (p.rank !== undefined && p.rank > highestRank) {
            highestRank = p.rank;
        } else {
            p.rank = highestRank + 1;
            highestRank += 1;
        }
        if (p.index === undefined) {
            p.index = exampleIndex;
            exampleIndex = exampleIndex + 1;
        }
        if (p.type === undefined) {
            p.type = "vertex";
        }
    }
    return points;
}

function loadExamples(points) {

    var data = makeData(points);

    d3.select('#rank_bar svg').remove();
    var rankSvg = d3.select('#rank_bar')
      .append('svg')
      .attr('width', 100 * data.length)
      .attr('height', 100);

    var boxes = rankSvg.selectAll('rect')
      .data(data)
      .enter()
        .append('rect')
          .call(appearance)
          .attr('width', 100)
          .attr('height', 100)
          .datum(function(d) { 
            d.origX = d3.select(this).attr('x');
            return d; 
          })
          .call(move, function(d, i) { return i * 100; })
          .call(drag);

    return boxes;
}

// REUSE: from default psiTurk task.js
var Questionnaire = function() {

	var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

	var record_responses = function() {
		psiTurk.recordTrialData({
            phase:'postquestionnaire',
            status:'submit'
        });
		$('textarea').each(function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);
		});
		$('select').each(function(i, val) {
			psiTurk.recordUnstructuredData(this.id, this.value);		
		});
	};

	var prompt_resubmit = function() {
            replaceBody(error_message);
            $("#resubmit").click(resubmit);
	};

	var resubmit = function() {
		replaceBody("<h1>Trying to resubmit...</h1>");
		var reprompt = setTimeout(prompt_resubmit, 10000);
		psiTurk.saveData({
			success: function() {
			    clearInterval(reprompt); 
                psiTurk.computeBonus('compute_bonus', function() { 
                    new Questionnaire(); 
                }); 
			}, 
			error: prompt_resubmit
		});
	};

	// Load the questionnaire snippet 
	psiTurk.showPage('postquestionnaire.html');
	psiTurk.recordTrialData({'phase':'postquestionnaire', 'status':'begin'});
	
	$("#next").click(function () {
	    record_responses();
	    psiTurk.saveData({
            success: function(){
                psiTurk.computeBonus('compute_bonus', function() { 
                	psiTurk.completeHIT(); // when finished saving compute bonus, the quit
                }); 
            }, 
            error: prompt_resubmit});
	});
    
	
};

function finish(pageName) {
    psiTurk.showPage(pageName);
    $('#next').click(function() {
        new Questionnaire();
    });
}

function loadPair(xNew, xBest) {
    $('#bayes_img_1').attr('src', xNew.img);
    $('#bayes_img_2').attr('src', xBest.img);
}

function init() {

    // For use by Bayesian Optimization
    var x, f, comparisons, xBest, xNew;
    function updatePair(reqData) {
        $.get('/bayesopt', reqData, function(data) {
            x = data.x;
            f = data.f;
            console.log("x:" + x);
            console.log("f:" + f);
            comparisons = data.comparisons;
            xBest = data.xbest;
            xNew = data.xnew;
            loadPair(xNew, xBest);
        });
        iterationIndex = iterationIndex + 1;
        if (iterationIndex > ABORT_ITERATIONS) {
            $('#abort_butt').show();
        }
    }

    if (OPTIMIZATION_MODE === 'BayesOpt') {

        $('.simplex').hide();
        updatePair({});
        $('.choice_butt').click(function() {
            if ($(this).attr('id') === 'choice_butt_1') {
                comparisons.push([xNew.index, xBest.index]);
            } else {
                comparisons.push([xBest.index, xNew.index]);
            }
            updatePair({
                x: JSON.stringify(x),
                f: JSON.stringify(f),
                comparisons: JSON.stringify(comparisons)
            });
        });

    } else if (OPTIMIZATION_MODE === 'NelderMead') {
        $('.bayesopt').hide();
        $.get('/step', {
            points: JSON.stringify([]),
            iteration: iterationIndex,
            get_images: true,
        }, function(data) {
            loadExamples(data.points);   
            iterationIndex = iterationIndex + 1;
        });
    }

    $('#upload_ranking_butt').click(function() {
        var data = d3.selectAll('#rank_bar rect').data();
        psiTurk.recordTrialData({
            phase: "ranking",
            points: data,
        });
        psiTurk.saveData();

        if (data[0].img === $('#exemplar_img').attr('src')) {
            psiTurk.recordTrialData({
                phase: "final ranking",
                points: data,
            });
            psiTurk.saveData();
            finish("success.html");
        }

        var query = {
            iteration: iterationIndex,
            points: JSON.stringify(data),
            bounds: JSON.stringify([[0, 4], [0, 4], [0, 4]]),
            get_images: true,
        };
        $.get('/step', query, function(data) {
            loadExamples(data.points);
            iterationIndex = iterationIndex + 1;
            if (iterationIndex > ABORT_ITERATIONS) {
                $('#abort_butt').show();
            }
        });

    });

    $('#abort_butt').click(function() {
        var data = d3.selectAll('#rank_bar rect').data();
        psiTurk.recordTrialData({
            phase: "abort ranking",
            points: data,
        });
        psiTurk.saveData({
            success: function() {
                finish("aborted.html");
            }
        });
    });

}


$(window).load( function(){
    psiTurk.doInstructions(
    	instructionPages, // a list of pages you want to display in sequence
    	function() { 
            psiTurk.showPage('stage.html');
            init();
        }
    );
});
