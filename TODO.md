# TODO

### Python
* Smooth out 1RM logic
* Define an expiration and/or uncertainty range that crops up when xRM's get several months old
* Color-code data points in workout frequency graph to correspond to the different types of activity
* Make separate frequency graph view for each level in the hierarchy (e.g. all workouts, cardio vs. weights, specific type of cardio, etc.)
* Populate Muscle in EXERCISE_INFO
* Populate percentages of Muscle/MuscleGroup in EXERCISE_INFO
* Ideal weekly volume inspiration: https://www.reddit.com/r/weightroom/comments/6674a4/dr_mike_israetels_training_tips_for_hypertrophy/

### Site
* Replicate Python graphing using js so that it can work dynamically (and so I can purge the graph .png's from the repo)

### UI
* Design Ideas:
    * Three main modes:
        1. Session Planning (single or multi-session level)
        2. Session Companion
        3. Performance Analysis
    * Main Views:
        * Session builder
            * Start from previous session
            * Add sets
            * Select or infer the session focus
            * Session fatigue score
            * Muscle heat map
            * Prompt for missed muscle groups relative to a selected focus
            * Suggested exercises to fill the gaps
        * Session companion (session focus, remaining exercises, current exercise, utility to add a set)
        * Exercise lookup (prompts, muscles worked, historical weight/reps)
        * Data Views for each level of granularity
            * Top-level view: All workout types
            * Second-level views: Cardio + Weight Training + Calisthenics
            * Third-level views: Walking + Running + Biking + Swimming ++ Muscle Group
            * Fourth-level views: Hiking + Treadmill walking + Outdoor walking ++ - ++ Stationary biking + Outdoor biking +++ Individual muscle
    * Muscle heat-maps (high-level visual view, clickable to view an in-depth hierarchical view)
    * Setup automated testing for the UI
    * Top-level overview will include:
        * Percentage + absolute volume/time of training during the past week {weight training, calisthenics, cardio}
        * Cardio Health: 2-week average resting heart rate, V02 Max
        * Major strength metrics: 1RM of the big three + strict press
        * Single total strength imbalance score (0 is perfect, +inf is the upper bound)
        * Push/pull/legs-level aggregate imbalance scores
        * Absolute strength score + bodyweight-relative strength score
        * Highlight-able weaknesses (e.g. any significant outliers such as "weak triceps")
        * Highlight-able next-workout recommendations (e.g. {high-intensity, steady state, etc} cardio of type X or weight training of type X with a focus on {low, mid, high} reps) (dependent on user-defined training goal?)
    * Cardio overview will include:
        * Training distribution between the different modalities
        * Walking: 1km time, 5km time, 1000ft climb time, max 1-min walking pace
        * Running: 100m sprint, 1 mile time, 5km time, half-marathon time, marathon time, maximum duration
        * Swimming: 400m freestyle time?, 1000m freestyle time?
    * Weight training overview will include:
        * Include major strength metrics here as well for convenience?
        * Compound vs isolated lift ratios for each muscle group (highlight ones with particularly low isolated frequencies? and recommend specific exercises to program in?)
        * Minor strength metrics organized by muscle group:
            * Chest: incline dumbbell press
            * Arms: 1RM overhead tricep extension, preacher curl
            * Legs: 1RM leg curl, leg extension, seated calf raise
            * Back: 1RM lawnmowers, lat pulldown
            * Shoulders: 1RM arnold press
            * Forearms: deadhang duration? grip strength in newtons?
            * Local imbalance measures
                * Unilateral vs. bilateral movements: bicep curl, overhead tricep extension, leg curl, leg extension, etc. (ideally bilateral should be around 2 * single-arm/leg + 20% or so)
                * Primary/antagonist muscle pair strength ratios: (e.g. tricep vs. bicep, quads vs. hamstring, back vs. chest, calf/forearm extensors vs. flexors)
    * Calisthenics overview will include:
        * max consecutive push-ups, pull-ups, burpees; static hang duration, vertical leap?
    * Detailed Training Frequency Info
        * Percentage + absolute volume/time of {weight training, calisthenics, cardio}
        * A drill-down on compound lifts, isolated lifts, muscle groups, cardio types