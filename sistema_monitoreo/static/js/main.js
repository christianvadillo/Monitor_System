
var parseTime = d3.timeParse("%Y-%m-%dT%H:%M:%S")
var formatTime = d3.timeFormat("%Y-%m-%dT%H:%M:%S")
var dates_url = 'http://127.0.0.1:8000/api/min_max_dates/' // url that returns min and max dates from all mediciones


var filteredData = {};
var ineChart_da_1,
    lineChart_da_2,
    lineChart_da_3,
    lineChart_da_4,
    lineChart_da_5,
    lineChart_da_6,
    lineChart_mec_1,
    lineChart_mec_2,
    lineChart_mec_3,
    lineChart_mec_4,
    lineChart_mec_5,
    lineChart_mec_6,
    lineChart_mec_7,
    lineChart_mec_8,
    lineChart_mec_9,
    lineChart_mec_10

//Event listeners
$("#da-select").on("change",function() { update(); })
$("#mec-select").on("change",function() { update(); })

//Add jQuery UI slider
fetch(dates_url) // Get min and max from api
    .then(data=>{return data.json()})  // Transform to json
    .then(res=>{
//           console.log(res);
       $("#date-slider").slider({
       range: true,
       max: parseTime(res[1].max).getTime(),
       min: parseTime(res[0].min).getTime(),
       //  step: 86400000, // One day
       step: 1000, // 1 ms
       values: [parseTime(res[0].min).getTime(), parseTime(res[1].max).getTime()],
       slide: function(event, ui){
            dates = ui.values.map(function(val) { return new Date(val); })
            xVals = dates.map(function(date) { return timeline.x(date); })
            timeline.brushComponent.call(timeline.brush.move, xVals)
            }
       })
//              console.log("fetch called");
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

//data = data_src


//d3.json('static/data/data.json').then(function(data){
//d3.json(data).then(function(data){
//d3.json("file.json", function(data) {
//    // data is loaded, save the full set
//    DATASET = data;
//    // filter the initial subset
//    var subdata = data.filter(...);
//    // now update the graph
//    updateGraph(subdata);
//});

d3.json("http://127.0.0.1:8000/api/data_mediciones/").then(function(data){
  data.map(function (d) {
    d.date = parseTime(d.date)
    d.da_dil1 = +d.da_dil1
    d.da_agv_in = +d.da_agv_in
    d.da_dqo_in = +d.da_dqo_in
    d.da_biomasa_x = +d.da_biomasa_x
    d.da_dqo_out = +d.da_dqo_out
    d.da_agv_out = +d.da_agv_out
    d.mec_agv_in = +d.mec_agv_in
    d.mec_dil2 = +d.mec_dil2
    d.mec_eapp = +d.mec_eapp
    d.mec_ace = +d.mec_ace
    d.mec_xa = +d.mec_xa
    d.mec_xm = +d.mec_xm
    d.mec_xh = +d.mec_xh
    d.mec_mox = +d.mec_mox
    d.mec_imec = +d.mec_imec
    d.mec_qh2 = +d.mec_qh2
    return d;
  })

// Change the structure of the data, now Recomendacion comes inside of 'error'
var flatData = data.map(function(d){
  return{
    id: d.id,
    errores: (d.tieneError).map(function(d){
      return{
        id: d.id,
        nombre: d.nombre,
        es_error_de: d.es_error_de,
        descripcion: d.descripcion,
        peligro: d.peligro,
        tieneRecomendacion: d.tieneRecomendacion[0]['descripcion']
      }
    }),
    date: d.date,
    da_dil1: d.da_dil1,
    da_agv_in: d.da_agv_in,
    da_dqo_in: d.da_dqo_in,
    da_biomasa_x: d.da_biomasa_x,
    da_dqo_out: d.da_dqo_out,
    da_agv_out: d.da_agv_out,
    mec_agv_in: d.mec_agv_in,
    mec_dil2: d.mec_dil2,
    mec_eapp: d.mec_eapp,
    mec_ace: d.mec_ace,
    mec_xa: d.mec_xa,
    mec_xm: d.mec_xm,
    mec_xh: d.mec_xh,
    mec_mox: d.mec_mox,
    mec_imec: d.mec_imec,
    mec_qh2: d.mec_qh2,
    da_estado: d.da_estado,
    mec_estado: d.mec_estado,
    fbr_estado: d.fbr_estado
  }
});
console.log(data)
console.log(flatData);

//  allData = data;
allData = flatData;

// GROUPING DATA BY 'id'
//  nestedID = d3.nest()
//        .key(function(d){
//          return d.id;
//        })
//        .entries(allData)

//  console.log(nestedID)


//  console.log(parseTime("2009-01-01T00:00:00"));
// GROUPING DATA BY 'year' FOR barChart
//  nestedYear = d3.nest()
//        .key(function(d){
//          return d.date.getFullYear();
//        })
//        .entries(allData)

//console.log(nestedYear);
//console.log(d3.entries(nestedYear));
//console.log(nestedYear["year"]=="2009");
//var filter = nestedYear.filter(function (d) { return d.key == "2019"})
//console.log(filter);
//console.log(d3.extent(data, function(d) { return formatTime(d.date); }));

// Entradas DA
lineChart_da_1 = new LineChart("#da-chart-area1", "da_dil1");
lineChart_da_2 = new LineChart("#da-chart-area2", "da_agv_in");
lineChart_da_3 = new LineChart("#da-chart-area3", "da_dqo_in");
// Salidas DA
lineChart_da_4 = new LineChart("#da-chart-area4", "da_biomasa_x");
lineChart_da_5 = new LineChart("#da-chart-area5", "da_dqo_out");
lineChart_da_6 = new LineChart("#da-chart-area6", "da_agv_out");
// Entradas MEC
lineChart_mec_1 = new LineChart("#mec-chart-area1", "mec_agv_in");
lineChart_mec_2 = new LineChart("#mec-chart-area2", "mec_dil2");
lineChart_mec_3 = new LineChart("#mec-chart-area3", "mec_eapp");
// Salidas MEC
lineChart_mec_4 = new LineChart("#mec-chart-area4", "mec_ace");
lineChart_mec_5 = new LineChart("#mec-chart-area5", "mec_xa");
lineChart_mec_6 = new LineChart("#mec-chart-area6", "mec_xm");
lineChart_mec_7 = new LineChart("#mec-chart-area7", "mec_xh");
lineChart_mec_8 = new LineChart("#mec-chart-area8", "mec_mox");
lineChart_mec_9 = new LineChart("#mec-chart-area9", "mec_imec");
lineChart_mec_10 = new LineChart("#mec-chart-area10", "mec_qh2");

timeline = new Timeline("#timeline")
})///End d3.json()

function update(){
    lineChart_da_1.wrangleData();
    lineChart_da_2.wrangleData();
    lineChart_da_3.wrangleData();
    lineChart_da_4.wrangleData();
    lineChart_da_5.wrangleData();
    lineChart_da_6.wrangleData();

    lineChart_mec_1.wrangleData();
    lineChart_mec_2.wrangleData();
    lineChart_mec_3.wrangleData();
    lineChart_mec_4.wrangleData();
    lineChart_mec_5.wrangleData();
    lineChart_mec_6.wrangleData();
    lineChart_mec_7.wrangleData();
    lineChart_mec_8.wrangleData();
    lineChart_mec_9.wrangleData();
    lineChart_mec_10.wrangleData();
}
