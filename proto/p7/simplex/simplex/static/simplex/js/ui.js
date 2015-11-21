/*global d3*/
/*jslint unparam:true */

console.log("Hello world!");

var svg = d3.select('#rank_panel')
  .append('svg')
  .attr('width', 400)
  .attr('height', 400);

var boxData = [
  {'rank': 1, 'value': 128}, 
  {'rank': 2, 'value': 64}, 
  {'rank': 3, 'value': 100}, 
  {'rank': 4, 'value': 32}
];

var boxes = svg.selectAll('rect')
  .data(boxData)
  .enter()
    .append('rect')
    .attr('x', function(d, i) { return i * 100; } )
    .attr('width', 100)
    .attr('height', 100)
    .style('fill', function(d) { 
      var v = d.value;
      return 'rgb(' + [v, v, v].join(',') + ')'; 
    });


// REUSE: Based on drag behavior from
// stackoverflow.com/questions/19931307/d3-differentiate-between-click-and-drag-for-an-element-which-has-a-drag-behavior
var drag = d3.behavior.drag()
  .on('drag', function() {
    d3.select(this)
      .attr('x', d3.event.x - d3.select(this).attr('width') / 2)
      .attr('y', d3.event.y - d3.select(this).attr('height') / 2);
  }).on('dragend', function() {
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
    boxes.attr('x', function(d, i) { return i * 100; });
  });
boxes.call(drag);
