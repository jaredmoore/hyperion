//    var graphData = {{ data.chart_data | safe }}

    // Set the dimensions of the svg
    var margin = {top: 30, right: 50, bottom: 80, left: 50};
    var svgWidth = 600;
    var svgHeight = 300;
    var graphWidth = svgWidth - margin.left - margin.right;
    var graphHeight = svgHeight - margin.top - margin.bottom;

    // Parse the date / time
    //var parseDate = d3.time.format("%Y-%m-%d").parse;
    var parseDate = d3.isoParse;

    // Set the ranges
    var x = d3.time.scale().range([0, graphWidth]);
    var y = d3.scale.linear().range([graphHeight, 0]);

    // Define the axes
    var xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5)
	.tickFormat(d3.time.format("%Y-%m-%d"));
    var yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

    // Define the temp line
    var tempLine = d3.svg.line()
        .x(function(d) { return x(d.time); })
        .y(function(d) { return y(d.temp); });

    var humidityLine = d3.svg.line()
        .x(function(d) { return x(d.time); })
        .y(function(d) { return y(d.humidity); });

    var moldWarnLine = d3.svg.line()
        .x(function(d) { return x(d.time); })
        .y(function(d) { return y(80); });
    
    // Adds the svg canvas
    var svg = d3.select("#graphDiv")
      .append("svg")
        .attr("width", svgWidth)
        .attr("height", svgHeight)
      .append("g")
        .attr("transform", 
        "translate(" + margin.left + "," + margin.top + ")")

    // define function
    function draw(data) {
      data.forEach(function(d) {
        d.time = d3.time.hour.offset(parseDate(d.time), 4);
        d.temp = +d.temp;
        d.humidity = +d.humidity;
      });
      // Scale the range of the data
      x.domain(d3.extent(data, function(d) { return d.time; }));
      y.domain([d3.min(data, function(d) {
          return 0 }),
          d3.max(data, function(d) {
          return 100 })]);
      // Add the 2 valueline paths.
      svg.append("path")
        .style("stroke", "green")
        .attr("d", tempLine(data));
      svg.append("path")
        .style("stroke", "blue")
        .attr("d", humidityLine(data));
      // Add the X Axis
      svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + graphHeight + ")")
          .call(xAxis)
	  .selectAll("text")	
            .style("text-anchor", "start")
            .attr("dx", ".8em")
            .attr("dy", "-.15em")
            .attr("transform", function(d) {
                return "rotate(45)" 
                });
      // Add the Y Axis
      svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
      
      // Add annotations for the two lines.
      svg.append("text")
        .attr("transform", "translate("+(graphWidth+3)+","+y(graphData[0].temp)+")")
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .style("fill", "green")
        .text("Temp");
      svg.append("text")
        .attr("transform", "translate("+(graphWidth+3)+","+y(graphData[0].humidity)+")")
        .attr("dy", ".35em")
        .attr("text-anchor", "start")
        .style("fill", "blue")
        .text("Humidity");

      // Add a line at 80 denoting mold/mildew humidity levels.
      svg.append("path")
	.style("stroke", "red")
	.attr("d", moldWarnLine(data));
      // Add a vertical line at August 28, 2018 at 1:00 PM for when
      // the dehumidifier was added.
      svg.append("line")
	    .attr("x1", x(d3.time.hour.offset(parseDate("2018-08-28 13:00:00"), 4)))  //<<== change your code here
	    .attr("y1", 0)
	    .attr("x2", x(d3.time.hour.offset(parseDate("2018-08-28 13:00:00"), 4)))  //<<== and here
	    .attr("y2", svgHeight - margin.top - margin.bottom)
	    .style("stroke-width", 2)
	    .style("stroke", "gray")
	    .style("fill", "none");
    };

//draw(graphData);
