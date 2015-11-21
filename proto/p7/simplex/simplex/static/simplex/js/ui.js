/*global d3*/
/*jslint unparam:true */

console.log("Hello world!");

function color(d) { 
  var v = d.value;
  return 'rgb(' + [v, v, v].join(',') + ')'; 
}

var exemplarSvg = d3.select('#exemplar_cont')
  .append('svg')
  .attr('width', 300)
  .attr('height', 300);

exemplarSvg.selectAll('rect')
  .data([{'value': 128}])
  .enter()
    .append('rect')
      .attr('width', 300)
      .attr('height', 300)
      .style('fill', color);

var boxData = [
  {'rank': 1, 'value': 128}, 
  {'rank': 2, 'value': 64}, 
  {'rank': 3, 'value': 100}, 
  {'rank': 4, 'value': 32}
];

var rankSvg = d3.select('#rank_bar')
  .append('svg')
  .attr('width', 100 * boxData.length)
  .attr('height', 100);

var boxes = rankSvg.selectAll('rect')
  .data(boxData)
  .enter()
    .append('rect')
      .attr('x', function(d, i) { return i * 100; } )
      .attr('width', 100)
      .attr('height', 100)
      .style('fill', color);


// REUSE: http://stackoverflow.com/questions/14167863/how-can-i-bring-a-circle-to-the-front-with-d3
d3.selection.prototype.moveToFront = function() {
  return this.each(function(){
    this.parentNode.appendChild(this);
  });
};

function getDisplacedNeighbor(sel) {
    var displaced = d3.selectAll('.nothing');
    boxes.each(function() {
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
    selection
      .attr('x', d3.event.x - d3.select(this).attr('width') / 2)
      .attr('y', d3.event.y - d3.select(this).attr('height') / 2)
      .moveToFront();

    // Highlight nearby box it will replace
    var displaced = getDisplacedNeighbor(selection);
    boxes.style('stroke-width', 0);
    displaced
      .style('stroke-width', 3)
      .style('stroke', 'rgb(166, 166, 255)');

  }).on('dragend', function() {
    
    // Rearrange the boxes based on where the current selection is dragged
    var selection = d3.select(this);
    var origX = selection.attr('x');
    var displaced = getDisplacedNeighbor(selection);
    var newX = displaced.attr('x');
    selection.attr('x', newX);
    displaced.attr('x', origX);

    boxes.each(function() {
      var thisNode = d3.select(this);
      thisNode.datum(function(d) {
        d.x = thisNode.attr('x');
        return d;
      });
    });
    boxes.sort(function(a, b) {
      return a.x - b.x;
    });
    boxes
      .attr('x', function(d, i) { return i * 100; })
      .attr('y', 0)
      .style('stroke-width', 0);

  });
boxes.call(drag);
