const { spawn } = require("child_process");
const imagePath = "../my_data/target_1.jpg";
const python = spawn("python", ["preprocess.py", imagePath]);

python.stdout.on("data", (data) => {
	console.log("image: ", data.toString());
});

python.stderr.on("data", (data) => {
	console.error("err: ", data.toString());
});

python.on("error", (error) => {
	console.error("error: ", error.message);
});

python.on("close", (code) => {
	console.log("child process exited with code ", code);
});
