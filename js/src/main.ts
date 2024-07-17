type D3Graph = d3.Selection<SVGSVGElement, undefined, HTMLElement | null, any>;
type D3Row = Record<string, any>;

const base_data_path: string = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/data"
const pred_data_path: string = `${base_data_path}/preds`
const graphMargin: number = 100;
const graphWidth: number = 1600;
const graphHeight: number = 900;

const legendSpacing: number = 150;
const legendHeight: string = "5em";
const legendIconHeight: string = "3.75em";

const lineStrokeWidth: number = 2;

const weightGraphId: string = "graph-weight";
const workoutFrequencyGraphId: string = "graph-workout-frequency";
const heartRateGraphId: string = "graph-resting-heartrate";

const secondaryGraphClassName: string = "secondary-chart";
const bpmcField: string = "bpmc(beats_per_metre_climbed)";
const bpmmField: string = "bpmm(beats_per_metre_moved)";

const bullet: string = "\u2022";

// Data loading computed metrics
function computeWalkScore(row, durationInS): number {
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

function computeBeatsPerMetreClimbed(row, durationInS): number {
  const numMetres = row["elevation(m)"];
  if (numMetres <= 10) {
    return -1;
  }
  return getNumBeats(row, durationInS) / numMetres;
}

function computeBeatsPerMetreMoved(row, durationInS): number {
  const numMetres = row["distance(km)"] * 1000;
  if (numMetres <= 500) {
    return -1;
  }
  return getNumBeats(row, durationInS) / numMetres;
}

function getNumBeats(row, durationInS): number {
    return row["avg_heart_rate"] * (durationInS / 60);
}

// Data loading
// TODO make separate dataloading module for this logic
// TODO also add the rest of the relevant loaders
async function loadHealthMetrics() {
  function rowAccessor(r) {
    return {
      "date": new Date(r.date),
      "weight(lbs)": d3IntOrNull(r["weight(lbs)"]),
      "resting_heart_rate(bpm)": d3IntOrNull(r["resting_heart_rate(bpm)"]),
      "notes": r.notes,
    };
  }
  return await readCSV(`${base_data_path}/health_metrics.csv`, rowAccessor);
}

async function loadWalks() {
  function rowAccessor(r) {
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
      "notes": r.notes,
      "score": computeWalkScore(r, durationInS),
      [bpmcField]: computeBeatsPerMetreClimbed(r, durationInS),
    };
  }
  return await readCSV(`${base_data_path}/walks.csv`, rowAccessor);
}

async function loadRuns() {
  function rowAccessor(r) {
    const durationInS = durationToS(r["duration(HH:mm:ss)"]);
    return {
      "date": new Date(r.date),
      "workout_type": r.workout_type,
      "duration(s)": durationInS,
      "distance(km)": d3NumOrNull(r["distance(km)"]),
      "steps": d3IntOrNull(r["steps"]),
      "elevation(m)": d3IntOrNull(r["elevation(m)"]),
      "avg_heart_rate": d3IntOrNull(r["avg_heart_rate"]),
      "max_heart_rate": d3IntOrNull(r["max_heart_rate"]),
      "notes": r.notes,
      [bpmmField]: computeBeatsPerMetreMoved(r, durationInS),
    };
  }
  return await readCSV(`${base_data_path}/runs.csv`, rowAccessor);
}

async function loadBikes() {
  function rowAccessor(r) {
    const durationInS = durationToS(r["duration(HH:mm:ss)"]);
    return {
      "date": new Date(r.date),
      "workout_type": r.workout_type,
      "duration(s)": durationInS,
      "distance(km)": d3NumOrNull(r["distance(km)"]),
      "avg_resistance": d3NumOrNull(r["avg_resistance"]),
      "max_resistance": d3NumOrNull(r["max_resistance"]),
      "avg_cadence(rpm)": d3IntOrNull(r["avg_cadence(rpm)"]),
      "max_cadence(rpm)": d3IntOrNull(r["max_cadence(rpm)"]),
      "avg_wattage": d3IntOrNull(r["avg_wattage"]),
      "max_wattage": d3IntOrNull(r["max_wattage"]),
      "max_speed(km/h)": d3NumOrNull(r["max_speed(km/h)"]),
      "avg_heart_rate": d3IntOrNull(r["avg_heart_rate"]),
      "max_heart_rate": d3IntOrNull(r["max_heart_rate"]),
      "notes": r.notes,
    };
  }
  return await readCSV(`${base_data_path}/bikes.csv`, rowAccessor);
}

