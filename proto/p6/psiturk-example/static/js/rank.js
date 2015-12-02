/*global d3, $, window*/
/*global PsiTurk, uniqueId, adServerLoc, mode, replaceBody, condition, counterbalance*/
/*jslint unparam:true */

/* PsiTurk setup */
var psiTurk = new PsiTurk(uniqueId, adServerLoc, mode);
var pages = [
    "instructions/instruct-1.html",
    "instructions/instruct-2.html",
    "instructions/instruct-3-Simplex.html",
    "instructions/instruct-3-BayesOpt.html",
    "instructions/instruct-ready.html",
    "stage.html",
    "aborted.html",
    "success.html",
    "postquestionnaire.html",
];
psiTurk.preloadPages(pages);
var mycondition = condition;  // these two variables are passed by the psiturk server process
var mycounterbalance = counterbalance;  // they tell you which condition you have been assigned to

/* Global configurations */
var iterationIndex = 1;
var exampleIndex = 1;
var optimizationMode;
var maxIterations;
var goalImg;
var abortIterations;  // If you make this larger than maxIterations, no option to abort will be given
var instructionPages = [
    "instructions/instruct-1.html",
    "instructions/instruct-2.html",
];

console.log("Condition:" + mycondition);
console.log("Typeof Condition:" + typeof mycondition);
if (mycondition === '0') {
    optimizationMode = 'BayesOpt';
    maxIterations = 20;
    abortIterations = 30;
} else if (mycondition === '1') {
    optimizationMode = 'Simplex';
    maxIterations = 20;
    abortIterations = 30;
}

if (mycounterbalance === '0') {
    goalImg = '/static/images/cuts/1000ppi_04.png';
} else if (mycounterbalance === '1') {
    goalImg = '/static/images/cuts/32ppi_17.png';
}

instructionPages.push("instructions/instruct-3-" + optimizationMode + ".html");
instructionPages.push("instructions/instruct-ready.html");

/* UI helpers for simplex optimization */

/* A routine to move a D3 object highest in the view order */
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
        .attr('xlink:href', function(d) { return d.img; })
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

