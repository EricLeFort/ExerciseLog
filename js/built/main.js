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
function getNumBeats(row, durationInS) {
    return row["avg_heart_rate"] * (durationInS / 60);
}
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
            "notes": r.notes,
            "score": computeWalkScore(r, durationInS),
            [bpmcField]: computeBeatsPerMetreClimbed(r, durationInS),
        };
    }
    return await readCSV(`${base_data_path}/walks.csv`, row);
}
async function loadRuns() {
    function row(r) {
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
    return await readCSV(`${base_data_path}/runs.csv`, row);
}
async function loadBikes() {
    function row(r) {
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
    return await readCSV(`${base_data_path}/bikes.csv`, row);
}
async function loadRows() {
    function row(r) {
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
    return await readCSV(`${base_data_path}/rows.csv`, row);
}
async function loadWeightTrainingWorkouts() {
    function row(r) {
        const durationInS = durationToS(r["duration(HH:mm:ss)"]);
        return {
            "date": new Date(r.date),
            "workout_type": r.workout_type,
            "duration(s)": durationInS,
            "location": r.location,
            "notes": r.notes,
        };
    }
    return await readCSV(`${base_data_path}/weight_training_workouts.csv`, row);
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
function nth(day) {
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
}
;
function month_day_nth(day) {
    const month = day.toLocaleString("default", { month: "long" });
    return `${month} ${day.getDate()}${nth(day)}`;
}
Date.prototype.addDays = function (days) {
    const date = new Date(this.valueOf());
    date.setDate(date.getDate() + days);
    return date;
};
function durationToS(val) {
    const hoursToS = 60 * 60;
    const minsToS = 60;
    const pieces = val.split(":");
    return hoursToS * +pieces[0] + minsToS * +pieces[1] + +pieces[2];
}
function containsCaseless(a, b) {
    return a.toLowerCase().includes(b.toLowerCase());
}
function d3NumOrNull(val) {
    return val === "" ? null : Number(val);
}
function d3IntOrNull(val) {
    return val === "" ? null : +val;
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
async function readCSV(path, row) {
    return await d3.csv(path, row);
}
function date_tick(d) {
    const year = d.getYear() + 1900;
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
    constructor(name) {
        this.name = name;
    }
}
RefLineType.Marker = new RefLineType("marker");
RefLineType.Threshold = new RefLineType("threshold");
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
        strokeColour = "black";
        dashArray = "3, 2";
    }
    else if (refLineType === RefLineType.Threshold) {
        strokeColour = "red";
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
    const width = svg.node().width.animVal.value;
    const height = svg.node().height.animVal.value;
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
    const width = svg.node().width.animVal.value;
    const height = svg.node().height.animVal.value;
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
    const width = svg.node().width.animVal.value;
    const height = svg.node().height.animVal.value;
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
    const lastDate = new Date(d3Max(healthMetrics, "date")).addDays(nDaysToExtrapolate);
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
        .filter(d => d["weight(lbs)"] !== null)
        .attr("cx", d => x(d["date"]))
        .attr("cy", d => y(d["weight(lbs)"]))
        .attr("r", 1.5);
    let valueLine = d3.line()
        .x(function (d, _) { return x(d["date"]); })
        .y(function (d, _) { return y(d["weight(lbs)"]); });
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
        .filter(function (d) { return d["duration"] <= maxTime; })
        .attr("cx", d => x(d["date"]))
        .attr("cy", d => y(d["duration"]))
        .attr("r", 1.5);
    let valueLine = d3.line()
        .x(function (d, _) { return x(d["date"]); })
        .y(function (d, _) { return y(d["avg_duration"]); });
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
        .filter(d => d["resting_heart_rate(bpm)"] !== null)
        .attr("cx", d => x(d["date"]))
        .attr("cy", d => y(d["resting_heart_rate(bpm)"]))
        .attr("r", 1.5);
    let valueLine = d3.line()
        .x(function (d, _) { return x(d["date"]); })
        .y(function (d, _) { return y(d["resting_heart_rate(bpm)"]); });
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
    data = data.filter(d => d[field] !== null);
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
        .attr("cx", d => x(d["date"]))
        .attr("cy", d => y(d[field]))
        .attr("r", 1.5);
    let valueLine = d3.line()
        .x(function (d, _) { return x(d["date"]); })
        .y(function (d, _) { return y(d[field]); });
    svg.append("path")
        .style("fill", "none")
        .style("stroke", "steelblue")
        .style("stroke-width", lineStrokeWidth)
        .attr("d", valueLine(data));
    svg.attr("id", graphId);
    return svg;
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
    var lines = [`${name}'s most recent workout was ${month_day_nth(day)}\n`];
    lines.push(...buildDailyWalkingSummary(walks, day));
    lines.push(...buildDailyRunningSummary(runs, day));
    lines.push(...buildDailyBikingSummary(bikes, day));
    lines.push(...buildDailyRowingSummary(rows, day));
    lines.push(...buildDailyLiftingSummary(weightTrainingWorkouts, day));
    if (lines.length <= 1) {
        lines = ["No workouts recorded yet, get out there!\n "];
    }
    var textBox = $(`#${summaryTextboxName}`);
    textBox.text(lines.join("\n") + "\n ");
    textBox.css("display", "flex");
}
function secondsToHHMM(durationInS) {
    var durationInH = Math.floor(durationInS / 3600);
    var durationInM = `${Math.floor((durationInS % 3600) / 60)}`.padStart(2, "0");
    durationInS = `${Math.floor((durationInS % 3600) % 60)}`.padStart(2, "0");
    return `${durationInH}:${durationInM}:${durationInS}`;
}
function buildDailyWalkingSummary(walks, day) {
    const day_as_time = day.getTime();
    walks = walks
        .filter(d => d["date"].getTime() == day_as_time);
    if (walks.length == 0) {
        return [];
    }
    var durationInS = d3Sum(walks, "duration(s)");
    var dist = d3Sum(walks, "distance(km)").toFixed(1);
    var elv = d3Sum(walks, "elevation(m)");
    var avgHR = d3Sum(walks, "avg_heart_rate") / walks.length;
    return [
        `${bullet} He walked for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km and climbing ${elv}m`,
        `  With an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyRunningSummary(runs, day) {
    const day_as_time = day.getTime();
    runs = runs
        .filter(d => d["date"].getTime() == day_as_time);
    if (runs.length == 0) {
        return [];
    }
    var durationInS = d3Sum(runs, "duration(s)");
    var dist = d3Sum(runs, "distance(km)").toFixed(1);
    var elv = d3Sum(runs, "elevation(m)");
    var avgHR = d3Sum(runs, "avg_heart_rate") / runs.length;
    return [
        `${bullet} He ran for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km and climbing ${elv}m`,
        `  With an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyBikingSummary(bikes, day) {
    const day_as_time = day.getTime();
    bikes = bikes
        .filter(d => d["date"].getTime() == day_as_time);
    if (bikes.length == 0) {
        return [];
    }
    var durationInS = d3Sum(bikes, "duration(s)");
    var dist = d3Sum(bikes, "distance(km)").toFixed(1);
    var kj = d3.sum(d3.map(bikes, (row) => row["avg_wattage"] * row["duration(s)"]));
    kj = 0.001 * kj;
    var avgHR = d3Sum(bikes, "avg_heart_rate") / bikes.length;
    return [
        `${bullet} He biked for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km with an output of ${kj}KJ`,
        `  And an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyRowingSummary(rows, day) {
    const day_as_time = day.getTime();
    rows = rows
        .filter(d => d["date"].getTime() == day_as_time);
    if (rows.length == 0) {
        return [];
    }
    var durationInS = d3Sum(rows, "duration(s)");
    var dist = d3Sum(rows, "distance(km)").toFixed(1);
    var kj = d3.sum(d3.map(rows, (row) => row["avg_wattage"] * row["duration(s)"]));
    kj = 0.001 * kj;
    kj = Math.floor(kj);
    var avgHR = d3Sum(rows, "avg_heart_rate") / rows.length;
    return [
        `${bullet} He rowed for ${secondsToHHMM(durationInS)}`,
        `  Covering ${dist}km with an output of ${kj}KJ`,
        `  And an average heart rate of ${avgHR}bpm\n`,
    ];
}
function buildDailyLiftingSummary(weightTrainingWorkouts, day) {
    const day_as_time = day.getTime();
    weightTrainingWorkouts = weightTrainingWorkouts
        .filter(d => d["date"].getTime() == day_as_time);
    var lines = [];
    for (const workout of weightTrainingWorkouts) {
        var workoutType = workout["workout_type"];
        var durationInS = workout["duration(s)"];
        lines.push(`${bullet} He trained ${workoutType} for ${secondsToHHMM(durationInS)}`);
    }
    return lines;
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
    var weightGraph = plotWeight(healthMetrics, weightTrendline).node();
    document.body.append(weightGraph);
    document.body.append(plotWorkoutFrequency(workoutFrequency).node());
    document.body.append(plotHeartRate(healthMetrics, heartRateTrendline).node());
    var docWidth = Math.max(weightGraph.width.baseVal.value, document.body.clientWidth);
    document.documentElement.style.width = `${docWidth}px`;
    var dropdown = $(`#${extraChartDropdownId}`);
    $("body").append(dropdown);
    dropdown.css("display", "block");
    var extraChartContainer = $(document.createElement("div"));
    extraChartContainer.attr("id", extraChartContainerId);
    $("body").append(extraChartContainer);
    const filteredWalks = walks
        .filter(d => d["workout_type"] == "walk (treadmill)")
        .filter(d => Number(d["duration(s)"]) >= 1200)
        .filter(d => !containsCaseless(d["notes"], "pre-workout"))
        .filter(d => !containsCaseless(d["notes"], "warm-up"))
        .filter(d => !containsCaseless(d["notes"], "post-workout"));
    let field = "score";
    let title = "Walk Scores";
    let walkScoresGraphId = "walk-scores-chart";
    let expGraph;
    expGraph = plotBasic(filteredWalks, field, title, walkScoresGraphId, 0, 200, 20, 5);
    expGraph.node().classList.add(secondaryGraphClassName);
    document.body.append(expGraph.node());
    title = "BPMC (Beats Per Metre Climbed)";
    let bpmcGraphId = "bpmc-chart";
    const bpmcFilteredWalks = filteredWalks
        .filter(d => Number(d[bpmcField]) > 0)
        .filter(d => d["workout_type"] == "walk (treadmill)");
    expGraph = plotBasic(bpmcFilteredWalks, bpmcField, title, bpmcGraphId, 0, 300, 100, 25);
    expGraph.node().classList.add(secondaryGraphClassName);
    document.body.append(expGraph.node());
    title = "BPMM (Beats Per Metre Moved)";
    let bpmmGraphId = "bpmm-chart";
    const bpmmFilteredRuns = runs
        .filter(d => Number(d[bpmmField]) > 0);
    expGraph = plotBasic(bpmmFilteredRuns, bpmmField, title, bpmmGraphId, 0, 2, 1, 0.1);
    expGraph.node().classList.add(secondaryGraphClassName);
    document.body.append(expGraph.node());
    var copyright = $("body").find("#copyright");
    copyright.css("width", `${weightGraph.getBoundingClientRect().width}px`);
    copyright.css("display", "block");
    $("body").append(copyright);
})();