async function loadRows() {
  function rowAccessor(r) {
    const durationInS = durationToS(r["duration(HH:mm:ss)"]);
    return {
      "date": new Date(r.date),
      "workout_type": r.workout_type,
      "duration(s)": durationInS,
      "distance(km)": d3NumOrNull(r["distance(km)"]),
      "avg_resistance": d3NumOrNull(r["avg_resistance"]),
      "max_resistance": d3NumOrNull(r["max_resistance"]),
      "avg_cadence(rpm)": d3IntOrNull(r["avg_cadence(rpm)"]),
      "max_cadence(rpm)": d3IntOrNull(r["max_cadence(rpm)"]),
      "avg_wattage": d3IntOrNull(r["avg_wattage"]),
      "max_wattage": d3IntOrNull(r["max_wattage"]),
      "avg_heart_rate": d3IntOrNull(r["avg_heart_rate"]),
      "max_heart_rate": d3IntOrNull(r["max_heart_rate"]),
      "notes": r.notes,
    };
  }
  return await readCSV(`${base_data_path}/rows.csv`, rowAccessor);
}

async function loadWeightTrainingWorkouts() {
  function rowAccessor(row: D3Row) {
    const durationInS = durationToS(row["duration(HH:mm:ss)"]);
    return {
      "date": new Date(row.date),
      "workout_type": row.workout_type,
      "duration(s)": durationInS,
      "location": row.location,
      "notes": row.notes,
    };
  }
  return await readCSV(`${base_data_path}/weight_training_workouts.csv`, rowAccessor);
}

async function loadWeightTrendline() {
  function rowAccessor(row: D3Row) {
    return {
      "date": new Date(row.date),
      "weight(lbs)": Number(row["weight(lbs)"]),
    };
  }
  return await readCSV(`${pred_data_path}/weight_trendline.csv`, rowAccessor);
}

async function loadWorkoutFrequency() {
  function rowAccessor(row: D3Row) {
    return {
      "date": new Date(row.date),
      "duration": Number(row["duration(s)"]) / 60,
      "avg_duration": Number(row["avg_duration(s)"]) / 60,
    };
  }
  return await readCSV(`${pred_data_path}/avg_workout_durations.csv`, rowAccessor);
}

async function loadHeartRateTrendline() {
  function rowAccessor(row: D3Row) {
    return {
      "date": new Date(row.date),
      "resting_heart_rate(bpm)": Number(row["resting_heart_rate(bpm)"]),
    };
  }
  return await readCSV(`${pred_data_path}/resting_heart_rate_trendline.csv`, rowAccessor);
}

// Utilities
function nth(day): string {
  day = day.getDate();
  if (day > 3 && day < 21) {
    return "th";
  }
  switch (day % 10) {
    case 1:
      return "st";
    case 2:
      return "nd";
    case 3:
      return "rd";
    default:
      return "th";
  }
};

function month_day_nth(day): string {
    const month = day.toLocaleString("default", {month: "long"});
    return `${month} ${day.getDate()}${nth(day)}`;
}


interface Date {
    addDays(number): Date;
}

Date.prototype.addDays = function(days) {
    const date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
}

function durationToS(durationStr: string): number {
  const hoursToS: number = 60 * 60;
  const minsToS: number = 60;
  const pieces: string[] = durationStr.split(":")
  if (pieces.length != 3) {
    // TODO (ericlefort): No ValueError or InvalidArgumentError? Really JS? Gotta add my own..
    throw new Error(`Improperly formatted date: ${durationStr}`);
  }
  return hoursToS * Number(pieces[0]) + minsToS * Number(pieces[1]) + Number(pieces[2]);
}

function containsCaseless (a, b): boolean {
  return a.toLowerCase().includes(b.toLowerCase());
}

// D3 utilities
function d3NumOrNull(val): number | null {
  return val === "" ? null : Number(val);
}

