/**
 * TODO (low priority)
 * This entire class assumes there's a single dropdown on the page. It should be extended to handle multiple.
 */
const extraChartContainerId = "extra-chart-container";

const baseImgPath = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/img"
const dropdownClassName = "dropdown";
const dropdownMenuClassName = "dropdown-menu";

const notFoundStr = "not-a-node";

class MenuData {
  name: string;
  /* eslint-disable no-use-before-define */  // This is valid, linter just isn't aware of recursive type defs
  submenus: (MenuData | string)[];
  /* eslint-enable no-use-before-define */

  constructor(name: string, submenus: (MenuData | string)[]) {
    this.name = name;
    this.submenus = submenus;
  }
}

// Defines the dropdown menu data for the extra charts
const experimentalSubmenuData = new MenuData(
  "Experimental...",
  [
    "Walk Scores",
    "BPMC (Beats Per Metre Climbed)",
    "BPMM (Beats Per Metre Moved)",
  ],
);
const healthSubmenuData = new MenuData(
  "Health...",
  ["TK"]
);
const enduranceSubmenuData = new MenuData(
  "Endurance...",
  ["TK"]
);
const strengthSubmenuData = new MenuData(
  "Strength...",
  [
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
  ],
);
const extraChartsMenuData = new MenuData(
  notFoundStr,
  [
    experimentalSubmenuData,
    healthSubmenuData,
    enduranceSubmenuData,
    strengthSubmenuData,
  ],
);

const extraChartsIdMap: Record<string, string> = {
  [notFoundStr]: notFoundStr,
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

/* Runtime set-on-load globals */
let submenuRoots: Element[];



/**
 * Shows the next level of the dropdown menu
 */
function showNodes(element: HTMLElement): void {
  $(element).find("ul").css("display", "block");
  $(element).find("li").css("display", "block");
}

/**
 * Hides the last level of the dropdown menu
 */
function hideNodes(element: HTMLElement): void {
  $(element).find("ul").css("display", "none");
  $(element).find("li").css("display", "none");
}

/**
 * Updates the dropdown's state
 */
function closeDropdown(): void {
  $(document).find(".dropdown .dropdown-menu").slideUp(100);
  $(document).find(".dropdown").removeClass("active");
}

/**
 * Hides all the nested ul's and li's in the dropdown
 */
function hideAll(): void {
  const ddMenu = $(document).find(".dropdown .dropdown-menu");
  ddMenu.css("display", "none");
  ddMenu.find("ul").css("display", "none");
  ddMenu.find("li").css("display", "none");
  closeDropdown();
}

function loadStrengthChart(chartName: string, chartId: string): void {
  const img = $(document.createElement("img"));
  img.attr("id", chartId);
  img.css("display", "block");
  img.css("margin", "0 auto");
  img.attr("src", `${baseImgPath}/strength/${chartName}.png`);
  img.attr("alt", chartName);
  $(`#${extraChartContainerId}`).append(img);
}

/**
 * Sets the secondary metric chart that should be made visible
 */
function setActiveExtraChart(oldChartName: string, newChartName: string): void {
  if (!(oldChartName in extraChartsIdMap)) {
    throw new Error(`Unrecognized old chart name: ${oldChartName}`);
  } else if (!(newChartName in extraChartsIdMap)) {
    throw new Error(`Unrecognized new chart name: ${newChartName}`);
  }
  const oldChartId: string = extraChartsIdMap[oldChartName] || notFoundStr;
  const newChartId: string = extraChartsIdMap[newChartName] || notFoundStr;

  if (oldChartId) {
    const oldChart = $(document).find(`#${oldChartId}`);
    oldChart.css("display", "none");
  }
  const newChart = $(document).find(`#${newChartId}`);
  // Haven't loaded this chart yet, download it
  if (newChart.length === 0) {
    // TODO this assumes every unloaded chart is a strenght chart but that won't always be true;
    // improve the design of this chunk
    loadStrengthChart(newChartName, newChartId);
  }
  newChart.css("display", "block");
}

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
      const ddMenu = $(this).find(".dropdown-menu");
      ddMenu.slideToggle(100);
      ddMenu.css("display", "block");
      ddMenu.children("li").css("display", "block");
    }
  });
  $(".dropdown .dropdown-menu li").on("click", function () {
    if ($(this).hasClass("dropdown-leaf")) {
      const dropdown = $(this).parents(".dropdown");
      dropdown.find("span").text($(this).children("x").text());
      const ddInput = dropdown.find("input");
      setActiveExtraChart(ddInput.attr("value") || notFoundStr, $(this).attr("id") || notFoundStr);
      ddInput.attr("value", $(this).attr("id") || notFoundStr);
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
 * Gets the first submenu of every dropdown on the page
 */
function initsubmenuRoots(): void {
  const dropdowns: HTMLCollection = document.getElementsByClassName(dropdownClassName);
  submenuRoots = [];
  for (const dropdown of dropdowns) {
    const candidate = dropdown.getElementsByClassName(dropdownMenuClassName);
    if (!candidate[0]) {
      throw new Error("Detected invalid dropdown structure.");
    }
    submenuRoots.push(candidate[0]);
  }
}

/**
 * Parses this layer of the menu and recursively parses any nested layers
 */
function parseSubMenu(listElement: Element, menuData: MenuData): void {
  for (const submenuData of menuData.submenus) {
    const isLeaf: boolean = typeof submenuData === "string" || submenuData instanceof String;
    const name: string = isLeaf ? submenuData as string : (submenuData as MenuData).name;
    const className: string = isLeaf ? "dropdown-leaf" : "dropdown-branch";

    const nestedli: Element = document.createElement("li");
    nestedli.setAttribute("style", "display: none;");
    nestedli.setAttribute("id", name);
    nestedli.setAttribute("class", className);
    const link: Element = document.createElement("x");
    link.appendChild(document.createTextNode(name));
    nestedli.appendChild(link);

    if (!isLeaf) {
      const subListElement: Element = document.createElement("ul");
      nestedli.appendChild(subListElement);
      parseSubMenu(subListElement, submenuData as MenuData);
    }
    listElement.appendChild(nestedli);
  }
}

/**
 * Parses the dropdown menu
 */
function parseMenu(): void {
  for (const submenuRoot of submenuRoots) {
    parseSubMenu(submenuRoot, extraChartsMenuData);
  }
}

/**
 * Initialize the menu on window load
 */
window.onload=function() {
  initsubmenuRoots();
  parseMenu();
  attachListeners();
};
