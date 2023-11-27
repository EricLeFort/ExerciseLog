const base_data_path = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/data"
const pred_data_path = `${base_data_path}/preds`
const graphMargin = 100;

const weightGraphId = "graph-weight-tmp";

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
  year = d.getYear() + 1900;  // Accommodating for library's weird year offset
  month = d.toDateString().substring(4, 7);
  return `${month} ${year}`;
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

function addRefLine(svg, label, yMin, yMax, yRef) {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const contentHeight = height - graphMargin - graphMargin;
  const axisBottom = height - graphMargin;
  const yRange = yMax - yMin;
  const refLineOffset = yRef - yMin;

  const pos = axisBottom - contentHeight * (refLineOffset / yRange);
  const refLineRight = width - graphMargin;
  const labelPosition = refLineRight + 5;
  svg.append("text")
    .text(label)
    .attr("x", labelPosition)
    .attr("y", pos)
    .attr("dy", ".35em")  // Centers the text on the reference line
    .attr("font-size", "0.8em");
  svg.append("line")
    .style("stroke", "black")
    .style("stroke-width", 2)
    .style("stroke-dasharray", ("3, 2"))
    .attr("x1", graphMargin)
    .attr("y1", pos)
    .attr("x2", refLineRight)
    .attr("y2", pos);
}

function addDateXAxis(svg) {
  const width = svg.node().width.animVal.value;
  const height = svg.node().height.animVal.value;
  const axisBottom = height - graphMargin;
  const axisTop = height - graphMargin - graphMargin;

  const x = d3.scaleUtc()
    .domain([first_date, last_date])
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

async function readCSV(path, row) {
  return await d3.csv(path, row);
}

function plotWeight(data, weightTrendline) {
  const minWeight = 180;
  const maxWeight = 305;
  const width = 1600;
  const height = 900;
  const nDaysToExtrapolate = 100;

  first_date = d3_min(data, "date");
  last_date = d3_max(data, "date").addDays(nDaysToExtrapolate);

  // Create the SVG container
  const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height);

  // Create the title, axes, and reference lines
  addTitle(svg, "Weight");
  addDateXAxis(svg);
  addLinearYAxis(svg, minWeight, maxWeight, 20, 5);
  addRefLine(svg, "Healthy", minWeight, maxWeight, 250);
  addRefLine(svg, "Target", minWeight, maxWeight, 200);
  
  // Add the legend
  const legendSpacing = 150;
  const legendHeight = "5em";
  const legendIconHeight = "3.75em";
  svg.append("text")
    .attr("x", width / 2 - legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Projected Weight")
    .attr("font-size", "0.8em");
  svg.append("line")
    .attr("x1", width / 2 - legendSpacing)
    .attr("y1", legendIconHeight)
    .attr("x2", width / 2 - 0.85 * legendSpacing)
    .attr("y2", legendIconHeight)
    .style("stroke", "steelblue")
    .style("stroke-width", 3)
    .style("stroke-dasharray", ("8, 4"));
  svg.append("text")
    .attr("x", width / 2 + legendSpacing / 2)
    .attr("y", legendHeight)
    .style("text-anchor", "middle")
    .text("Weight (lbs)")
    .attr("font-size", "0.8em");
  svg.append("g")
    .attr("fill", "steelblue")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .append("circle")
      .attr("cx", width / 2 + legendSpacing / 5)
      .attr("cy", legendIconHeight)
      .attr("r", 1.5);

  // Plot the data
  const axisBottom = height - graphMargin;
  weightData = data.map(function(d) {
    return {
      "date": d["date"],
      "weight(lbs)": d["weight(lbs)"],
    };
  });
  const x = d3.scaleUtc()
    .domain([first_date, last_date])
    .range([graphMargin, width - graphMargin]);
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
    .style("stroke-width", 2)
    .style("stroke-dasharray", ("8, 4"))
    .attr("d", valueLine(weightTrendline));

  // Annotate object and append to the page
  svg.attr("id", weightGraphId);
  return svg;
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

  // Build and display the graphs
  weightGraph = plotWeight(healthMetrics, weightTrendline);
  document.body.append(weightGraph.node());
})();
