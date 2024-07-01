const base_data_path = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/data"
const pred_data_path = `${base_data_path}/preds`
const graphMargin = 100;
const graphWidth = 1600;
const graphHeight = 900;

const legendSpacing = 150;
const legendHeight = "5em";
const legendIconHeight = "3.75em";

const lineStrokeWidth = 2;

const weightGraphId = "graph-weight";
const workoutFrequencyGraphId = "graph-workout-frequency";
const heartRateGraphId = "graph-resting-heartrate";

const secondaryGraphClassName = "secondary-chart";
const bpmClimbField = "bpm(beats_per_metre_climbed)";

function computeWalkScore(row, durationInS) {
  const durationInH = durationInS / 3600;
  const pace = row["distance(km)"] / durationInH;
  const rateOfClimb = row["elevation(m)"] / durationInH;

  // These are some base values 
  if (row["distance(km)"] < 0.1) {
    return 0;
  }
  if (pace <= 3 && rateOfClimb <= 150) {
    return 1;
  }

  // paceFactor gives about 3->1, 4->2, 5->4, 6->7, 7->15, 8->25
  // climbFactor gives about 150->1, 200->2, 250->4, 300->6, 350->8, 400->11, 450->14, 500->19, 550->24, 600->31
  const pace2 = pace ** 2;
  const pace4 = pace2 ** 2;
  const pace6 = pace2 ** 3;
  const climb2 = rateOfClimb ** 2;
  const climb4 = climb2 ** 2;

  const paceFactor = 0.1 * pace2 + 0.001 * pace4 + 0.00005 * pace6;
  const climbFactor = 0.00005 * climb2 + 0.0000000001 * climb4;
  const timeFactor = durationInH;

  return timeFactor * (paceFactor + paceFactor * climbFactor);
}

function computeBeatsPerMetre(row, durationInS) {
  const numMetres = row["elevation(m)"];
  if (numMetres <= 10) {
      return 0;
  }
  const numBeats = row["avg_heart_rate"] * (durationInS / 60);
  return numBeats / numMetres;
}

// TODO make separate dataloading module for this logic
// TODO also add the rest of the relevant loaders
async function loadHealthMetrics() {
  function row(r) {
    return {
      "date": new Date(r.date),
      "weight(lbs)": d3IntOrNull(r["weight(lbs)"]),
      "resting_heart_rate(bpm)": d3IntOrNull(r["resting_heart_rate(bpm)"]),
      "notes": r.notes,
    };
  }
  return await readCSV(`${base_data_path}/health_metrics.csv`, row);
}

