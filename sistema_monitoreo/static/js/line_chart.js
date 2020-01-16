LineChart= function(_parentElement, _variable){
  this.parentElement = _parentElement;
  this.variable = _variable;

  this.initVis();
}//End CONSTRUCTOR


LineChart.prototype.initVis = function(){

  var vis = this;

  vis.margin = { left:50, right:60, top:30, bottom:40 },
      vis.height = 150 - vis.margin.top - vis.margin.bottom,
      vis.width = 300 - vis.margin.left - vis.margin.right;

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

   // Title
   vis.g.append("text")
        .attr("x", (vis.width / 2))
        .attr("y", 0 - (vis.margin.top / 2))
        .attr("text-anchor", "middle")
        .style("font-size", "1.1vw")
//        .style("text-decoration", "underline")
        .text( vis.variable.slice(vis.variable.match('_').index+1,) );

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
//        console.log(s);
//        console.log(s.slice(0, 2));
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
};//End wrangleData


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
  d3.select(".focus."+vis.variable).remove();
  d3.select(".overlay."+vis.variable).remove();

  // Tooltip code

  var focus = vis.g.append("g")
      .attr("class", "focus " + vis.variable)
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
      .attr("class", "overlay " + vis.variable)
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
          filtered_data = (d1 && d0) ? (x0 - d0.date > d1.date - x0 ? d1 : d0) : 0; // New data filtered by date
//          console.log(filtered_data);
      focus.attr("transform", "translate(" + vis.x(filtered_data.date) + "," + vis.y(filtered_data[vis.yValue]) + ")");
      focus.select("text").text(function() { return d3.format(",")(filtered_data[vis.yValue].toFixed(4)); });
      focus.select(".x-hover-line").attr("y2", vis.height - vis.y(filtered_data[vis.yValue]));
      focus.select(".y-hover-line").attr("x2", -vis.x(filtered_data.date));

// DA - Carousel
     var errores_by_proceso = d3.nest()
                                .key(function(d){ return d.es_error_de;})
                                .entries(filtered_data.errores) // Grouping by proceso
//     console.log(errores_by_proceso)
        // Splitting into da and mec dataset
     var da_filter = errores_by_proceso.filter(function (d) { return d.key === "DA"})
     var mec_filter = errores_by_proceso.filter(function (d) { return d.key === "MEC"})
//    console.log(da_filter[0])
//     console.log(d3.entries(mec_filter[0]));


// Clean old data
     d3.select("#da-estado").selectAll("*").remove(); // Delete previous data in da-estado section
     d3.select("#da-errores").selectAll("*").remove(); // Delete previous data in da-errores section
     d3.select("#da-recomendaciones").selectAll("*").remove();  // Delete previous data in da-recomendaciones section

// Start feeding carousel
// Add new data
//    console.log(filtered_data)
     d3.select("#da-estado")
        .append("div")
        .html("<a href=" + "http://127.0.0.1:8000/medicion/" + filtered_data.id + "/" + ">Fecha:" + filtered_data.date +"</a>");
     d3.select("#da-estado")
        .append("div")
        .text("Estado de proceso: " + filtered_data.da_estado)

//    If there there are NOT errors in the process then print "ALL OK"
     if (da_filter.length === 0){
          d3.select("#da-errores").append("div").text("Proceso funcionando correctamente")
    } else{
    d3.select("#da-errores").append("div").selectAll("div") //Append div
                            .data(da_filter)//top level of the data
                            .enter()    //Enter to the data
                            .each(function(){ //For each entry in the top level
                                var li = d3.select(this); //Select the canvas
//                                li.append("p")
//                                    .text(function(d) {return d.key})
                                li.append("ul").selectAll("div") // Append a list
                                    .data(function(d){return d.values; }) //second-level of the json data
                                    .enter().append("li") // enter to the new level
                                    .text(function(d){
//                                    console.log(d)
                                     return d.nombre; //Append the name of error to the list
                                    })
                                    })

//        Check comments of the above
      d3.select("#da-recomendaciones").append("div").selectAll("div")
                            .data(da_filter)//top level
                            .enter()
                            .each(function(){
                                var li = d3.select(this);
                                li.append("ul").selectAll("div")
                                    .data(function(d){return d.values; }) //second-level
                                    .enter().append("li")
                                    .text(function(d){return d.tieneRecomendacion})
                            })
  } // End IF
  // END DA CARUCEL


