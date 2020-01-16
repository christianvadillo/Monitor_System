
var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S")
var formatTime = d3.timeFormat("%Y-%m-%dT%H:%M:%S")

var filteredData = {};
var lineChart_da_1, lineChart_da_2, lineChart_da_3,
    lineChart_da_4, lineChart_da_5, lineChart_da_6;
//Event listeners
$("#da-select").on("change",function() { update(); })
$("#mec-select").on("change",function() { update(); })

//Add jQuery UI slider

$("#date-slider").slider({
  range: true,
  max: parseTime("2018-11-10T01:00:00").getTime(),
  min: parseTime("2009-01-01T00:00:00").getTime(),
  step: 86400000, // One day
  values: [parseTime("2009-01-01T00:00:00").getTime(), parseTime("2018-11-10T01:00:00").getTime()],
  slide: function(event, ui){
    dates = ui.values.map(function(val) { return new Date(val); })
    xVals = dates.map(function(date) { return timeline.x(date); })

    timeline.brushComponent.call(timeline.brush.move, xVals)

  }
})


function brushed() {
    var selection = d3.event.selection || timeline.x.range();
    var newValues = selection.map(timeline.x.invert)

    $("#date-slider")
        .slider('values', 0, newValues[0])
        .slider('values', 1, newValues[1]);
    $("#dateLabel1").text(formatTime(newValues[0]));
    $("#dateLabel2").text(formatTime(newValues[1]));
    update()

}


//d3.json('static/data/data.json').then(function(data){
d3.json('static/data/bio_data.json').then(function(data){
  data.map(function (d) {
    d.date = parseTime(d.date)
    d.dil1 = +d.dil1
    d.agv_in_da = +d.agv_in_da
    d.dqo_in_da = +d.dqo_in_da
    d.biomasa_x = +d.biomasa_x
    d.dqo_out = +d.dqo_out
    d.agv_out_da = +d.agv_out_da
    d.agv_in_mec = +d.agv_in_mec
    d.dil2 = +d.dil2
    d.eapp = +d.eapp
    d.ace = +d.ace
    d.xa = +d.xa
    d.xm = +d.xm
    d.xh = +d.xh
    d.mox = +d.mox
    d.imec = +d.imec
    d.qh2 = +d.qh2
    return d;
  })
  allData = data;


  console.log(parseTime("2009-01-01T00:00:00"));
// GROUPING DATA BY 'year' FOR barChart
  nestedYear = d3.nest()
        .key(function(d){
          return d.date.getFullYear();
        })
        .entries(allData)

console.log(nestedYear);
console.log(d3.entries(nestedYear));
console.log(nestedYear["year"]=="2009");
var filter = nestedYear.filter(function (d) { return d.key == "2009"})
console.log(filter);
console.log(d3.extent(data, function(d) { return formatTime(d.date); }));
// GROUPING DATA BY 'year' FOR barChart

lineChart_da_1 = new LineChart("#chart-area1", "dqo_out");
lineChart_da_2 = new LineChart("#chart-area2", "agv_out_da");
lineChart_da_3 = new LineChart("#chart-area3", "biomasa_x");
lineChart_da_4 = new LineChart("#chart-area4", "ace");
lineChart_da_5 = new LineChart("#chart-area5", "xa");
lineChart_da_6 = new LineChart("#chart-area6", "qh2");
timeline = new Timeline("#timeline")
})///End d3.json()

function update(){
  lineChart_da_1.wrangleData();
  lineChart_da_2.wrangleData();
  lineChart_da_3.wrangleData();
  lineChart_da_4.wrangleData();
  lineChart_da_5.wrangleData();
  lineChart_da_6.wrangleData();
}
