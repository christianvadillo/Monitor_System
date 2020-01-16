LineChart= function(_parentElement, _variable){
  this.parentElement = _parentElement;
  this.variable = _variable;

  this.initVis();
}//End CONSTRUCTOR


LineChart.prototype.initVis = function(){

  var vis = this;

  vis.margin = { left:50, right:120, top:30, bottom:40 },
      vis.height = 150 - vis.margin.top - vis.margin.bottom,
      vis.width = 400 - vis.margin.left - vis.margin.right;

  vis.svg = d3.select(vis.parentElement)
      .append("svg")
      .attr("width", vis.width + vis.margin.left + vis.margin.right)
      .attr("height", vis.height + vis.margin.top + vis.margin.bottom)
  vis.g = vis.svg.append("g")
            .attr("transform", "translate(" + vis.margin.left +
                ", " + vis.margin.top + ")");

  vis.t = function() { return d3.transition().duration(1000); }
  vis.bisectDate = d3.bisector( function(d) {return d.date; }).left;

  vis.linePath = vis.g.append("path")
      .attr('class', 'line')
      .attr('fill', 'none')
      .attr('stroke', 'blue')
      .attr('stroke-width', "0.5px")

  // Labels
  vis.xLabel = vis.g.append("text")
      .attr("class", "x axisLabel")
      .attr("y", vis.height +25)
      .attr("x", vis.width / 2)
      .attr("font-size", "7px")
      .attr("text-anchor", "middle")
      .text("Tiempo");

  vis.yLabel = vis.g.append("text")
      .attr("class", "y axisLabel")
      .attr("transform", "rotate(-90)")
      .attr("y", -40)
      .attr("x", -vis.height / 2)
      .attr("font-size", "7px")
      .attr("text-anchor", "middle")
      .text("Biomasa (gL⁻¹)")

      // Scales
  vis.x = d3.scaleTime().range([0, vis.width]);
  vis.y = d3.scaleLinear().range([vis.height, 0]);

      // X-axis
  vis.xAxisCall = d3.axisBottom()
        .ticks(4);
  vis.xAxis = vis.g.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + vis.height +")");

      // Y-axis
  vis.yAxisCall = d3.axisLeft()
        .ticks(4)
        .tickFormat(function (d){
        var formatSi = d3.format(".2s");
        var s = formatSi(d);
        console.log(s);
        console.log(s.slice(0, 2));
        switch (s[s.length - 1]) {
        case "G": return s.slice(0, -1) + "B";
        case "k": return s.slice(0, -1) + "K";
        case "Y": return s.slice(0, 2) + "Y";
        }
        return s;
        });
  vis.yAxis = vis.g.append("g")
      .attr("class", "y axis");

      // Gridline
  vis.xGrid = d3.axisTop(vis.x)
      .tickFormat("")
      .ticks(4)
      .tickSize(-vis.height)
      .scale(vis.x);

  vis.yGrid = d3.axisLeft(vis.y)
      .tickFormat("")
      .ticks(4)
      .tickSize(-vis.width)
      .scale(vis.y);

        // add the X gridlines
  vis.svg.append("g")
      .attr("class", "grid")
      .attr("transform", "translate("+ vis.margin.left +"," + vis.margin.top + ")")
      .call(vis.xGrid)

  vis.svg.append("g")
      .attr("class", "grid")
      .attr("transform", "translate("+ vis.margin.left +"," + vis.margin.top + ")")
      .call(vis.yGrid)

  vis.wrangleData();
}//END initVis


LineChart.prototype.wrangleData = function(){
  var vis = this;

  // Filter data based on selections
//  vis.yValue = $("#da-select").val(),
  vis.yValue = vis.variable
  vis.sliderValues = $("#date-slider").slider("values");

  vis.dataTimeFiltered = allData.filter(function(d){
      return ((d.date >= vis.sliderValues[0]) && (d.date <= vis.sliderValues[1]))
  });

  vis.updateVis();
}//End wrangleData


