const { PythonShell } = require("python-shell");

const imagePath = "../my_data/target_1.jpg";

let options = {
	args: [imagePath],
};

PythonShell.run("preprocess.py", options).then((results) => {
	console.log(results[0]);
});
