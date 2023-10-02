# Exercise Log
This is a project that started as an easy way to track my fitness over time in the ways I am interested in tracking it.

Check out the companion [Instagram account](https://www.instagram.com/its.today.again/) which I use as a way to visually track my progress.

I also maintain a scrappy [GitHub Pages site](https://ericlefort.github.io/ExerciseLog/) to showcase some of the more high-level metrics.

This codebase has grown organically from there over time as I added new features I felt were useful. Examples of metrics it tracks include:
* body weight
* resting heart rate
* daily workout duration
* strength over time
* workout-specific information (e.g. steps taken during a walk, elevation gain, etc.)

### Setup
To start developing on this project, you'll need to first run the setup script:
```
./scripts/setup.sh
```

### Add a Workout
Adding a workout is done via the `add-workout.sh` script:
```
./scripts/add-workout.sh DD-MMM-YYYY
# (e.g. ./scripts/add-workout.sh 01-JAN-2023)
```

### Running Tests
Tests should automatically run as a pre-commit hook that gets setup as part of the `setup.sh` script but if you want to run them manually, you can use the `run-test.sh` script.
```
./scripts/run-tests.sh
```