function d3IntOrNull(val): number | null {
  return val === "" ? null : +val;
}

function d3Min(data, c_name): any {
  return d3.min(data, function(row: D3Row) { return row[c_name]; });
}

function d3Max(data, c_name): any {
  return d3.max(data, function(row: D3Row) { return row[c_name]; });
}

function d3Sum(data, c_name): number {
  return d3.sum(data, function(row: D3Row) { return row[c_name]; });
}

async function readCSV(path, rowAccessor) {
  return await d3.csv(path, rowAccessor);
}

// Plotting
function date_tick(d): string {
  const year = d.getYear() + 1900;  // Accommodating for library's weird year offset
  const month = d.toDateString().substring(4, 7);
  return `${month} ${year}`;
}

function time_tick(t): string {
  const mins = t % 60;
  const hours = (t - mins) / 60;
  if (hours > 0) {
    return `${hours}h ${mins}m`;
  }
  return `${mins}m`;
}

function addTitle(svg, title): void {
  const width = svg.node().width.animVal.value;
  svg.append("text")
    .attr("x", width / 2)
    .attr("y", "1em")
    .style("text-anchor", "middle")
    .style("font-weight", "bold")
    .text(title);
}

interface RefLineType {
  name: string;
}

class RefLineType {
  static Marker = new RefLineType("marker")
  static Threshold = new RefLineType("threshold")

  constructor(name) {
    this.name = name
  }
}

