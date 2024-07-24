"use strict";
const base_data_path = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/data";
const pred_data_path = `${base_data_path}/preds`;
const graphMargin = 100;
const graphWidth = 1600;
const graphHeight = 900;
const legendSpacing = 150;
const legendHeight = "5em";
const legendIconHeight = "3.75em";
const lineStrokeWidth = 2;
const extraChartDropdownId = "extra-chart-dropdown";
const weightGraphId = "graph-weight";
const workoutFrequencyGraphId = "graph-workout-frequency";
const heartRateGraphId = "graph-resting-heartrate";
const secondaryGraphClassName = "secondary-chart";
const bpmcField = "bpmc(beats_per_metre_climbed)";
const bpmmField = "bpmm(beats_per_metre_moved)";
const bullet = "\u2022";
function computeWalkScore(row, durationInS) {
    const durationInH = durationInS / 3600;
    const pace = row["distance(km)"] / durationInH;
    const rateOfClimb = row["elevation(m)"] / durationInH;
    if (row["distance(km)"] < 0.1) {
        return 0;
    }
    if (pace <= 3 && rateOfClimb <= 150) {
        return 1;
    }
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
function getNumBeats(row, durationInS) {
    return row["avg_heart_rate"] * (durationInS / 60);
}
function computeBeatsPerMetreClimbed(row, durationInS) {
    const numMetres = row["elevation(m)"];
    if (numMetres <= 10) {
        return -1;
    }
    return getNumBeats(row, durationInS) / numMetres;
}
function computeBeatsPerMetreMoved(row, durationInS) {
    const numMetres = row["distance(km)"] * 1000;
    if (numMetres <= 500) {
        return -1;
    }
    return getNumBeats(row, durationInS) / numMetres;
}
function nth(day) {
    const day_num = day.getDate();
    if (day_num > 3 && day_num < 21) {
        return "th";
    }
    switch (day_num % 10) {
        case 1:
            return "st";
        case 2:
            return "nd";
        case 3:
            return "rd";
        default:
            return "th";
    }
}
;
function month_day_nth(day) {
    const month = day.toLocaleString("default", { month: "long" });
    return `${month} ${day.getDate()}${nth(day)}`;
}
function addDays(day, numDays) {
    const date = new Date(day.valueOf());
    date.setDate(date.getDate() + numDays);
    return date;
}
function durationToS(durationStr) {
    const hoursToS = 60 * 60;
    const minsToS = 60;
    const pieces = durationStr.split(":");
    if (pieces.length !== 3) {
        throw new Error(`Improperly formatted date: ${durationStr}`);
    }
    return hoursToS * Number(pieces[0]) + minsToS * Number(pieces[1]) + Number(pieces[2]);
}
function containsCaseless(a, b) {
    return a.toLowerCase().includes(b.toLowerCase());
}
function d3NumOrNull(val) {
    return val === "" ? null : Number(val);
}
function d3IntOrNull(val) {
    return val === "" ? null : Number(val);
}
function d3Min(data, c_name) {
    return d3.min(data, function (row) { return row[c_name]; });
}
function d3Max(data, c_name) {
    return d3.max(data, function (row) { return row[c_name]; });
}
function d3Sum(data, c_name) {
    return d3.sum(data, function (row) { return row[c_name]; });
}
async function readCSV(path, rowAccessor) {
    return await d3.csv(path, rowAccessor);
}
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
    function rowAccessor(row) {
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
    function rowAccessor(row) {
        return {
            "date": new Date(row.date),
            "weight(lbs)": Number(row["weight(lbs)"]),
        };
    }
    return await readCSV(`${pred_data_path}/weight_trendline.csv`, rowAccessor);
}
async function loadWorkoutFrequency() {
    function rowAccessor(row) {
        return {
            "date": new Date(row.date),
            "duration": Number(row["duration(s)"]) / 60,
            "avg_duration": Number(row["avg_duration(s)"]) / 60,
        };
    }
    return await readCSV(`${pred_data_path}/avg_workout_durations.csv`, rowAccessor);
}
async function loadHeartRateTrendline() {
    function rowAccessor(row) {
        return {
            "date": new Date(row.date),
            "resting_heart_rate(bpm)": Number(row["resting_heart_rate(bpm)"]),
        };
    }
    return await readCSV(`${pred_data_path}/resting_heart_rate_trendline.csv`, rowAccessor);
}
function date_tick(d) {
    const year = d.getFullYear();
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
    const node = svg.node();
    if (node === null) {
        throw new Error("Encountered null SVG node when adding title.");
    }
    const width = node.width.animVal.value;
    svg.append("text")
        .attr("x", width / 2)
        .attr("y", "1em")
        .style("text-anchor", "middle")
        .style("font-weight", "bold")
        .text(title);
}
class RefLineType {
    constructor(name) {
        this.name = name;
    }
}
RefLineType.Marker = new RefLineType("marker");
RefLineType.Threshold = new RefLineType("threshold");
function addRefLine(svg, label, yMin, yMax, yRef, refLineType) {
    const node = svg.node();
    if (node === null) {
        throw new Error("Encountered null SVG node when adding reference line.");
    }
    const width = node.width.animVal.value;
    const height = node.height.animVal.value;
    const contentHeight = height - graphMargin - graphMargin;
    const axisBottom = height - graphMargin;
    const yRange = yMax - yMin;
    const refLineOffset = yRef - yMin;
    const pos = axisBottom - contentHeight * (refLineOffset / yRange);
    const refLineRight = width - graphMargin;
    const labelPosition = refLineRight + 5;
    let strokeColour;
    let dashArray;
    if (refLineType === RefLineType.Marker) {
        strokeColour = "black";
        dashArray = "3, 2";
    }
    else if (refLineType === RefLineType.Threshold) {
        strokeColour = "red";
        dashArray = "";
    }
    else {
        throw new TypeError(`Unexpected RefLineType: ${refLineType}`);
    }
    svg.append("text")
        .text(label)
        .attr("x", labelPosition)
        .attr("y", pos)
        .attr("dy", ".35em")
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
    const node = svg.node();
    if (node === null) {
        throw new Error("Encountered null SVG node when adding date-based x-axis.");
    }
    const width = node.width.animVal.value;
    const height = node.height.animVal.value;
    const axisBottom = height - graphMargin;
    const axisTop = height - graphMargin - graphMargin;
    const x = d3.scaleUtc()
        .domain([firstDate, lastDate])
        .range([graphMargin, width - graphMargin]);
    svg.append("g")
        .attr("transform", `translate(0, ${axisBottom})`)
        .call(d3.axisBottom(x)
        .ticks(d3.timeMonth.every(1))
        .tickFormat(date_tick))
        .call(g => g.selectAll(".tick line").clone()
        .attr("stroke-opacity", 0.3)
        .attr("y1", -axisTop));
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
    const node = svg.node();
    if (node === null) {
        throw new Error("Encountered null SVG node when adding linear y-axis.");
    }
    const width = node.width.animVal.value;
    const height = node.height.animVal.value;
    const axisBottom = height - graphMargin;
    const contentWidth = width - graphMargin - graphMargin;
    const y = d3.scaleLinear()
        .domain([minVal, maxVal])
        .range([axisBottom, graphMargin]);
    svg.append("g")
        .attr("transform", `translate(${graphMargin}, 0)`)
        .call(d3.axisLeft(y)
        .tickValues(d3.range(minVal, maxVal + 1, majorStep)))
        .call(g => g.selectAll(".tick line").clone()
        .attr("stroke-opacity", 0.3)
        .attr("x1", contentWidth));
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
    const node = svg.node();
    if (node === null) {
        throw new Error("Encountered null SVG node when adding time-based y-axis.");
    }
    const width = node.width.animVal.value;
    const height = node.height.animVal.value;
    const axisBottom = height - graphMargin;
    const contentWidth = width - graphMargin - graphMargin;
    const y = d3.scaleLinear()
        .domain([minTime, maxTime])
        .range([axisBottom, graphMargin]);
    svg.append("g")
        .attr("transform", `translate(${graphMargin}, 0)`)
        .call(d3.axisLeft(y)
        .tickValues(d3.range(minTime, maxTime + 1, majorStep))
        .tickFormat(time_tick))
        .call(g => g.selectAll(".tick line").clone()
        .attr("stroke-opacity", 0.3)
        .attr("x1", contentWidth));
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
function plotWeight(healthMetrics, weightTrendline) {
    const minWeight = 180;
    const maxWeight = 305;
    const nDaysToExtrapolate = 100;
    const firstDate = new Date(d3Min(healthMetrics, "date"));
    const lastDate = addDays(new Date(d3Max(healthMetrics, "date")), nDaysToExtrapolate);
    const svg = d3.create("svg")
        .attr("width", graphWidth)
        .attr("height", graphHeight);
    addTitle(svg, "Weight");
    addDateXAxis(svg, firstDate, lastDate);
    addLinearYAxis(svg, minWeight, maxWeight, 20, 5);
    addRefLine(svg, "Healthy", minWeight, maxWeight, 250, RefLineType.Marker);
    addRefLine(svg, "Target", minWeight, maxWeight, 200, RefLineType.Marker);
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
        .filter((row) => row["weight(lbs)"] !== null)
        .attr("cx", (row) => x(row["date"]))
        .attr("cy", (row) => y(row["weight(lbs)"]))
        .attr("r", 1.5);
    const valueLine = d3.line()
        .x(function (row, _) { return x(row["date"]); })
        .y(function (row, _) { return y(row["weight(lbs)"]); });
    svg.append("path")
        .style("stroke", "steelblue")
        .style("stroke-width", lineStrokeWidth)
        .style("stroke-dasharray", ("8, 4"))
        .style("fill", "none")
        .attr("d", valueLine(weightTrendline));
    svg.attr("id", weightGraphId);
    return svg;
}
function plotWorkoutFrequency(workoutFrequencies) {
    const minTime = 0;
    const maxTime = 210;
    const firstDate = new Date(d3Min(workoutFrequencies, "date"));
    const lastDate = new Date(d3Max(workoutFrequencies, "date"));
    const svg = d3.create("svg")
        .attr("width", graphWidth)
        .attr("height", graphHeight);
    addTitle(svg, "Workout Frequency");
    addDateXAxis(svg, firstDate, lastDate);
    addLinearTimeYAxis(svg, minTime, maxTime, 30, 10);
    addRefLine(svg, "Target Minimum", minTime, maxTime, 22.5, RefLineType.Threshold);
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
        .filter(function (row) { return row["duration"] <= maxTime; })
        .attr("cx", (row) => x(row["date"]))
        .attr("cy", (row) => y(row["duration"]))
        .attr("r", 1.5);
    const valueLine = d3.line()
        .x(function (row, _) { return x(row["date"]); })
        .y(function (row, _) { return y(row["avg_duration"]); });
    svg.append("path")
        .style("fill", "none")
        .style("stroke", "steelblue")
        .style("stroke-width", lineStrokeWidth)
        .attr("d", valueLine(workoutFrequencies));
    svg.attr("id", workoutFrequencyGraphId);
    return svg;
}
function plotHeartRate(healthMetrics, heartRateTrendline) {
    const minHR = 45;
    const maxHR = 85;
    const firstDate = new Date(d3Min(heartRateTrendline, "date"));
    const lastDate = new Date(d3Max(heartRateTrendline, "date"));
    const svg = d3.create("svg")
        .attr("width", graphWidth)
        .attr("height", graphHeight);
    addTitle(svg, "Resting Heart Rate");
    addDateXAxis(svg, firstDate, lastDate);
    addLinearYAxis(svg, minHR, maxHR, 5, 1);
    addRefLine(svg, "Poor", minHR, maxHR, 82, RefLineType.Marker);
    addRefLine(svg, "Average", minHR, maxHR, 72, RefLineType.Marker);
    addRefLine(svg, "Above Average", minHR, maxHR, 68, RefLineType.Marker);
    addRefLine(svg, "Good", minHR, maxHR, 63, RefLineType.Marker);
    addRefLine(svg, "Excellent", minHR, maxHR, 58, RefLineType.Marker);
    addRefLine(svg, "Athlete", minHR, maxHR, 50, RefLineType.Marker);
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
        .filter((row) => row["resting_heart_rate(bpm)"] !== null)
        .attr("cx", (row) => x(row["date"]))
        .attr("cy", (row) => y(row["resting_heart_rate(bpm)"]))
        .attr("r", 1.5);
    const valueLine = d3.line()
        .x(function (row, _) { return x(row["date"]); })
        .y(function (row, _) { return y(row["resting_heart_rate(bpm)"]); });
    svg.append("path")
        .style("fill", "none")
        .style("stroke", "steelblue")
        .style("stroke-width", lineStrokeWidth)
        .style("stroke-dasharray", ("8, 4"))
        .style("fill", "none")
        .attr("d", valueLine(heartRateTrendline));
    svg.attr("id", heartRateGraphId);
    return svg;
}
function plotBasic(data, field, title, graphId, minVal, maxVal, minorStep, majorStep) {
    data = data.filter((row) => row[field] !== null);
    const firstDate = new Date(d3Min(data, "date"));
    const lastDate = new Date(d3Max(data, "date"));
    const svg = d3.create("svg")
        .attr("width", graphWidth)
        .attr("height", graphHeight);
    addTitle(svg, title);
    addDateXAxis(svg, firstDate, lastDate);
    addLinearYAxis(svg, minVal, maxVal, minorStep, majorStep);
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
        .attr("cx", (row) => x(row["date"]))
        .attr("cy", (row) => y(row[field]))
        .attr("r", 1.5);
    const valueLine = d3.line()
        .x(function (row, _) { return x(row["date"]); })
        .y(function (row, _) { return y(row[field]); });
    svg.append("path")
        .style("fill", "none")
        .style("stroke", "steelblue")
        .style("stroke-width", lineStrokeWidth)
        .attr("d", valueLine(data));
    svg.attr("id", graphId);
    return svg;
}
function secondsToHHMM(durationInS) {
    const durationInH = Math.floor(durationInS / 3600);
    const durationInMStr = `${Math.floor((durationInS % 3600) / 60)}`.padStart(2, "0");
    const durationInSStr = `${Math.floor((durationInS % 3600) % 60)}`.padStart(2, "0");
    return `${durationInH}:${durationInMStr}:${durationInSStr}`;
}
function buildDailyWalkingSummary(walks, day) {
    const day_as_time = day.getTime();
    walks = walks
        .filter((row) => row["date"].getTime() === day_as_time);
    if (walks.length === 0) {
        return [];
    }
    const durationInS = d3Sum(walks, "duration(s)");
    const dist = d3Sum(walks, "distance(km)").toFixed(1);
    const elv = d3Sum(walks, "elevation(m)");
    const avgHR = d3Sum(walks, "avg_heart_rate") / walks.length;
    return [
        `${bullet} He walked for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km and climbing ${elv}m`,
        `  With an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyRunningSummary(runs, day) {
    const day_as_time = day.getTime();
    runs = runs
        .filter((row) => row["date"].getTime() === day_as_time);
    if (runs.length === 0) {
        return [];
    }
    const durationInS = d3Sum(runs, "duration(s)");
    const dist = d3Sum(runs, "distance(km)").toFixed(1);
    const elv = d3Sum(runs, "elevation(m)");
    const avgHR = d3Sum(runs, "avg_heart_rate") / runs.length;
    return [
        `${bullet} He ran for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km and climbing ${elv}m`,
        `  With an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyBikingSummary(bikes, day) {
    const day_as_time = day.getTime();
    bikes = bikes
        .filter((row) => row["date"].getTime() === day_as_time);
    if (bikes.length === 0) {
        return [];
    }
    const durationInS = d3Sum(bikes, "duration(s)");
    const dist = d3Sum(bikes, "distance(km)").toFixed(1);
    const avgHR = d3Sum(bikes, "avg_heart_rate") / bikes.length;
    let kj = d3.sum(d3.map(bikes, (row) => row["avg_wattage"] * row["duration(s)"]));
    kj *= 0.001;
    return [
        `${bullet} He biked for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km with an output of ${kj}KJ`,
        `  And an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyRowingSummary(rows, day) {
    const day_as_time = day.getTime();
    rows = rows
        .filter((row) => row["date"].getTime() === day_as_time);
    if (rows.length === 0) {
        return [];
    }
    const durationInS = d3Sum(rows, "duration(s)");
    const dist = d3Sum(rows, "distance(km)").toFixed(1);
    const avgHR = d3Sum(rows, "avg_heart_rate") / rows.length;
    let kj = d3.sum(d3.map(rows, (row) => row["avg_wattage"] * row["duration(s)"]));
    kj *= 0.001;
    kj = Math.floor(kj);
    return [
        `${bullet} He rowed for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km with an output of ${kj}KJ`,
        `  And an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyLiftingSummary(weightTrainingWorkouts, day) {
    const day_as_time = day.getTime();
    weightTrainingWorkouts = weightTrainingWorkouts
        .filter((row) => row["date"].getTime() === day_as_time);
    const lines = [];
    for (const workout of weightTrainingWorkouts) {
        const workoutType = workout["workout_type"];
        const durationInS = workout["duration(s)"];
        lines.push(`${bullet} He trained ${workoutType} for ${secondsToHHMM(durationInS)}`);
    }
    return lines;
}
function computeSingleDaySummary(walks, runs, bikes, rows, weightTrainingWorkouts, day = null) {
    const summaryTextboxName = "single-day-summary-textbox";
    const name = "Eric";
    if (day === null) {
        let day_time = new Date(d3Max(walks, "date")).getTime();
        day_time = Math.max(day_time, new Date(d3Max(runs, "date")).getTime());
        day_time = Math.max(day_time, new Date(d3Max(bikes, "date")).getTime());
        day_time = Math.max(day_time, new Date(d3Max(rows, "date")).getTime());
        day_time = Math.max(day_time, new Date(d3Max(weightTrainingWorkouts, "date")).getTime());
        day = new Date(day_time);
    }
    let lines = [`${name}'s most recent workout was ${month_day_nth(day)}\n`];
    lines.push(...buildDailyWalkingSummary(walks, day));
    lines.push(...buildDailyRunningSummary(runs, day));
    lines.push(...buildDailyBikingSummary(bikes, day));
    lines.push(...buildDailyRowingSummary(rows, day));
    lines.push(...buildDailyLiftingSummary(weightTrainingWorkouts, day));
    if (lines.length <= 1) {
        lines = ["No workouts recorded yet, get out there!\n "];
    }
    const textBox = $(`#${summaryTextboxName}`);
    textBox.text(`${lines.join("\n")}\n `);
    textBox.css("display", "flex");
}
(async function () {
    const healthMetrics = await loadHealthMetrics();
    const walks = await loadWalks();
    const runs = await loadRuns();
    const bikes = await loadBikes();
    const rows = await loadRows();
    const weight_training_workouts = await loadWeightTrainingWorkouts();
    const weightTrendline = await loadWeightTrendline();
    const workoutFrequency = await loadWorkoutFrequency();
    const heartRateTrendline = await loadHeartRateTrendline();
    computeSingleDaySummary(walks, runs, bikes, rows, weight_training_workouts);
    const weightGraph = plotWeight(healthMetrics, weightTrendline).node();
    const workoutFrequencyGraph = plotWorkoutFrequency(workoutFrequency).node();
    const heartRateGraph = plotHeartRate(healthMetrics, heartRateTrendline).node();
    if (weightGraph === null || workoutFrequencyGraph === null || heartRateGraph === null) {
        throw new Error("Issue building one of the main graphs.");
    }
    document.body.append(weightGraph);
    document.body.append(workoutFrequencyGraph);
    document.body.append(heartRateGraph);
    const docWidth = Math.max(weightGraph.width.baseVal.value, document.body.clientWidth);
    document.documentElement.style.width = `${docWidth}px`;
    const dropdown = $(`#${extraChartDropdownId}`);
    $("body").append(dropdown);
    dropdown.css("display", "block");
    const extraChartContainer = $(document.createElement("div"));
    extraChartContainer.attr("id", extraChartContainerId);
    $("body").append(extraChartContainer);
    const filteredWalks = walks
        .filter((row) => row["workout_type"] === "walk (treadmill)")
        .filter((row) => Number(row["duration(s)"]) >= 1200)
        .filter((row) => !containsCaseless(row["notes"], "pre-workout"))
        .filter((row) => !containsCaseless(row["notes"], "warm-up"))
        .filter((row) => !containsCaseless(row["notes"], "post-workout"));
    let title = "Walk Scores";
    const field = "score";
    const walkScoresGraphId = "walk-scores-chart";
    let expGraph = plotBasic(filteredWalks, field, title, walkScoresGraphId, 0, 200, 20, 5);
    let node = expGraph.node();
    if (node === null) {
        throw new Error("Issue building walk scores chart.");
    }
    node.classList.add(secondaryGraphClassName);
    document.body.append(node);
    title = "BPMC (Beats Per Metre Climbed)";
    const bpmcGraphId = "bpmc-chart";
    const bpmcFilteredWalks = filteredWalks
        .filter((row) => Number(row[bpmcField]) > 0)
        .filter((row) => row["workout_type"] === "walk (treadmill)");
    expGraph = plotBasic(bpmcFilteredWalks, bpmcField, title, bpmcGraphId, 0, 300, 100, 25);
    node = expGraph.node();
    if (node === null) {
        throw new Error("Issue building the BPMM graph");
    }
    node.classList.add(secondaryGraphClassName);
    document.body.append(node);
    title = "BPMM (Beats Per Metre Moved)";
    const bpmmGraphId = "bpmm-chart";
    const bpmmFilteredRuns = runs.filter((row) => Number(row[bpmmField]) > 0);
    expGraph = plotBasic(bpmmFilteredRuns, bpmmField, title, bpmmGraphId, 0, 2, 1, 0.1);
    node = expGraph.node();
    if (node === null) {
        throw new Error("Issue building the BPMM graph");
    }
    node.classList.add(secondaryGraphClassName);
    document.body.append(node);
    const copyright = $("body").find("#copyright");
    copyright.css("width", `${weightGraph.getBoundingClientRect().width}px`);
    copyright.css("display", "block");
    $("body").append(copyright);
})();
//# sourceMappingURL=main.js.map