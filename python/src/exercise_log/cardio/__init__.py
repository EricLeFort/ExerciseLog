"""Responsible for logic related to cardio activities."""

"""
Research questions:
    1. Height should be included as a factor (as mentioned here but only for flat ground:
        https://pubmed.ncbi.nlm.nih.gov/26679617/)
    2. Different configurations of holding weight would have some impact, what does that effect look like?
        (e.g. a ruck vs. a weight vest vs. a standard backpack)
"""


def compute_run_watts(weight: float, pace: float) -> float:
    """
    Compute an estimate of the metabolic cost of running.

    Room for growth:
        1. Set the efficiency_coefficient according to the runner's skill level
        2. Define/use a terrain_factor (it's not the same one as walking)
        3. Incorporate the cost of running with a load (a pack or a weight vest) -- this isn't in the literature
        4. Incorporate the cost of the vertical grade
        Idea: https://hetgeheimvanhardlopen.nl/wp-content/uploads/2017/02/17.-The-Energy-Cost-of-Running-on-hills.pdf

    Args:
        weight (float): The weight (in kg) of the person
        pace (float): The pace (in m/s)
    Returns:
        The wattage representing the total metabolic cost of running
    """
    efficiency_coefficient = 1.06  # Note: this is ~1.04 for a good runner, ~1.08 for an inefficient one
    return efficiency_coefficient * pace * weight


def compute_walk_watts(
    weight: float,
    pack_weight: float,
    pace: float,
    grade: float,
    terrain_factor: float,
) -> float:
    """
    Compute an estimate of the metabolic cost of walking, including the cost of carrying a pack.

    terrain_factor is a messy variable (https://jhp-ojs-tamucc.tdl.org/jhp/article/view/67/pdf_17) but some examples to
    use as a rough rule of thumb for now:
    1.0 - paved road/treadmill
    1.1 - dirt road
    1.2 - light brush
    1.5 - heavy brush
    1.8 - swamp
    2.1 - loose sand

    The equation probably falls apart for grades outside of the range of [0, 0.15] or so

    Args:
        weight (float): The weight (in kg) of the person
        pack_weight (float): The weight (in kg) of the pack
        pace (float): The pace (in m/s)
        grade (float): The percentage grade expressed as a decimal (e.g. 5% -> 0.05)
        terrain_factor (float): The terrain factor modifier
    Returns:
        The wattage representing the total metabolic cost of walking
    """
    a = compute_standing_metabolic_rate(weight)
    b = compute_pack_carry_metabolic_rate(weight, pack_weight)
    c = walk_metabolic_rate(weight, pack_weight, pace, grade, terrain_factor)
    return a + b + c


def compute_standing_metabolic_rate(weight: float) -> float:
    """
    Compute the metabolic cost (in watts) of standing.

    1.5 x weight

    Args:
        weight (float): The weight (in kg) of the person
    Returns:
        The wattage representing the expected metabolic energy
    """
    return 1.5 * weight


def compute_pack_carry_metabolic_rate(weight: float, pack_weight: float) -> float:
    """
    Compute the metabolic cost (in watts) of carrying a pack.

    2 * (pack_weight + weight) * (pack_weight / weight)^2

    Args:
        weight (float): The weight (in kg) of the person
        pack_weight (float): The weight (in kg) of the pack
    Returns:
        The wattage representing the expected metabolic energy
    """
    return 2 * (pack_weight + weight) * (pack_weight / weight) ** 2


def run_metabolic_rate(weight: float, pace: float) -> float:
    """
    Compute an estimate of the metabolic cost of running.

    Args:
        weight (float): The weight (in kg) of the person
        pace (float): The pace (in m/s)
    Returns:
        The wattage representing the expected metabolic energy
    """
    efficiency_coefficient = 1.06  # Note: this is ~1.04 for a good runner, ~1.08 for an inefficient one
    return efficiency_coefficient * pace * weight


def walk_metabolic_rate(weight: float, pack_weight: float, pace: float, grade: float, terrain_factor: float) -> float:
    """
    Compute the metabolic cost (in watts) of walking while wearing a pack.

    terrain_factor * (weight + pack_weight) * (1.5*pace^2 + 0.35*pace*grade)

    Args:
        weight (float): The weight (in kg) of the person
        pack_weight (float): The weight (in kg) of the pack
        pace (float): The pace (in m/s)
        grade (float): The percentage grade expressed as a decimal (e.g. 5% -> 0.05)
        terrain_factor (float): The terrain factor modifier
    Returns:
        The wattage representing the expected metabolic energy
    """
    # Reverse-engineered the 0.25 factor using wattages reported by a treadmill I use that also agrees closely on
    #   caloric expenditure with my Apple Watch, sample size of 1 but the rest is just the Pandolf equation
    return 0.25 * terrain_factor * (weight + pack_weight) * (1.5 * pace**2 + 0.35 * pace * grade)
