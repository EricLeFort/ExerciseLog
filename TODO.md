# TODO

## Low-Hanging Fruit
* Move language-specific configs into the proper subdirectory (e.g. requirements.txt should be in python/, package.json should be in js/)
* Extract shared structural information

## Most Important
* Fatigue scores
* Support multiple users

### Visualization
* Make a visualization for Watt/Kg for biking
* Make separate frequency graph view for each level in the hierarchy (e.g. all workouts, cardio vs. weights, specific type of cardio, etc.)
* Color-code data points in workout frequency graph to correspond to the different types of activity
* Graphs with selectable date range + a dynamic y-axis

### Python
* Extract shared structural information into separate, language-agnostic files so they can be shared with JS
    - Ontological information (e.g. the EXERCISE_INFO dict in ontology.py, heart rate thresholds, etc.)
    - Metadata (e.g. ColumnName values)
* Make Volume a first-class citizen for all domains
    - Make a visualization for volume (e.g. distance, HR zones, total watts for cardio + num sets by type, weight moved for strength)
    - Ideal weekly volume inspiration: https://www.reddit.com/r/weightroom/comments/6674a4/dr_mike_israetels_training_tips_for_hypertrophy
    - Research something like Dr. Mike's weekly volume recommendations but for individual and combined cardio modalities (and all training?)
* Unit testing framework for randomization + performance
    - Performance -- run N times, take top 10% as performance mark, assert M (<< 10%) tests beat that threshold
    - Randomization -- use seeds, any seeds that fail should be recorded, if there's any failed seeds -- run those first, on success -- clear failed seeds
    - For now, just write to the repo under some path in the test file tree
* Support multiple users
* Extend EXERCISE_INFO
    - Populate Muscle in EXERCISE_INFO
    - Populate percentages of Muscle/MuscleGroup in EXERCISE_INFO
* Define local and global ideal strength ratios
* Smooth out xRM logic
* Define an expiration and/or uncertainty range that crops up when xRM's get several months old
* Work out and implement the fatigue factor logic
* Make ExerciseInfo a parameterized singleton

### Site
* Make the non-main charts lazy-load
* Add testing framework and some simple wide-coverage, simple validation tests
* Extract constants
* Break up main.js into better sub-components/sub-files
* Migrate to React
* Bug: dropdown doesn't work well with long text -- let cell height expand for multi-line? Or modify its width and/or shorten the text itself.
* Make domain (date ranges) selectable for any given graph
    - Create the selectable domain functionality
    - Auto-determine the range (min/max, major step, minor step) given the values
    - Add a "back to full" button
* Plot a combined metric using rate_of_climb + pace (+ duration?)
    - Experiment with adding duration into the equation (maybe also something like a strive score using avg, max + duration?)
* Use the data in the ontological files (see Python section above) for thresholds
* When I extend to multi-user, start by making template users for continuous manual UX testing:
    - brand new user with no data
    - single entry in weight training OR cardio
    - some entries in only weight training OR cardio
    - user with some entries in weight training OR cardio AND a single entry in the other (and vice versa)
    - user with some entries in both categories

### Database (removes the need to support any data analysis in JS, can also purge visualization support from Python and get clean separation)
* Create one (performance doesn't matter but flexibility does) (DynamoDB on AWS is fine for now)

### UI
* Design Ideas:
    * Three main modes:
        1. Session Planning (single or multi-session level)
        2. Session Companion
        3. Performance Analysis
        4. Training Targets
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
            * Third-level views: Walking + Running + Biking + Swimming ++ Muscle Group (do I care about *time* for muscle training?)
            * Fourth-level views: Hiking + Treadmill walking + Outdoor walking ++ - ++ Stationary biking + Outdoor biking +++ Individual muscle
    * Muscle heat-maps (high-level visual view, clickable to view an in-depth hierarchical view)
    * Setup automated testing for the UI
    * Top-level overview will include:
        * Percentage + absolute volume/time of training during the past week {weight training, calisthenics, cardio}
        * Cardio Health: 2-week average resting heart rate, V02 Max
        * Major strength metrics: 1RM of the big three + strict press
        * Single total strength imbalance score (0 is perfect, +inf is the upper bound)
        * Track exercises that count seconds or steps differently than those that count reps (e.g. plank)
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
        * Muscular endurance (AMRAP pushups, pullups, walking lunges with 100lbs, deadlift with 135lbs, bicep curls with 20lbs, strict press with 100lbs)
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
    * Can the entire companion app functionality be hosted on something like an Apple Watch? Would be nice to remove the necessity of having a phone on hand
    * Build out a prompt to gauge max values at some irregular interval (e.g. "test your max pushups + pullups" one day, "test your 1RM bench press" another -- 1RMs need at least a one week buildup though)
    * Health trackers don't do a great job of accounting for the caloric cost of weight training IMO, maybe there's a better rule of thumb to be applied given we know the exact sets being performed?
    * Add a way to visualize a user's training plan by week, month, mesocycle, etc. (historical to start but maybe a planning version at some point? could also include a diff between the plan and reality)