LineChart.prototype.updateVis = function(){
  var vis = this;

  // Update scales
  vis.x.domain(d3.extent(vis.dataTimeFiltered, function(d){ return d.date; }));
  vis.y.domain([d3.min(vis.dataTimeFiltered, function(d){ return d[vis.yValue]; }) / 1.005,
                d3.max(vis.dataTimeFiltered, function(d){ return d[vis.yValue]; }) * 1.005]);


  // Update axes
  vis.xAxisCall.scale(vis.x);
  vis.xAxis.transition(vis.t()).call(vis.xAxisCall);
  vis.yAxisCall.scale(vis.y);
  vis.yAxis.transition(vis.t()).call(vis.yAxisCall);

  // Clear old tooltips
  d3.select(".focus").remove();
  d3.select(".overlay").remove();

  // Tooltip code

  var focus = vis.g.append("g")
      .attr("class", "focus")
      .style("display", "none");

  focus.append("line")
      .attr("class", "x-hover-line hover-line")
      .attr("y1", 0)
      .attr("y2", vis.height);

  focus.append("line")
      .attr("class", "y-hover-line hover-line")
      .attr("x1", 0)
      .attr("x2", vis.width);

  focus.append("circle")
      .attr("r", 2);

  focus.append("text")
      .attr("x", 10)
      .attr("dy", ".31em");

  vis.svg.append("rect")
      .attr("transform", "translate(" + vis.margin.left + "," + vis.margin.top + ")")
      .attr("class", "overlay")
      .attr("width", vis.width)
      .attr("height", vis.height)
      .on("mouseover", function() { focus.style("display", null); })
      .on("mouseout", function(d) { focus.style("display", "none"); })
      .on("mousemove", mousemove);

  function mousemove() {
      var x0 = vis.x.invert(d3.mouse(this)[0]),
          i = vis.bisectDate(vis.dataTimeFiltered, x0, 1),
          d0 = vis.dataTimeFiltered[i - 1],
          d1 = vis.dataTimeFiltered[i],
          d = (d1 && d0) ? (x0 - d0.date > d1.date - x0 ? d1 : d0) : 0;
        //  console.log(x0);
      focus.attr("transform", "translate(" + vis.x(d.date) + "," + vis.y(d[vis.yValue]) + ")");
      focus.select("text").text(function() { return d3.format(",")(d[vis.yValue].toFixed(4)); });
      focus.select(".x-hover-line").attr("y2", vis.height - vis.y(d[vis.yValue]));
      focus.select(".y-hover-line").attr("x2", -vis.x(d.date));

      d3.select("#showdata").selectAll("*").remove();
      d3.select("#showdata")
            .append("div")
            .text("Date: " + formatTime(d.date))
            .style("font-size", "10px")
            .style("color", "blue")
      d3.select("#showdata").append("div").text("dil1: " + d.dil1).style("font-size", "10px").style('color', 'red')
      d3.select("#showdata").append("div").text("agv_in_da: " + d.agv_in_da).style("font-size", "10px").style('color', 'brown')
      d3.select("#showdata").append("div").text("dqo_in_da: " + d.dqo_in_da).style("font-size", "10px").style('color', 'green')
      d3.select("#showdata").append("div").text("agv_in_mec: " + d.agv_in_mec).style("font-size", "10px").style('color', 'red')
      d3.select("#showdata").append("div").text("dil2: " + d.dil2).style("font-size", "10px").style('color', 'green')

  }

  // Path generator
  var line = d3.line()
      .x(function(d){ return vis.x(d.date); })
      .y(function(d){ return vis.y(d[vis.yValue]); });

  // Update our line path
  vis.g.select(".line")
      .transition(vis.t)
      .attr("d", line(vis.dataTimeFiltered));

  // Update y-axis label
  var newText = (vis.yValue == "biomasa_x") ? "Biomasa (gL⁻¹)" :
      ((vis.yValue == "dqo_out") ?  "DQO(gL⁻¹)" :
      (vis.yValue == "agv_out_da" ? "Ace(gL⁻¹)" :
      ((vis.yValue == "ace") ? "Ace(gL⁻¹)" :
      (vis.yValue == "xa" ? "Xₐ (mgL⁻¹)" :
      (vis.yValue == "xm" ? "Xₘ (mgL⁻¹)":
      (vis.yValue == "xh" ? "Xₕ (mgL⁻¹)":
      (vis.yValue == "mox" ? "Mₒₓ (L⁻¹)":
      (vis.yValue == "imec" ? "Iₘₑ𝒸 (A)":
      "Qₕ₂ (Ld⁻¹)"))))))))
  vis.yLabel.text(newText);

}//End updateVis