function addRefLine(svg, label, yMin, yMax, yRef, refLineType): void {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const contentHeight = height - graphMargin - graphMargin;
  const axisBottom = height - graphMargin;
  const yRange = yMax - yMin;
  const refLineOffset = yRef - yMin;

  const pos = axisBottom - contentHeight * (refLineOffset / yRange);
  const refLineRight = width - graphMargin;
  const labelPosition = refLineRight + 5;

  let strokeColour: string;
  let dashArray: string | null = null;
  if (refLineType === RefLineType.Marker) {
    strokeColour = "black";
    dashArray = "3, 2";
  } else if (refLineType === RefLineType.Threshold) {
    strokeColour = "red";
  } else {
    throw new TypeError(`Unexpected RefLineType: ${refLineType}`);
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

function addDateXAxis(svg, firstDate: Date, lastDate: Date): void {
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

function addLinearYAxis(svg, minVal, maxVal, majorStep, minorStep): void {
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

function addLinearTimeYAxis(svg, minTime, maxTime, majorStep, minorStep): void {
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

function plotWeight(healthMetrics, weightTrendline): D3Graph {
  const minWeight = 180;
  const maxWeight = 305;
  const nDaysToExtrapolate = 100;

  const firstDate: Date = new Date(d3Min(healthMetrics, "date"));
  const lastDate: Date = new Date(d3Max(healthMetrics, "date")).addDays(nDaysToExtrapolate);

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
      .filter((row: D3Row) => row["weight(lbs)"] !== null)
      .attr("cx", (row: D3Row) => x(row["date"]))
      .attr("cy", (row: D3Row) => y(row["weight(lbs)"]))
      .attr("r", 1.5);

  // Plot the trendline
  let valueLine = d3.line()
    .x(function (row: D3Row, _) { return x(row["date"]); })
    .y(function (row: D3Row, _) { return y(row["weight(lbs)"]); });
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

function plotWorkoutFrequency(workoutFrequencies): D3Graph {
  const minTime = 0;
  const maxTime = 210;

  const firstDate: Date = new Date(d3Min(workoutFrequencies, "date"));
  const lastDate: Date = new Date(d3Max(workoutFrequencies, "date"));

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
      .filter(function (row: D3Row) { return row["duration"] <= maxTime; })
      .attr("cx", (row: D3Row) => x(row["date"]))
      .attr("cy", (row: D3Row) => y(row["duration"]))
      .attr("r", 1.5);

  // Plot the trendline
  let valueLine = d3.line()
    .x(function (row: D3Row, _) { return x(row["date"]); })
    .y(function (row: D3Row, _) { return y(row["avg_duration"]); });
  svg.append("path")
    .style("fill", "none")
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .attr("d", valueLine(workoutFrequencies));

  // Annotate object and append to the page
  svg.attr("id", workoutFrequencyGraphId);
  return svg;
}

function plotHeartRate(healthMetrics, heartRateTrendline): D3Graph {
  const minHR: number = 45;
  const maxHR: number = 85;

  const firstDate: Date = new Date(d3Min(heartRateTrendline, "date"));
  const lastDate: Date = new Date(d3Max(heartRateTrendline, "date"));

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
      .filter((row: D3Row) => row["resting_heart_rate(bpm)"] !== null)
      .attr("cx", (row: D3Row) => x(row["date"]))
      .attr("cy", (row: D3Row) => y(row["resting_heart_rate(bpm)"]))
      .attr("r", 1.5);

  // Plot the trendline
  let valueLine = d3.line()
    .x(function (row: D3Row, _) { return x(row["date"]); })
    .y(function (row: D3Row, _) { return y(row["resting_heart_rate(bpm)"]); });
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

function plotBasic(data, field, title, graphId, minVal, maxVal, minorStep, majorStep): D3Graph {
  // First filter out any null entries
  data = data.filter((row: D3Row) => row[field] !== null);

  const firstDate: Date = new Date(d3Min(data, "date"));
  const lastDate: Date = new Date(d3Max(data, "date"));

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
      .attr("cx", (row: D3Row) => x(row["date"]))
      .attr("cy", (row: D3Row) => y(row[field]))
      .attr("r", 1.5);

  // Plot the line
  let valueLine = d3.line()
    .x(function (d, _) { return x(d["date"]); })
    .y(function (d, _) { return y(d[field]!); });
  svg.append("path")
    .style("fill", "none")
    .style("stroke", "steelblue")
    .style("stroke-width", lineStrokeWidth)
    .attr("d", valueLine(data));

  // Annotate object and append to the page
  svg.attr("id", graphId);
  return svg;
}

// Single-Day Summary
function computeSingleDaySummary(walks, runs, bikes, rows, weightTrainingWorkouts, day: Date | null = null): void {
  const summaryTextboxName = "single-day-summary-textbox";

  // These should be user-specific when that part gets built out
  const name = "Eric";

  // If a date isn't provided, use the most recent across all workout types
  if (day === null) {
      let day_time: number = new Date(d3Max(walks, "date")).getTime();
      day_time = Math.max(day_time, new Date(d3Max(runs, "date")).getTime());
      day_time = Math.max(day_time, new Date(d3Max(bikes, "date")).getTime());
      day_time = Math.max(day_time, new Date(d3Max(rows, "date")).getTime());
      day_time = Math.max(day_time, new Date(d3Max(weightTrainingWorkouts, "date")).getTime());
      day = new Date(day_time);
  }

  // Build up the daily workout summary text by each workout modality
  let lines = [`${name}'s most recent workout was ${month_day_nth(day)}\n`];
  lines.push(...buildDailyWalkingSummary(walks, day));
  lines.push(...buildDailyRunningSummary(runs, day));
  lines.push(...buildDailyBikingSummary(bikes, day));
  lines.push(...buildDailyRowingSummary(rows, day));
  lines.push(...buildDailyLiftingSummary(weightTrainingWorkouts, day));

  // No matching workouts, instead display a default message
  if (lines.length <= 1) {
      lines = ["No workouts recorded yet, get out there!\n "];
  }

  // Add the generated summary text to the textbox
  let textBox = $(`#${summaryTextboxName}`);
  textBox.text(lines.join("\n") +  "\n ");
  textBox.css("display", "flex");
}

function secondsToHHMM(durationInS): string {
  let durationInH = Math.floor(durationInS / 3600);
  let durationInM = `${Math.floor((durationInS % 3600) / 60)}`.padStart(2, "0");
  durationInS = `${Math.floor((durationInS % 3600) % 60)}`.padStart(2, "0");
  return `${durationInH}:${durationInM}:${durationInS}`;
}

function buildDailyWalkingSummary(walks, day): string[] {
    let day_as_time = day.getTime();
    walks = walks
      .filter((row: D3Row) => row["date"].getTime() == day_as_time);
    if (walks.length == 0) {
      return [];
    }

    let durationInS = d3Sum(walks, "duration(s)");
    let dist = d3Sum(walks, "distance(km)").toFixed(1);
    let elv = d3Sum(walks, "elevation(m)");
    let avgHR = d3Sum(walks, "avg_heart_rate") / walks.length;
    return [
      `${bullet} He walked for ${secondsToHHMM(durationInS)}`,
      `  Covering ${dist}km and climbing ${elv}m`,
      `  With an average heart rate of ${avgHR}bpm\n`,
    ];
}

function buildDailyRunningSummary(runs, day): string[] {
  let day_as_time = day.getTime();
  runs = runs
    .filter((row: D3Row) => row["date"].getTime() == day_as_time);
  if (runs.length == 0) {
    return [];
  }

  let durationInS = d3Sum(runs, "duration(s)");
  let dist = d3Sum(runs, "distance(km)").toFixed(1);
  let elv = d3Sum(runs, "elevation(m)");
  let avgHR = d3Sum(runs, "avg_heart_rate") / runs.length;
  return [
    `${bullet} He ran for ${secondsToHHMM(durationInS)}`,
    `  Covering ${dist}km and climbing ${elv}m`,
    `  With an average heart rate of ${avgHR}bpm\n`,
  ];
}

function buildDailyBikingSummary(bikes, day): string[] {
  let day_as_time = day.getTime();
  bikes = bikes
    .filter((row: D3Row) => row["date"].getTime() == day_as_time);
  if (bikes.length == 0) {
    return [];
  }

  let durationInS = d3Sum(bikes, "duration(s)");
  let dist = d3Sum(bikes, "distance(km)").toFixed(1);
  let kj = d3.sum(d3.map(bikes, (row: D3Row) => row["avg_wattage"] * row["duration(s)"]));
  kj = 0.001 * kj;  // This is just the conversion factor from Watt to KJ/s
  let avgHR = d3Sum(bikes, "avg_heart_rate") / bikes.length;
  return [
    `${bullet} He biked for ${secondsToHHMM(durationInS)}`,
    `  Covering ${dist}km with an output of ${kj}KJ`,
    `  And an average heart rate of ${avgHR}bpm\n`,
  ];
}

function buildDailyRowingSummary(rows, day): string[] {
  let day_as_time: number = day.getTime();
  rows = rows
    .filter((row: D3Row) => row["date"].getTime() == day_as_time);
  if (rows.length == 0) {
    return [];
  }

  let durationInS = d3Sum(rows, "duration(s)");
  let dist = d3Sum(rows, "distance(km)").toFixed(1);
  let kj = d3.sum(d3.map(rows, (row: D3Row) => row["avg_wattage"] * row["duration(s)"]));
  kj = 0.001 * kj;  // This is just the conversion factor from Watt to KJ/s
  kj = Math.floor(kj);
  let avgHR = d3Sum(rows, "avg_heart_rate") / rows.length;
  return [
    `${bullet} He rowed for ${secondsToHHMM(durationInS)}`,
    `  Covering ${dist}km with an output of ${kj}KJ`,
    `  And an average heart rate of ${avgHR}bpm\n`,
  ];
}

function buildDailyLiftingSummary(weightTrainingWorkouts, day): string[] {
  const day_as_time = day.getTime();
  weightTrainingWorkouts = weightTrainingWorkouts
    .filter((row: D3Row) => row["date"].getTime() == day_as_time);

  let lines: string[] = [];
  for (const workout of weightTrainingWorkouts) {
    let workoutType: number = workout["workout_type"];
    let durationInS: number = workout["duration(s)"];
    lines.push(`${bullet} He trained ${workoutType} for ${secondsToHHMM(durationInS)}`);
    // TODO Need to publish meta metrics with this from Python, I don't want to load set data in browser
    // lines.push(`He moved ${totalWeight}lbs across ${numSets} sets\n`);
  }
  return lines;
}

(async function() {
  // Load data
  const healthMetrics = await loadHealthMetrics();
  const walks = await loadWalks();
  const runs = await loadRuns();
  const bikes = await loadBikes();
  const rows = await loadRows();
  const weight_training_workouts = await loadWeightTrainingWorkouts();
  //const weight_training_sets = readCSV(`${base_data_path}/weight_training_sets.csv`);
  //const travel_days = readCSV(`${base_data_path}/travel_days.csv`);

  // Load predictions
  const weightTrendline = await loadWeightTrendline();
  const workoutFrequency = await loadWorkoutFrequency();
  const heartRateTrendline = await loadHeartRateTrendline();

  // Populate the default contents of the single-day summary
  computeSingleDaySummary(
      walks,
      runs,
      bikes,
      rows,
      weight_training_workouts,
  );

  // Build and display the main graphs; update width of entire document to fit
  let weightGraph: SVGSVGElement = plotWeight(healthMetrics, weightTrendline).node()!;
  document.body.append(weightGraph);
  document.body.append(plotWorkoutFrequency(workoutFrequency).node()!);
  document.body.append(plotHeartRate(healthMetrics, heartRateTrendline).node()!);
  let docWidth = Math.max(weightGraph.width.baseVal.value, document.body.clientWidth);
  document.documentElement.style.width = `${docWidth}px`;

  // Position the secondary metrics dropbox selector appropriately
  let dropdown = $(`#${extraChartDropdownId}`);
  $("body").append(dropdown);
  dropdown.css("display", "block");

  // Add the container that'll hold the secondary metric charts
  let extraChartContainer = $(document.createElement("div"));
  extraChartContainer.attr("id", extraChartContainerId);
  $("body").append(extraChartContainer);

  // TODO Build out more secondary metric graphs
  // TODO Include the strength over time metric graphs

  // Experiment with new graphs (defaults to hidden)
  // Experiment: Walk scores
  // TODO refine this formula
  const filteredWalks = walks
      .filter((row: D3Row) => row["workout_type"] == "walk (treadmill)")
      .filter((row: D3Row) => Number(row["duration(s)"]) >= 1200)
      .filter((row: D3Row) => !containsCaseless(row["notes"], "pre-workout"))
      .filter((row: D3Row) => !containsCaseless(row["notes"], "warm-up"))
      .filter((row: D3Row) => !containsCaseless(row["notes"], "post-workout"));
  let field: string = "score";
  let title: string = "Walk Scores";
  let walkScoresGraphId: string = "walk-scores-chart";
  let expGraph: D3Graph;
  let expNode: SVGSVGElement;
  expGraph = plotBasic(filteredWalks, field, title, walkScoresGraphId, 0, 200, 20, 5);
  expNode = expGraph.node()!;
  expNode.classList.add(secondaryGraphClassName);
  document.body.append(expNode);

  // Experiment: Heartbeats required to climb a metre
  // Note: Only considers walking since that's more efficient for elevation gain
  title = "BPMC (Beats Per Metre Climbed)";
  let bpmcGraphId: string = "bpmc-chart";
  const bpmcFilteredWalks = filteredWalks
      .filter((row: D3Row) => Number(row[bpmcField]) > 0)
      .filter((row: D3Row) => row["workout_type"] == "walk (treadmill)");
  expGraph = plotBasic(bpmcFilteredWalks, bpmcField, title, bpmcGraphId, 0, 300, 100, 25);
  expNode = expGraph.node()!;
  expNode.classList.add(secondaryGraphClassName);
  document.body.append(expNode);

  // Experiment: Heartbeats required to run a metre
  // Note: Only considers running since that's more efficient for covering horizontal distance
  title = "BPMM (Beats Per Metre Moved)";
  let bpmmGraphId: string = "bpmm-chart";
  const bpmmFilteredRuns = runs
      .filter((row: D3Row) => Number(row[bpmmField]) > 0);
  expGraph = plotBasic(bpmmFilteredRuns, bpmmField, title, bpmmGraphId, 0, 2, 1, 0.1);
  expNode = expGraph.node()!;
  expNode.classList.add(secondaryGraphClassName);
  document.body.append(expNode);

  // Append the copyright now that the main graphs have been added
  let copyright = $("body").find("#copyright");
  copyright.css("width", `${weightGraph.getBoundingClientRect().width}px`);
  copyright.css("display", "block");
  $("body").append(copyright);
})();
