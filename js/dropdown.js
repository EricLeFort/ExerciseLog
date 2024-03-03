/**
 * TODO (low priority)
 * This entire class assumes there's a single dropdown on the page. It should be extended to handle multiple.
 */

const baseImgPath = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/img"
const dropdownClassName = "dropdown";
const dropdownMenuClassName = "dropdown-menu";
const extraChartsMenuData = [
    {
        "name": "Experimental...",
        "submenu": [
            {"name": "Walk Scores"},
        ]
    }, {
        "name": "Health...",
        "submenu": [
            {"name": "TK"},
        ],
    }, {
        "name": "Endurance...",
        "submenu": [
            {"name": "TK"},
        ],
    }, {
        "name": "Strength...",
        "submenu": [
            {"name": "Arnold Press"},
            {"name": "Barbell Lunges"},
            {"name": "Bench Press"},
            {"name": "Bicep Curl"},
            {"name": "Cable Lying Hip Flexors"},
            {"name": "Arnold Press"},
            {"name": "Barbell Lunges"},
            {"name": "Bench Press"},
            {"name": "Bicep Curl"},
            {"name": "Cable Lying Hip Flexors"},
            {"name": "Concentration Curl"},
            {"name": "Deadlift"},
            {"name": "Delt Flies"},
            {"name": "Hammer Curl"},
            {"name": "Incline Dumbbell Bench Press"},
            {"name": "Lat Pulldown"},
            {"name": "Lateral Lift"},
            {"name": "Lawnmowers"},
            {"name": "Machine Hip Abductors"},
            {"name": "Machine Hip Adductors"},
            {"name": "Machine Pec Flies"},
            {"name": "Military Press"},
            {"name": "Overhead Tricep Extension"},
            {"name": "Pullovers"},
            {"name": "Seated Row"},
            {"name": "Shrugs"},
            {"name": "Single-Arm Farmer's Carry"},
            {"name": "Single-Leg Leg Curl"},
            {"name": "Skullcrushers"},
            {"name": "Squats"},
            {"name": "Strict Press"},
            {"name": "Tricep Pushdown"},
            {"name": "Tricep Pushdown (V-Bar)"},
            {"name": "Wide-Grip Pull-Up"},
        ],
    },
];

const extraChartsIdMap = {
    "Walk Scores": "walk-scores-chart",
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

/* Runtime set-on-load globals */
var firstSubMenus;

/**
 *  Attaches listeners to the dropdown menu
 */
function attachListeners() {
    $(".dropdown").on("click", function () {
        if ($(this).hasClass("closing")) {
            // This triggers once right when an item is selected, this debounces that
            $(this).removeClass("closing");
        } else if (!$(this).hasClass("active")) {
            $(this).attr("tabindex", 1).focus();
            $(this).toggleClass("active");
            var ddMenu = $(this).find(".dropdown-menu");
            ddMenu.slideToggle(100);
            ddMenu.css("display", "block");
            ddMenu.children("li").css("display", "block");
        }
    });
    $(".dropdown .dropdown-menu li").on("click", function () {
        if ($(this).hasClass("dropdown-leaf")) {
            var dropdown = $(this).parents(".dropdown");
            dropdown.find("span").text($(this).children("x").text());
            var ddInput = dropdown.find("input")
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

/**
 * Sets the secondary metric chart that should be made visible
 */
function setActiveExtraChart(oldChartName, newChartName) {
    var oldChartId = extraChartsIdMap[oldChartName];
    var newChartId = extraChartsIdMap[newChartName];

    if (oldChartId) {
        var oldChart = $(document).find(`#${oldChartId}`);
        oldChart.css("display", "none");
    }
    var newChart = $(document).find(`#${newChartId}`);
    // Haven't loaded this chart yet, download it
    if (newChart.length === 0) {
        // TODO this assumes every unloaded chart is a strenght chart but that won't always be true;
        // improve the design of this chunk
        loadStrengthChart(newChartName, newChartId);
    }
    newChart.css("display", "block");
}

function loadStrengthChart(chartName, chartId) {
    var img = $(document.createElement("img"));
    img.attr("id", chartId);
    img.css("width", "1600px");
    img.css("height", "900px");
    img.css("display", "block");
    img.css("margin", "0 auto");
    img.attr("src", `${baseImgPath}/strength/${chartName}.png`);
    img.attr("alt", chartName);
    img.addClass("svg");
    $("body").append(img);
}

/**
 * Hides all the nested ul's and li's in the dropdown
 */
function hideAll() {
    var dropdown = $(document).find(".dropdown");
    var ddMenu = $(document).find(".dropdown .dropdown-menu");
    ddMenu.css("display", "none");
    ddMenu.find("ul").css("display", "none");
    ddMenu.find("li").css("display", "none");
    closeDropdown();
}

/**
 * Updates the dropdown's state
 */
function closeDropdown() {
    $(document).find(".dropdown .dropdown-menu").slideUp(100);
    $(document).find(".dropdown").removeClass("active");
}

/**
 * Gets the first submenu of every dropdown on the page
 */
function initFirstSubMenus() {
    var dropdowns = document.getElementsByClassName(dropdownClassName);
    firstSubMenus = new Array(dropdowns.length);
    for (var i = 0; i < dropdowns.length; i++) {
        var candidate = dropdowns[i].getElementsByClassName(dropdownMenuClassName);
        if (candidate.length !== 1) {
            throw new Error("Detected invalid dropdown structure.");
        }
        firstSubMenus[i] = candidate[0];
    }
}

/**
 * Parses the dropdown menu
 */
function parseMenu() {
    for (var i = 0; i < firstSubMenus.length; i++) {
        parseSubMenu(
           firstSubMenus[i],
           extraChartsMenuData,
        );
    }
}

/**
 * Parses this layer of the menu and recursively parses any nested layers
 */
function parseSubMenu(listElement, data) {
    for (var i = 0; i < data.length; i++) {
        var nestedli = document.createElement("li");
        nestedli.setAttribute("style", "display: none;");
        nestedli.setAttribute("id", data[i].name);
        var link = document.createElement("x");
        link.appendChild(document.createTextNode(data[i].name));
        nestedli.appendChild(link);
        if (data[i].submenu != null) {
            nestedli.setAttribute("class", "dropdown-branch");
            var subListElement = document.createElement("ul");
            nestedli.appendChild(subListElement);
            parseSubMenu(subListElement, data[i].submenu);
        } else {
            nestedli.setAttribute("class", "dropdown-leaf");
        }
        listElement.appendChild(nestedli);
    }
}

/**
 * Shows the next level of the dropdown menu
 */
function showNodes(element) {
    $(element).find("ul").css("display", "block");
    $(element).find("li").css("display", "block");
}

/**
 * Hides the last level of the dropdown menu
 */
function hideNodes(element) {
    $(element).find("ul").css("display", "none");
    $(element).find("li").css("display", "none");
}

/**
 * Initialize the menu on window load
 */
window.onload=function() {
    initFirstSubMenus();
    parseMenu();
    attachListeners();
};