// var margin = { left:80, right:100, top:50, bottom:100 },
//     height = 500 - margin.top - margin.bottom,
//     width = 800 - margin.left - margin.right;
//
// var svg = d3.select("#linechart-area")
//     .append("svg")
//     .attr("width", width + margin.left + margin.right)
//     .attr("height", height + margin.top + margin.bottom)
// var g = svg.append("g")
//         .attr("transform", "translate(" + margin.left +
//             ", " + margin.top + ")");
//
//
// var t = function(){ return d3.transition().duration(1000); }
//
// var bisectDate = d3.bisector(function(d) { return d.date; }).left;
//
// // Add the line for the first time
// g.append("path")
//     .attr("class", "line")
//     .attr("fill", "none")
//     .attr("stroke", "blue")
//     .attr("stroke-width", "0.5px");
//
// // Labels
// var xLabel = g.append("text")
//     .attr("class", "x axisLabel")
//     .attr("y", height + 50)
//     .attr("x", width / 2)
//     .attr("font-size", "15px")
//     .attr("text-anchor", "middle")
//     .text("Time");
// var yLabel = g.append("text")
//     .attr("class", "y axisLabel")
//     .attr("transform", "rotate(-90)")
//     .attr("y", -60)
//     .attr("x", -170)
//     .attr("font-size", "15px")
//     .attr("text-anchor", "middle")
//     .text("Biomasa (gL⁻¹)")
//
//
// // Scales
// var x = d3.scaleTime().range([0, width]);
// var y = d3.scaleLinear().range([height, 0]);
//
// // X-axis
// var xAxisCall = d3.axisBottom()
//     .ticks(8);
// var xAxis = g.append("g")
//     .attr("class", "x axis")
//     .attr("transform", "translate(0," + height +")");
//
// // Y-axis
// var yAxisCall = d3.axisLeft()
// var yAxis = g.append("g")
//     .attr("class", "y axis");
//
// // Gridline
//
// var xGrid = d3.axisTop(x)
//                   .tickFormat("")
//                   .ticks(6)
//                   .tickSize(-height)
//                   .scale(x);
//
// var yGrid = d3.axisLeft(y)
//                   .tickFormat("")
//                   .ticks(6)
//                   .tickSize(-width)
//                   .scale(y);
//
//
//   // add the X gridlines
//   svg.append("g")
//       .attr("class", "grid")
//       .attr("transform", "translate("+ margin.left +"," + margin.top + ")")
//       .call(xGrid)
//
//   svg.append("g")
//       .attr("class", "grid")
//       .attr("transform", "translate("+ margin.left +"," + margin.top + ")")
//       .call(yGrid)
//
//
//
// function update() {
//     // Filter data based on selections
//     var yValue = $("#out-select").val(),
//         year = $("#in-select").val()
//         sliderValues = $("#date-slider").slider("values");
//
//
//
//     var dataTimeFiltered = allData.filter(function(d){
//         return ((d.date >= sliderValues[0]) && (d.date <= sliderValues[1]))
//     });
//
//     // Update scales
//     x.domain(d3.extent(dataTimeFiltered, function(d){ return d.date; }));
//     y.domain([d3.min(dataTimeFiltered, function(d){ return d[yValue]; }) / 1.005,
//         d3.max(dataTimeFiltered, function(d){ return d[yValue]; }) * 1.005]);
//
//     // Fix for format values
//     var formatSi = d3.format(".2s");
//     function formatAbbreviation(x) {
//       var s = formatSi(x);
//       switch (s[s.length - 1]) {
//         case "G": return s.slice(0, -1) + "B";
//         case "k": return s.slice(0, -1) + "K";
//       }
//       return s;
//     }
//
//
//
//     // Update axes
//     xAxisCall.scale(x);
//     xAxis.transition(t()).call(xAxisCall);
//     yAxisCall.scale(y);
//     yAxis.transition(t()).call(yAxisCall);
//
//     // Clear old tooltips
//     d3.select(".focus").remove();
//     d3.select(".overlay").remove();
//
//     // Tooltip code
//
//     var focus = g.append("g")
//         .attr("class", "focus")
//         .style("display", "none");
//
//     focus.append("line")
//         .attr("class", "x-hover-line hover-line")
//         .attr("y1", 0)
//         .attr("y2", height);
//
//     focus.append("line")
//         .attr("class", "y-hover-line hover-line")
//         .attr("x1", 0)
//         .attr("x2", width);
//
//     focus.append("circle")
//         .attr("r", 2);
//
//     focus.append("text")
//         .attr("x", 10)
//         .attr("dy", ".31em");
//
//     svg.append("rect")
//         .attr("transform", "translate(" + margin.left + "," + margin.top + ")")
//         .attr("class", "overlay")
//         .attr("width", width)
//         .attr("height", height)
//         .on("mouseover", function() {
//           focus.style("display", null);
//
//           })
//         .on("mouseout", function(d) {
//           focus.style("display", "none");
//            })
//         .on("mousemove", mousemove);
//
//
//     function mousemove() {
//         var x0 = x.invert(d3.mouse(this)[0]),
//             i = bisectDate(dataTimeFiltered, x0, 1),
//             d0 = dataTimeFiltered[i - 1],
//             d1 = dataTimeFiltered[i],
//             d = (d1 && d0) ? (x0 - d0.date > d1.date - x0 ? d1 : d0) : 0;
//           //  console.log(x0);
//         focus.attr("transform", "translate(" + x(d.date) + "," + y(d[yValue]) + ")");
//         focus.select("text").text(function() { return d3.format(",")(d[yValue].toFixed(4)); });
//         focus.select(".x-hover-line").attr("y2", height - y(d[yValue]));
//         focus.select(".y-hover-line").attr("x2", -x(d.date));
//
//         d3.select("#showdata").selectAll("*").remove();
//         d3.select("#showdata")
//               .append("div")
//               .text("Date: " + formatTime(d.date))
//               .style("font-size", "10px")
//               .style("color", "blue")
//         d3.select("#showdata").append("div").text("Dil1: " + d.dil1).style("font-size", "10px").style('color', 'red')
//         d3.select("#showdata").append("div").text("DQO_in: " + d.dqo_in).style("font-size", "10px").style('color', 'green')
//         d3.select("#showdata").append("div").text("AGV_in_DA: " + d.agv_in).style("font-size", "10px").style('color', 'brown')
//         d3.select("#showdata").append("div").text("AGV_in_MEC: " + d.agv_out).style("font-size", "10px").style('color', 'red')
//         d3.select("#showdata").append("div").text("Dil2: " + d.dil2).style("font-size", "10px").style('color', 'green')
//
//     }
//
//
//
//
//     // Path generator
//     line = d3.line()
//         .x(function(d){ return x(d.date); })
//         .y(function(d){ return y(d[yValue]); });
//
//     // Update our line path
//     g.select(".line")
//         .transition(t)
//         .attr("d", line(dataTimeFiltered));
//
//     // Update y-axis label
//     var newText = (yValue == "biomasa_x") ? "Biomasa (gL⁻¹)" :
//         ((yValue == "dqo_out") ?  "DQO(gL⁻¹)" :
//         ((yValue == "ace") ? "Ace(gL⁻¹)" :
//         (yValue == "xa" ? "Xₐ (mgL⁻¹)" :
//         (yValue == "xm" ? "Xₘ (mgL⁻¹)":
//         (yValue == "xh" ? "Xₕ (mgL⁻¹)":
//         (yValue == "mox" ? "Mₒₓ (L⁻¹)":
//         (yValue == "imec" ? "Iₘₑ𝒸 (A)":
//         "Qₕ₂ (Ld⁻¹)")))))))
//     yLabel.text(newText);
// }
