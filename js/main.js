const base_data_path = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/data"
const pred_data_path = `${base_data_path}/preds`
const graphMargin = 100;
const graphWidth = 1600;
const graphHeight = 900;

const legendSpacing = 150;
const legendHeight = "5em";
const legendIconHeight = "3.75em";

const lineStrokeWidth = 2;

const weightGraphId = "graph-weight-tmp";
const workoutFrequencyGraphId = "graph-workout-frequency-tmp";
const heartRateGraphId = "graph-resting-heartrate-tmp"

// TODO make separate dataloading module for this logic
// TODO also add the rest of the relevant loaders
async function loadHealthMetrics() {
  function row(d) {
    return {
      "date": new Date(d.date),
      "weight(lbs)": +d["weight(lbs)"],
      "resting_heart_rate(bpm)": +d["resting_heart_rate(bpm)"],
      "notes": d.notes,
    };
  }
  return await readCSV(`${base_data_path}/health_metrics.csv`, row);
}

async function loadWeightTrendline() {
  function row(d) {
    return {
      "date": new Date(d.date),
      "weight(lbs)": +d["weight(lbs)"],
    };
  }
  return await readCSV(`${pred_data_path}/weight_trendline.csv`, row);
}

async function loadWorkoutFrequency() {
  function row(d) {
    return {
      "date": new Date(d.date),
      "duration": +d["duration(s)"] / 60,
      "avg_duration": +d["avg_duration(s)"] / 60,
    };
  }
  return await readCSV(`${pred_data_path}/avg_workout_durations.csv`, row);
}

async function loadHeartRateTrendline() {
  function row(d) {
    return {
      "date": new Date(d.date),
      "resting_heart_rate(bpm)": +d["resting_heart_rate(bpm)"],
    };
  }
  return await readCSV(`${pred_data_path}/resting_heart_rate_trendline.csv`, row);
}

