const danfo = dfd
const tf = danfo.tensorflow

// Constants
const base_data_path = "https://raw.githubusercontent.com/ericlefort/exerciselog/main/data"

function readCSV(path, variableName) {
  return new Promise((resolve, reject) => {
    dfd.readCSV(path)
      .then(df => { resolve(df); })
      .catch(e => { reject(e); });
  });
}

(async function() {
    // Load data
    const health_metrics = await readCSV(`${base_data_path}/health_metrics.csv`)
    const cardio_workouts = await readCSV(`${base_data_path}/cardio_workouts.csv`)
    const weight_training_workouts = await readCSV(`${base_data_path}/weight_training_workouts.csv`)
    const weight_training_sets = await readCSV(`${base_data_path}/weight_training_sets.csv`)
    const travel_days = await readCSV(`${base_data_path}/travel_days.csv`)

    console.log(Object.getOwnPropertyNames(health_metrics));
    health_metrics.tail().print()
})();