async function loadWalks() {
  function row(r) {
    const durationInS = durationToS(r["duration(HH:mm:ss)"]);
    return {
      "date": new Date(r.date),
      "workout_type": r.workout_type,
      "duration(s)": durationInS,
      "distance(km)": d3NumOrNull(r["distance(km)"]),
      "steps": d3IntOrNull(r["steps"]),
      "elevation(m)": d3IntOrNull(r["elevation(m)"]),
      "weight(lbs)": d3NumOrNull(r["weight(lbs)"]),
      "avg_heart_rate": d3IntOrNull(r["avg_heart_rate"]),
      "max_heart_rate": d3IntOrNull(r["max_heart_rate"]),
      "score": computeWalkScore(r, durationInS),
      [bpmClimbField]: computeBeatsPerMetre(r, durationInS),
      "notes": r.notes,
    };
  }
  return await readCSV(`${base_data_path}/walks.csv`, row);
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

function durationToS(val) {
  const hoursToS = 60 * 60;
  const minsToS = 60;
  pieces = val.split(":")
  return hoursToS * +pieces[0] + minsToS * +pieces[1] + +pieces[2]
}

function containsCaseless (a, b) {
  return a.toLowerCase().includes(b.toLowerCase());
}

function d3NumOrNull(val) {
  return val === "" ? null : Number(val);
}

function d3IntOrNull(val) {
  return val === "" ? null : +val;
}

function d3Min(data, c_name) {
  return d3.min(data, function(row) { return row[c_name]; });
}

function d3Max(data, c_name) {
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
    .style("fill", "none")
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
    .call(d3.axisBottom(x)
      .ticks(d3.timeMonth.every(1))
      .tickFormat(date_tick))
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
      .tickValues(d3.range(minVal, maxVal + 1, majorStep)))
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

function plotWeight(healthMetrics, weightTrendline) {
  const minWeight = 180;
  const maxWeight = 305;
  const nDaysToExtrapolate = 100;

  const firstDate = d3Min(healthMetrics, "date");
  const lastDate = d3Max(healthMetrics, "date").addDays(nDaysToExtrapolate);

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
    .style("stroke-dasharray", ("8, 4"))
    .style("fill", "none");
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
    .selectAll("dot")
    .data(healthMetrics)
    .enter().append("circle")
      .filter(d => d["weight(lbs)"] !== null)
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
    .style("fill", "none")
    .attr("d", valueLine(weightTrendline));

  // Annotate object and append to the page
  svg.attr("id", weightGraphId);
  return svg;
}

function plotWorkoutFrequency(workoutFrequencies) {
  const minTime = 0;
  const maxTime = 210;

  const firstDate = d3Min(workoutFrequencies, "date");
  const lastDate = d3Max(workoutFrequencies, "date");

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
    .selectAll("dot")
    .data(workoutFrequencies)
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
    .attr("d", valueLine(workoutFrequencies));

  // Annotate object and append to the page
  svg.attr("id", workoutFrequencyGraphId);
  return svg;
}

function plotHeartRate(healthMetrics, heartRateTrendline) {
  const minHR = 45;
  const maxHR = 85;
  const nDaysToExtrapolate = 100;

  const firstDate = d3Min(heartRateTrendline, "date");
  const lastDate = d3Max(heartRateTrendline, "date");

  // Create the SVG container
  const svg = d3.create("svg")
    .attr("width", graphWidth)
    .attr("height", graphHeight);

  // Create the title, axes, and reference lines
  addTitle(svg, "Resting Heart Rate");
  addDateXAxis(svg, firstDate, lastDate);
  addLinearYAxis(svg, minHR, maxHR, 5, 1);
  addRefLine(svg, "Poor", minHR, maxHR, 82, RefLineType.Marker);
  addRefLine(svg, "Average", minHR, maxHR, 72, RefLineType.Marker);
  addRefLine(svg, "Above Average", minHR, maxHR, 68, RefLineType.Marker);
  addRefLine(svg, "Good", minHR, maxHR, 63, RefLineType.Marker);
  addRefLine(svg, "Excellent", minHR, maxHR, 58, RefLineType.Marker);
  addRefLine(svg, "Athlete", minHR, maxHR, 50, RefLineType.Marker);

  // Add the legend
  svg.append("text")
    .attr("x", graphWidth / 2 - legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Projected Resting HR")
    .attr("font-size", "0.8em");
  svg.append("line")
    .attr("x1", graphWidth / 2 - 1.05 * legendSpacing)
    .attr("y1", legendIconHeight)
    .attr("x2", graphWidth / 2 - 0.9 * legendSpacing)
    .attr("y2", legendIconHeight)
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .style("stroke-dasharray", ("8, 4"))
    .style("fill", "none");
  svg.append("text")
    .attr("x", graphWidth / 2 + legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Resting HR")
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
    .domain([minHR, maxHR])
    .range([axisBottom, graphMargin]);
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .selectAll("dot")
    .data(healthMetrics)
    .enter().append("circle")
      .filter(d => d["resting_heart_rate(bpm)"] !== null)
      .attr("cx", d => x(d["date"]))
      .attr("cy", d => y(d["resting_heart_rate(bpm)"]))
      .attr("r", 1.5);

  // Plot the trendline
  valueLine = d3.line()
    .x(function (d, i) { return x(d["date"]); })
    .y(function (d, i) { return y(d["resting_heart_rate(bpm)"]); });
  svg.append("path")
    .style("fill", "none")
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .style("stroke-dasharray", ("8, 4"))
    .style("fill", "none")
    .attr("d", valueLine(heartRateTrendline));

  // Annotate object and append to the page
  svg.attr("id", heartRateGraphId);
  return svg;
}

function plotBasic(data, field, title, graphId, minVal, maxVal, minorStep, majorStep) {
  // First filter out any null entries
  data = data.filter(d => d[field] !== null);

  const firstDate = d3Min(data, "date");
  const lastDate = d3Max(data, "date");

  // Create the SVG container
  const svg = d3.create("svg")
    .attr("width", graphWidth)
    .attr("height", graphHeight);

  // Create the title, axes, and reference lines
  addTitle(svg, title);
  addDateXAxis(svg, firstDate, lastDate);
  addLinearYAxis(svg, minVal, maxVal, minorStep, majorStep);

  // Plot each point
  const axisBottom = graphHeight - graphMargin;
  const x = d3.scaleUtc()
    .domain([firstDate, lastDate])
    .range([graphMargin, graphWidth - graphMargin]);
  const y = d3.scaleLinear()
    .domain([minVal, maxVal])
    .range([axisBottom, graphMargin]);
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .selectAll("dot")
    .data(data)
    .enter().append("circle")
      .attr("cx", d => x(d["date"]))
      .attr("cy", d => y(d[field]))
      .attr("r", 1.5);

  // Plot the line
  valueLine = d3.line()
    .x(function (d, i) { return x(d["date"]); })
    .y(function (d, i) { return y(d[field]); });
  svg.append("path")
    .style("fill", "none")
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .attr("d", valueLine(data));

  // Annotate object and append to the page
  svg.attr("id", graphId);
  return svg;
}

(async function() {
  // Load data
  const healthMetrics = await loadHealthMetrics();
  const walks = await loadWalks();
  //const bikes = readCSV(`${base_data_path}/bikes.csv`);
  //const runs = readCSV(`${base_data_path}/runs.csv`);
  //const weight_training_workouts = readCSV(`${base_data_path}/weight_training_workouts.csv`);
  //const weight_training_sets = readCSV(`${base_data_path}/weight_training_sets.csv`);
  //const travel_days = readCSV(`${base_data_path}/travel_days.csv`);

  // Load predictions
  const weightTrendline = await loadWeightTrendline();
  const workoutFrequency = await loadWorkoutFrequency();
  const heartRateTrendline = await loadHeartRateTrendline();

  // Build and display the main graphs; update width of entire document to fit
  var weightGraph = plotWeight(healthMetrics, weightTrendline).node();
  document.body.append(weightGraph);
  document.body.append(plotWorkoutFrequency(workoutFrequency).node());
  document.body.append(plotHeartRate(healthMetrics, heartRateTrendline).node());
  var docWidth = Math.max(weightGraph.width.baseVal.value, document.body.clientWidth);
  document.documentElement.style.width = `${docWidth}px`;

  // Position the secondary metrics dropbox selector appropriately
  //$(".dropdown").css("top", $(document).height());
  var dropdown = $(`#${extraChartDropdownId}`);
  $("body").append(dropdown);
  dropdown.css("display", "block");

  // Add the container that'll hold the secondary metric charts
  var extraChartContainer = $(document.createElement("div"));
  extraChartContainer.attr("id", extraChartContainerId);
  $("body").append(extraChartContainer);

  // TODO Build out more secondary metric graphs
  // TODO Include the strength over time metric graphs

  // Experiment with new graphs (defaults to hidden)
  // Experiment: Walk scores
  // TODO refine the formula
  const filteredWalks = walks
      .filter(d => d["workout_type"] == "walk (treadmill)")
      .filter(d => d["duration(s)"] >= 1200)
      .filter(d => !containsCaseless(d["notes"], "pre-workout"))
      .filter(d => !containsCaseless(d["notes"], "warm-up"))
      .filter(d => !containsCaseless(d["notes"], "post-workout"));
  var field = "score";
  var title = "Walk Scores";
  var walkScoresGraphId = "walk-scores-chart";
  expGraph = plotBasic(filteredWalks, field, title, walkScoresGraphId, 0, 200, 20, 5);
  expGraph.node().classList.add(secondaryGraphClassName);
  document.body.append(expGraph.node());

  // Experiment: Heartbeats required to climb a metre
  title = "BPMC (Beats Per Metre Climbed)";
  bpmcGraphId = "bpmc-climbed-chart";
  const bpmFilteredWalks = filteredWalks
      .filter(d => d[bpmClimbField] > 0)
      .filter(d => d["workout_type"] == "walk (treadmill)");
  expGraph = plotBasic(bpmFilteredWalks, bpmClimbField, title, bpmcGraphId, 0, 300, 100, 25);
  expGraph.node().classList.add(secondaryGraphClassName);
  document.body.append(expGraph.node());

  // Append the copyright now that the main graphs have been added
  var copyright = $("body").find("#copyright");
  copyright.css("width", `${weightGraph.getBoundingClientRect().width}px`);
  copyright.css("display", "block");
  $("body").append(copyright);
})();
