"use strict";
const extraChartDropdownId = "extra-chart-dropdown";
const extraChartContainerId = "extra-chart-container";
const baseImgPath = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/img";
const dropdownClassName = "dropdown";
const dropdownMenuClassName = "dropdown-menu";
class MenuData {
    constructor(name, submenus) {
        this.name = name;
        this.submenus = submenus;
    }
}
const experimentalSubmenuData = new MenuData("Experimental...", [
    "Walk Scores",
    "BPMC (Beats Per Metre Climbed)",
    "BPMM (Beats Per Metre Moved)",
]);
const healthSubmenuData = new MenuData("Health...", ["TK"]);
const enduranceSubmenuData = new MenuData("Endurance...", ["TK"]);
const strengthSubmenuData = new MenuData("Strength...", [
    "Arnold Press",
    "Barbell Lunges",
    "Bench Press",
    "Bicep Curl",
    "Cable Lying Hip Flexors",
    "Arnold Press",
    "Barbell Lunges",
    "Bench Press",
    "Bicep Curl",
    "Cable Lying Hip Flexors",
    "Concentration Curl",
    "Deadlift",
    "Delt Flies",
    "Hammer Curl",
    "Incline Dumbbell Bench Press",
    "Lat Pulldown",
    "Lateral Lift",
    "Lawnmowers",
    "Machine Hip Abductors",
    "Machine Hip Adductors",
    "Machine Pec Flies",
    "Military Press",
    "Overhead Tricep Extension",
    "Pullovers",
    "Seated Row",
    "Shrugs",
    "Single-Arm Farmer's Carry",
    "Single-Leg Leg Curl",
    "Skullcrushers",
    "Squats",
    "Strict Press",
    "Tricep Pushdown",
    "Tricep Pushdown (V-Bar)",
    "Wide-Grip Pull-Up",
]);
const extraChartsMenuData = new MenuData("", [
    experimentalSubmenuData,
    healthSubmenuData,
    enduranceSubmenuData,
    strengthSubmenuData,
]);
const extraChartsIdMap = {
    "": "",
    "Walk Scores": "walk-scores-chart",
    "BPMC (Beats Per Metre Climbed)": "bpmc-chart",
    "BPMM (Beats Per Metre Moved)": "bpmm-chart",
    "Arnold Press": "arnold-press-chart",
    "Barbell Lunges": "barbell-lunges-chart",
    "Bench Press": "bench-press-chart",
    "Bicep Curl": "bicep-curl-chart",
    "Cable Lying Hip Flexors": "cable-lying-hip-flexors-chart",
    "Concentration Curl": "concentration-curl",
    "Deadlift": "deadlift-chart",
    "Delt Flies": "delt-flies-chart",
    "Hammer Curl": "hammer-curl-chart",
    "Incline Dumbbell Bench Press": "incline-dumbbell-bench-press-chart",
    "Lat Pulldown": "lat-pulldown-chart",
    "Lateral Lift": "lateral-lift-chart",
    "Lawnmowers": "lawnmowers-chart",
    "Machine Hip Abductors": "machine-hip-abductors-chart",
    "Machine Hip Adductors": "machine-hip-abductors-chart",
    "Machine Pec Flies": "machine-pec-flies-chart",
    "Military Press": "military-press-chart",
    "Overhead Tricep Extension": "overhead-tricep-extension-chart",
    "Pullovers": "pullovers-chart",
    "Seated Row": "seated-row-chart",
    "Shrugs": "shrugs-chart",
    "Single-Arm Farmer's Carry": "single-arm-farmers-carry-chart",
    "Single-Leg Leg Curl": "single-leg-leg-curl-chart",
    "Single-Leg Leg Extension": "single-leg-leg-extension-chart",
    "Skullcrushers": "skullcrushers-chart",
    "Squats": "squats-chart",
    "Strict Press": "strict-press-chart",
    "Tricep Pushdown": "tricep-pushdown-chart",
    "Tricep Pushdown (V-Bar)": "tricep-pushdown-v-bar-chart",
    "Wide-Grip Pull-Up": "wide-grip-pull-up-chart",
};
let submenuRoots;
function attachListeners() {
    $(".dropdown").on("click", function () {
        if ($(this).hasClass("closing")) {
            $(this).removeClass("closing");
        }
        else if (!$(this).hasClass("active")) {
            $(this).attr("tabindex", 1).focus();
            $(this).toggleClass("active");
            let ddMenu = $(this).find(".dropdown-menu");
            ddMenu.slideToggle(100);
            ddMenu.css("display", "block");
            ddMenu.children("li").css("display", "block");
        }
    });
    $(".dropdown .dropdown-menu li").on("click", function () {
        if ($(this).hasClass("dropdown-leaf")) {
            let dropdown = $(this).parents(".dropdown");
            dropdown.find("span").text($(this).children("x").text());
            let ddInput = dropdown.find("input");
            setActiveExtraChart(ddInput.attr("value"), $(this).attr("id"));
            ddInput.attr("value", $(this).attr("id"));
            dropdown.addClass("closing");
            hideAll();
        }
    });
    $(".dropdown").on("focusout", function () {
        hideAll();
    });
    $(".dropdown-menu > li").on("mouseenter", function () {
        showNodes(this);
    });
    $(".dropdown-menu > li").on("mouseleave", function () {
        hideNodes(this);
    });
}
function setActiveExtraChart(oldChartName, newChartName) {
    if (!(oldChartName in extraChartsIdMap)) {
        throw new Error(`Unrecognized old chart name: ${oldChartName}`);
    }
    else if (!(newChartName in extraChartsIdMap)) {
        throw new Error(`Unrecognized new chart name: ${newChartName}`);
    }
    let oldChartId = extraChartsIdMap[oldChartName];
    let newChartId = extraChartsIdMap[newChartName];
    if (oldChartId) {
        let oldChart = $(document).find(`#${oldChartId}`);
        oldChart.css("display", "none");
    }
    let newChart = $(document).find(`#${newChartId}`);
    if (newChart.length === 0) {
        loadStrengthChart(newChartName, newChartId);
    }
    newChart.css("display", "block");
}
function loadStrengthChart(chartName, chartId) {
    let img = $(document.createElement("img"));
    img.attr("id", chartId);
    img.css("display", "block");
    img.css("margin", "0 auto");
    img.attr("src", `${baseImgPath}/strength/${chartName}.png`);
    img.attr("alt", chartName);
    $(`#${extraChartContainerId}`).append(img);
}
function hideAll() {
    let ddMenu = $(document).find(".dropdown .dropdown-menu");
    ddMenu.css("display", "none");
    ddMenu.find("ul").css("display", "none");
    ddMenu.find("li").css("display", "none");
    closeDropdown();
}
function closeDropdown() {
    $(document).find(".dropdown .dropdown-menu").slideUp(100);
    $(document).find(".dropdown").removeClass("active");
}
function initsubmenuRoots() {
    let dropdowns = document.getElementsByClassName(dropdownClassName);
    submenuRoots = [];
    for (const dropdown of dropdowns) {
        let candidate = dropdown.getElementsByClassName(dropdownMenuClassName);
        if (candidate.length !== 1) {
            throw new Error("Detected invalid dropdown structure.");
        }
        submenuRoots.push(candidate[0]);
    }
}
function parseMenu() {
    for (const submenuRoot of submenuRoots) {
        parseSubMenu(submenuRoot, extraChartsMenuData);
    }
}
function parseSubMenu(listElement, menuData) {
    for (const submenuData of menuData.submenus) {
        let isLeaf = typeof submenuData === "string" || submenuData instanceof String;
        let name = isLeaf ? submenuData : submenuData.name;
        let className = isLeaf ? "dropdown-leaf" : "dropdown-branch";
        let nestedli = document.createElement("li");
        nestedli.setAttribute("style", "display: none;");
        nestedli.setAttribute("id", name);
        nestedli.setAttribute("class", className);
        let link = document.createElement("x");
        link.appendChild(document.createTextNode(name));
        nestedli.appendChild(link);
        if (!isLeaf) {
            let subListElement = document.createElement("ul");
            nestedli.appendChild(subListElement);
            parseSubMenu(subListElement, submenuData);
        }
        listElement.appendChild(nestedli);
    }
}
function showNodes(element) {
    $(element).find("ul").css("display", "block");
    $(element).find("li").css("display", "block");
}
function hideNodes(element) {
    $(element).find("ul").css("display", "none");
    $(element).find("li").css("display", "none");
}
window.onload = function () {
    initsubmenuRoots();
    parseMenu();
    attachListeners();
};