//     d3.select("#da-estado").append("div").text("Click Aquí para más información").on("click", function(d, i) { window.open("www.google.com"); });

//        Check comments of the above
// Clean old data
     d3.select("#mec-estado").selectAll("*").remove(); // Delete previous data in mec-estadoo section
     d3.select("#mec-errores").selectAll("*").remove();
     d3.select("#mec-recomendaciones").selectAll("*").remove();

// Start MEC carucel
// Add new data
    console.log(filtered_data)

     d3.select("#mec-estado").append("div").html("<a href=" + "http://127.0.0.1:8000/medicion/" + filtered_data.id + "/" + ">Fecha:" + filtered_data.date +"</a>").style("font-size", "1vw");
     d3.select("#mec-estado").append("div").text("ESTADO: " + filtered_data.mec_estado)

     if (mec_filter.length === 0){
        d3.select("#mec-errores").append("div").text("Proceso funcionando correctamente")
    } else{
    d3.select("#mec-errores").append("div").selectAll("div")
                            .data(mec_filter)//top level
                            .enter()
                            .each(function(){
                                var li = d3.select(this);
//                                li.append("p")
//                                    .text(function(d) {return d.key})
                                li.append("ul").selectAll("div")
                                    .data(function(d){return d.values; }) //second-level
                                    .enter().append("li")
                                    .text(function(d){
//                                    console.log(d)
                                     return d.nombre;
                                    }).style("font-size", "10px").style('color', 'black')
                                    })

      d3.select("#mec-recomendaciones").append("div").selectAll("div")
                            .data(mec_filter)//top level
                            .enter()
                            .each(function(){
                                var li = d3.select(this);
                                li.append("ul").selectAll("div")
                                    .data(function(d){return d.values; }) //second-level
                                    .enter().append("li")
                                    .text(function(d){return d.tieneRecomendacion})
                            })
  } // End IF
  // END mec CARUCEL




//TO FILL TABLE OF VALUES FOR TOOLTIP IN DA SECTION TABLE"
      d3.select("#da-dil1").selectAll("*").remove();
      d3.select("#da-dil1").append("div").text("dil1")
      d3.select("#da-dil1-value").selectAll("*").remove();
      d3.select("#da-dil1-value").append("div").text(filtered_data.da_dil1)

      d3.select("#da-agv-in").selectAll("*").remove();
      d3.select("#da-agv-in").append("div").text("agv_in")
      d3.select("#da-agv-in-value").selectAll("*").remove();
      d3.select("#da-agv-in-value").append("div").text(filtered_data.da_agv_in)

      d3.select("#da-dqo-in").selectAll("*").remove();
      d3.select("#da-dqo-in").append("div").text("dqo_in")
      d3.select("#da-dqo-in-value").selectAll("*").remove();
      d3.select("#da-dqo-in-value").append("div").text(filtered_data.da_dqo_in)

      d3.select("#da-biomasa-x").selectAll("*").remove();
      d3.select("#da-biomasa-x").append("div").text("biomasa")
      d3.select("#da-biomasa-x-value").selectAll("*").remove();
      d3.select("#da-biomasa-x-value").append("div").text(filtered_data.da_biomasa_x)

      d3.select("#da-dqo-out").selectAll("*").remove();
      d3.select("#da-dqo-out").append("div").text("dqo_out")
      d3.select("#da-dqo-out-value").selectAll("*").remove();
      d3.select("#da-dqo-out-value").append("div").text(filtered_data.da_dqo_out)

      d3.select("#da-agv-out").selectAll("*").remove();
      d3.select("#da-agv-out").append("div").text("agv_out")
      d3.select("#da-agv-out-value").selectAll("*").remove();
      d3.select("#da-agv-out-value").append("div").text(filtered_data.da_agv_out)
