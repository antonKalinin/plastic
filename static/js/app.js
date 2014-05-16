$(function() {
    var margin = {top: 20, right: 20, bottom: 30, left: 100},
        width = 960 - margin.left - margin.right,
        height = 5000 - margin.top - margin.bottom;

    var x = d3.scale.linear()
        .range([0, width]);

    var y = d3.scale.ordinal()
        .rangeRoundBands([0, height], .1);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("bottom")
        .ticks(10, ".");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("left");

    var svg = d3.select(".chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    d3.json("/api", function(error, data) {
        x.domain([0, d3.max(data, function(d) { return d.count; })]);
        y.domain(data.map(function(d) { return d.lang; }));

        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis)
            .append("text")
            .attr("x", -10)
            .attr("dy",".85em")
            .style("text-anchor", "end")
            .text("Files");

        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis)
            .append("text")
            .attr("x", -10)
            .attr("dy",".85em")
            .style("text-anchor", "end")
            .text("Languages");

        var dy = 10;

        svg.selectAll(".bar")
            .data(data)
            .enter().append("rect")
            .attr("class", "bar")
            .attr("x", 0)
            .attr("width", function(d) { return x(d.count); })
            .attr("y", function(d) { return y(d.lang); })
            .attr("height", y.rangeBand());
    });
});