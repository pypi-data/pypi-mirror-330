const path = require("path");

module.exports = {
    mode: "development",
    entry: {
        forms: ["./src/css/style.css", "./src/js/formFunctions.js",],
    },
    output: {
        filename: "[name].bundle.js",
        path: path.resolve(__dirname, "../dist"),
        library: "fv",
        libraryTarget: "umd",
        globalObject: "this",
    },
    module: {
        rules: [
            {
                test: /\.css/i,
                use: ["style-loader", "css-loader"],
            },
        ],
    },
}