/// END DA SECTION

//TO FILL TABLE OF VALUES FOR TOOLTIP IN MEC SECTION TABLE
      d3.select("#mec-agv_in").selectAll("*").remove();
      d3.select("#mec-agv_in").append("div").text("agv_in")
      d3.select("#mec-agv_in-value").selectAll("*").remove();
      d3.select("#mec-agv_in-value").append("div").text(filtered_data.mec_agv_in)

      d3.select("#mec-dil2").selectAll("*").remove();
      d3.select("#mec-dil2").append("div").text("dil2")
      d3.select("#mec-dil2-value").selectAll("*").remove();
      d3.select("#mec-dil2-value").append("div").text(filtered_data.mec_dil2)

      d3.select("#mec-eapp").selectAll("*").remove();
      d3.select("#mec-eapp").append("div").text("eapp")
      d3.select("#mec-eapp-value").selectAll("*").remove();
      d3.select("#mec-eapp-value").append("div").text(filtered_data.mec_eapp)

      d3.select("#mec-ace").selectAll("*").remove();
      d3.select("#mec-ace").append("div").text("ace")
      d3.select("#mec-ace-value").selectAll("*").remove();
      d3.select("#mec-ace-value").append("div").text(filtered_data.mec_ace)

      d3.select("#mec-xa").selectAll("*").remove();
      d3.select("#mec-xa").append("div").text("xa")
      d3.select("#mec-xa-value").selectAll("*").remove();
      d3.select("#mec-xa-value").append("div").text(filtered_data.mec_xa)

      d3.select("#mec-xm").selectAll("*").remove();
      d3.select("#mec-xm").append("div").text("xm")
      d3.select("#mec-xm-value").selectAll("*").remove();
      d3.select("#mec-xm-value").append("div").text(filtered_data.mec_xm)

      d3.select("#mec-xh").selectAll("*").remove();
      d3.select("#mec-xh").append("div").text("xh")
      d3.select("#mec-xh-value").selectAll("*").remove();
      d3.select("#mec-xh-value").append("div").text(filtered_data.mec_xh)

      d3.select("#mec-mox").selectAll("*").remove();
      d3.select("#mec-mox").append("div").text("mox")
      d3.select("#mec-mox-value").selectAll("*").remove();
      d3.select("#mec-mox-value").append("div").text(filtered_data.mec_mox)

      d3.select("#mec-imec").selectAll("*").remove();
      d3.select("#mec-imec").append("div").text("imec")
      d3.select("#mec-imec-value").selectAll("*").remove();
      d3.select("#mec-imec-value").append("div").text(filtered_data.mec_imec)

      d3.select("#mec-qh2").selectAll("*").remove();
      d3.select("#mec-qh2").append("div").text("qh2")
      d3.select("#mec-qh2-value").selectAll("*").remove();
      d3.select("#mec-qh2-value").append("div").text(filtered_data.mec_qh2)

  } //end mousemove()

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
      ((vis.yValue == "da_dqo_out") ?  "DQO(gL⁻¹)" :
      (vis.yValue == "da_agv_out" ? "Ace(gL⁻¹)" :
      ((vis.yValue == "mec_ace") ? "Ace(gL⁻¹)" :
      (vis.yValue == "mec_xa" ? "Xₐ (mgL⁻¹)" :
      (vis.yValue == "mec_xm" ? "Xₘ (mgL⁻¹)":
      (vis.yValue == "mec_xh" ? "Xₕ (mgL⁻¹)":
      (vis.yValue == "mec_mox" ? "Mₒₓ (L⁻¹)":
      (vis.yValue == "mec_imec" ? "Iₘₑ𝒸 (A)":
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