Date.prototype.addDays = function(days) {
    const date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

function d3_min(data, c_name) {
  return d3.min(data, function(row) { return row[c_name]; });
}

function d3_max(data, c_name) {
  return d3.max(data, function(row) { return row[c_name]; });
}

function date_tick(d) {
  const year = d.getYear() + 1900;  // Accommodating for library's weird year offset
  const month = d.toDateString().substring(4, 7);
  return `${month} ${year}`;
}

function time_tick(t) {
  const mins = t % 60;
  const hours = (t - mins) / 60;
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
}

function addTitle(svg, title) {
  const width = svg.node().width.animVal.value;
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", "1em")
    .style("text-anchor", "middle")
    .style("font-weight", "bold")
    .text(title);
}

class RefLineType {
  static Marker = new RefLineType("marker")
  static Threshold = new RefLineType("threshold")

  constructor(name) {
    this.name = name
  }
}

function addRefLine(svg, label, yMin, yMax, yRef, refLineType) {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const contentHeight = height - graphMargin - graphMargin;
  const axisBottom = height - graphMargin;
  const yRange = yMax - yMin;
  const refLineOffset = yRef - yMin;

  const pos = axisBottom - contentHeight * (refLineOffset / yRange);
  const refLineRight = width - graphMargin;
  const labelPosition = refLineRight + 5;

  var strokeColour = null;
  var dashArray = null;
  if (refLineType === RefLineType.Marker) {
    var strokeColour = "black";
    var dashArray = ("3, 2");
  } else if (refLineType === RefLineType.Threshold) {
    var strokeColour = "red";
  }

  svg.append("text")
    .text(label)
    .attr("x", labelPosition)
    .attr("y", pos)
    .attr("dy", ".35em")  // Centers the text on the reference line
    .attr("font-size", "0.8em");
  svg.append("line")
    .style("stroke", strokeColour)
    .style("stroke-width", 2)
    .style("stroke-dasharray", dashArray)
    .attr("x1", graphMargin)
    .attr("y1", pos)
    .attr("x2", refLineRight)
    .attr("y2", pos);
}

function addDateXAxis(svg, firstDate, lastDate) {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const axisBottom = height - graphMargin;
  const axisTop = height - graphMargin - graphMargin;

  const x = d3.scaleUtc()
    .domain([firstDate, lastDate])
    .range([graphMargin, width - graphMargin]);

  // Major gridlines (monthly)
  svg.append("g")
    .attr("transform", `translate(0, ${axisBottom})`)
    .call(d3.axisBottom(x).tickFormat(date_tick))
    .call(g => g.selectAll(".tick line").clone()
      .attr("stroke-opacity", 0.3)
      .attr("y1", -axisTop));

  // Minor gridlines (weekly)
  svg.append("g")
    .attr("transform", `translate(0, ${axisBottom})`)
    .call(d3.axisBottom(x)
      .ticks(d3.timeWeek.every(1))
      .tickFormat((_) => "")
      .tickSize(0))
    .call(g => g.selectAll(".tick line").clone()
      .attr("stroke-opacity", 0.1)
      .attr("y1", -axisTop));
}

function addLinearYAxis(svg, minVal, maxVal, majorStep, minorStep) {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const axisBottom = height - graphMargin;
  const contentWidth = width - graphMargin - graphMargin;
  const y = d3.scaleLinear()
    .domain([minVal, maxVal])
    .range([axisBottom, graphMargin]);

  // Major gridlines
  svg.append("g")
    .attr("transform", `translate(${graphMargin}, 0)`)
    .call(d3.axisLeft(y)
      .tickValues(d3.range(minVal, maxVal, majorStep)))
    .call(g => g.selectAll(".tick line").clone()
      .attr("stroke-opacity", 0.3)
      .attr("x1", contentWidth));

  // Minor gridlines
  if (minorStep !== null) {
    svg.append("g")
      .attr("transform", `translate(${graphMargin}, 0)`)
      .call(d3.axisLeft(y)
        .tickValues(d3.range(minVal, maxVal, minorStep))
        .tickFormat((_) => "")
        .tickSize(0))
      .call(g => g.selectAll(".tick line").clone()
        .attr("stroke-opacity", 0.1)
        .attr("x1", contentWidth));
  }
}

function addLinearTimeYAxis(svg, minTime, maxTime, majorStep, minorStep) {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const axisBottom = height - graphMargin;
  const contentWidth = width - graphMargin - graphMargin;

  const y = d3.scaleLinear()
    .domain([minTime, maxTime])
    .range([axisBottom, graphMargin]);

  // Major gridlines (monthly)
  svg.append("g")
    .attr("transform", `translate(${graphMargin}, 0)`)
    .call(d3.axisLeft(y)
      .tickValues(d3.range(minTime, maxTime + 1, majorStep))
      .tickFormat(time_tick))
    .call(g => g.selectAll(".tick line").clone()
      .attr("stroke-opacity", 0.3)
      .attr("x1", contentWidth));

  // Minor gridlines (weekly)
  svg.append("g")
    .attr("transform", `translate(${graphMargin}, 0)`)
    .call(d3.axisLeft(y)
        .tickValues(d3.range(minTime, maxTime, minorStep))
        .tickFormat((_) => "")
        .tickSize(0))
    .call(g => g.selectAll(".tick line").clone()
      .attr("stroke-opacity", 0.1)
      .attr("x1", contentWidth));
}

async function readCSV(path, row) {
  return await d3.csv(path, row);
}

function plotWeight(data, weightTrendline) {
  const minWeight = 180;
  const maxWeight = 305;
  const nDaysToExtrapolate = 100;

  const firstDate = d3_min(data, "date");
  const lastDate = d3_max(data, "date").addDays(nDaysToExtrapolate);

  // Create the SVG container
  const svg = d3.create("svg")
    .attr("width", graphWidth)
    .attr("height", graphHeight);

  // Create the title, axes, and reference lines
  addTitle(svg, "Weight");
  addDateXAxis(svg, firstDate, lastDate);
  addLinearYAxis(svg, minWeight, maxWeight, 20, 5);
  addRefLine(svg, "Healthy", minWeight, maxWeight, 250, RefLineType.Marker);
  addRefLine(svg, "Target", minWeight, maxWeight, 200, RefLineType.Marker);
  
  // Add the legend
  svg.append("text")
    .attr("x", graphWidth / 2 - legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Projected Weight")
    .attr("font-size", "0.8em");
  svg.append("line")
    .attr("x1", graphWidth / 2 - legendSpacing)
    .attr("y1", legendIconHeight)
    .attr("x2", graphWidth / 2 - 0.85 * legendSpacing)
    .attr("y2", legendIconHeight)
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .style("stroke-dasharray", ("8, 4"));
  svg.append("text")
    .attr("x", graphWidth / 2 + legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Weight (lbs)")
    .attr("font-size", "0.8em");
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .append("circle")
      .attr("cx", graphWidth / 2 + 0.2 * legendSpacing)
      .attr("cy", legendIconHeight)
      .attr("r", 1.5);

  // Plot the data
  const axisBottom = graphHeight - graphMargin;
  const x = d3.scaleUtc()
    .domain([firstDate, lastDate])
    .range([graphMargin, graphWidth - graphMargin]);
  const y = d3.scaleLinear()
    .domain([minWeight, maxWeight])
    .range([axisBottom, graphMargin]);
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .selectAll("dot")
    .data(data)
    .enter().append("circle")
      .attr("cx", d => x(d["date"]))
      .attr("cy", d => y(d["weight(lbs)"]))
      .attr("r", 1.5);

  // Plot the trendline
  valueLine = d3.line()
    .x(function (d, i) { return x(d["date"]); })
    .y(function (d, i) { return y(d["weight(lbs)"]); });
  svg.append("path")
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .style("stroke-dasharray", ("8, 4"))
    .attr("d", valueLine(weightTrendline));

  // Annotate object and append to the page
  svg.attr("id", weightGraphId);
  return svg;
}

function plotWorkoutFrequency(data) {
  const minTime = 0;
  const maxTime = 210;

  const firstDate = d3_min(data, "date");
  const lastDate = d3_max(data, "date");

  // Create the SVG container
  const svg = d3.create("svg")
    .attr("width", graphWidth)
    .attr("height", graphHeight);

  // Create the title, axes, and reference lines
  addTitle(svg, "Workout Frequency");
  addDateXAxis(svg, firstDate, lastDate);
  addLinearTimeYAxis(svg, minTime, maxTime, 30, 10);
  addRefLine(svg, "Target Minimum", minTime, maxTime, 22.5, RefLineType.Threshold);
  
  // Add the legend
  svg.append("text")
    .attr("x", graphWidth / 2 - legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("N-Day Avg Daily Duration")
    .attr("font-size", "0.8em");
  svg.append("line")
    .attr("x1", graphWidth / 2 - 1.15 * legendSpacing)
    .attr("y1", legendIconHeight)
    .attr("x2", graphWidth / 2 - legendSpacing)
    .attr("y2", legendIconHeight)
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth);
  svg.append("text")
    .attr("x", graphWidth / 2 + legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Workout Duration")
    .attr("font-size", "0.8em");
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .append("circle")
      .attr("cx", graphWidth / 2 + 0.1 * legendSpacing)
      .attr("cy", legendIconHeight)
      .attr("r", 1.5);

  // Plot the data
  const axisBottom = graphHeight - graphMargin;
  const x = d3.scaleUtc()
    .domain([firstDate, lastDate])
    .range([graphMargin, graphWidth - graphMargin]);
  const y = d3.scaleLinear()
    .domain([minTime, maxTime])
    .range([axisBottom, graphMargin]);
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .selectAll("dot")
    .data(data)
    .enter().append("circle")
      .filter( function (d) { return d["duration"] <= maxTime; })
      .attr("cx", d => x(d["date"]))
      .attr("cy", d => y(d["duration"]))
      .attr("r", 1.5);

  // Plot the trendline
  valueLine = d3.line()
    .x(function (d, i) { return x(d["date"]); })
    .y(function (d, i) { return y(d["avg_duration"]); });
  svg.append("path")
    .style("fill", "none")
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .attr("d", valueLine(data));

  // Annotate object and append to the page
  svg.attr("id", workoutFrequencyGraphId);
  return svg;
}

function plotHeartRate(data, heartRateTrendline) {
  // TODO
}

(async function() {
  // Load data
  const healthMetrics = await loadHealthMetrics();
  //const walks = readCSV(`${base_data_path}/walks.csv`);
  //const bikes = readCSV(`${base_data_path}/bikes.csv`);
  //const runs = readCSV(`${base_data_path}/runs.csv`);
  //const weight_training_workouts = readCSV(`${base_data_path}/weight_training_workouts.csv`);
  //const weight_training_sets = readCSV(`${base_data_path}/weight_training_sets.csv`);
  //const travel_days = readCSV(`${base_data_path}/travel_days.csv`);

  // Load predictions
  const weightTrendline = await loadWeightTrendline();
  const workoutFrequency = await loadWorkoutFrequency();
  const heartRateTrendline = await loadHeartRateTrendline();

  // Build and display the graphs
  document.body.append(plotWeight(healthMetrics, weightTrendline).node());
  document.body.append(plotWorkoutFrequency(workoutFrequency).node());
  //document.body.append(plotHeartRate(healthMetrics, heartRateTrendline).node());
})();
