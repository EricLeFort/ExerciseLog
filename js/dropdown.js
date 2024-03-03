/**
 * TODO (low priority)
 * This entire class assumes there's a single dropdown on the page. It should be extended to handle multiple.
 */

var dropdownClassName = "dropdown";
var dropdownMenuClassName = "dropdown-menu";
var extraChartsMenuData = [
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
        ],
    },
];

// TODO finish populating this
var extraChartsIdMap = {
    "Walk Scores": "walk-scores-chart",
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

function setActiveExtraChart(oldVal, newVal) {
    var oldChartId = extraChartsIdMap[oldVal];
    var newChartId = extraChartsIdMap[newVal];

    if (oldChartId) {
        var oldChart = $(document).find(`#${oldChartId}`);
        oldChart.css("display", "none");
    }
    var newChart = $(document).find(`#${newChartId}`);
    newChart.css("display", "block");
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