/* Questionnaire for the end of the study */
// REUSE: from default psiTurk task.js
var Questionnaire = function() {

    var error_message = "<h1>Oops!</h1><p>Something went wrong submitting your HIT. This might happen if you lose your internet connection. Press the button to resubmit.</p><button id='resubmit'>Resubmit</button>";

    var record_responses = function() {
            psiTurk.recordTrialData({
        phase:'Questionnaire:Submit',
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
        }, error: prompt_resubmit
        });
    };

    // Load the questionnaire snippet 
    psiTurk.showPage('postquestionnaire.html');
    psiTurk.recordTrialData({
        phase: 'Questionnaire:Begin',
        status:'begin'
    });
    
    $("#next").click(function () {
        record_responses();
        psiTurk.saveData({
        success: function(){
            psiTurk.computeBonus('compute_bonus', function() { 
                psiTurk.completeHIT(); // when finished saving compute bonus, the quit
            }); 
        }, 
        error: prompt_resubmit
        });
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

    // Set the goal image
    $('#rank_exemplar_img').attr('src', goalImg);

    // Variables to maintain the state of Bayesian optimization
    var x, f, comparisons, xBest, xNew;

    /* A function to abstract out common logging boilerplate */
    function bayesOptLog(eventName, extras, success) {
        var data = {
            x: x,
            f: f,
            comparisons: comparisons,
        };
        $.extend(data, extras);
        psiTurk.recordTrialData({
            phase: "BayesOpt::" + eventName,
            data: data,
        });
        psiTurk.saveData({success: success});
    }

    /* 
    For Bayesian optimization, update the pair of images based on recent user selection,
    reporting past x and f values and comparisons to the server for picking a new point.
    */
    function updatePair(reqData) {

        // Disable buttons and update the text on them
        $('button.choice_butt').prop('disabled', true);
        var origText = $('button.choice_butt').first().text();
        $('button.choice_butt').text("Waiting for new pair...");

        $.get('/bayesopt', reqData, function(data) {

            x = data.x;
            f = data.f;
            comparisons = data.comparisons;
            xBest = data.xbest;
            xNew = data.xnew;

            loadPair(xNew, xBest);

            // Reset the buttons to their original text
            $('button.choice_butt').prop('disabled', false);
            $('button.choice_butt').text(origText);

            // Show all objects that were hidden for the first round
            $('.hide_first_round').show();

        });

        iterationIndex = iterationIndex + 1;
    
        // Let user abort if they aren't seeing any more improvement
        if (iterationIndex === abortIterations) {
            $('#abort_butt').show();
        // Automatically abort the experiment after a certain number of trials.
        // Server starts to slow down with too many points to compare.
        } else if (iterationIndex > maxIterations) {
            bayesOptLog("Forced End", {}, function() { 
                finish("aborted.html"); 
            });
        }
    }

    if (optimizationMode === 'BayesOpt') {

        // Hide all elements related to simplex method
        $('.simplex').hide();

        // Initialize with a server-chosen pair of points
        updatePair({});

        // When a choice is made, save it as a comparison and update the points.
        $('.choice_butt').click(function() {

            // Add a comparison based on the user's choice
            var xBetter, xWorse;
            if ($(this).attr('id') === 'choice_butt_1') {
                xBetter = xNew;
                xWorse = xBest;
            } else {
                xBetter = xBest;
                xWorse = xNew;
            }
            comparisons.push([xBetter.index, xWorse.index]);
    
            bayesOptLog("Choice", {
                xBest: xBest,
                xNew: xNew,
                xBetter: xBetter,
            });

            // End the experiment when the user has achieved the exemplar
            if (xBetter.img === $('#rank_exemplar_img').attr('src')) {
                bayesOptLog("Success", {
                    xChoice: xBest.value,
                }, function() { finish("success.html"); });
            }

            updatePair({
                x: JSON.stringify(x),
                f: JSON.stringify(f),
                comparisons: JSON.stringify(comparisons)
            });
        });

    } else if (optimizationMode === 'Simplex') {

        // Hide all elements unrelated to the simplex method
        $('.bayesopt').hide();

        // Initialize with a set of server-chosen points
        $.get('/step', {
            points: JSON.stringify([]),
            iteration: iterationIndex,
            get_images: true,
        }, function(data) {
            loadExamples(data.points);   
            iterationIndex = iterationIndex + 1;
        });

        $('#upload_ranking_butt').click(function() {

            var data = d3.selectAll('#rank_bar rect').data();

            // Save current data on vertexes and their rankings
            psiTurk.recordTrialData({
                phase: "Simplex::Choice",
                points: data,
            });
            psiTurk.saveData();

            // End the experiment when the user has achieved the exemplar
            if (data[0].img === $('#rank_exemplar_img').attr('src')) {
                psiTurk.recordTrialData({
                    phase: "Simplex::Success",
                    points: data,
                });
                psiTurk.saveData();
                finish("success.html");
            }

            // Fetch the next set of images from the server based on the current ranking.
            $.get('/step', {
                iteration: iterationIndex,
                points: JSON.stringify(data),
                bounds: JSON.stringify([[0, 4], [0, 4], [0, 4]]),
                get_images: true,
            }, function(data) {

                loadExamples(data.points);

                // Allow the user to quit if they haven't reached the exemplar
                iterationIndex = iterationIndex + 1;
                if (iterationIndex === abortIterations) {
                    $('#abort_butt').show();
                } else if (iterationIndex > maxIterations) {
                    psiTurk.recordTrialData({
                        phase: "Simplex::Forced End",
                        points: data,
                    });
                    psiTurk.saveData({
                        success: function() {
                            finish("aborted.html");
                        }
                    });
                }
            });
        });
    }

    $('#abort_butt').click(function() {
        var data = d3.selectAll('#rank_bar rect').data();
        psiTurk.recordTrialData({
            phase: "All::Aborted",
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
