const express = require('express');
const app = express();
app.use(express.json());
var studentList = [
    { id: 1, name: 'A' },
    { id: 2, name: 'B' }
];

app.get("/", (request, result) => {
    result.send("Hello World");
});

app.get("/studentlist", (request, result) => {
    if (!studentList) {
        result.statusCode(404);
        result.statusMessage("No student found");
    } else {
        result.send(studentList);
    }
})

app.post("/studentlist", (request, result) => {
    if (!request.body.name && request.bodey.name == "") {
        result.statusCode(404);
        result.statusMessage("Name not found");
    } else {
        studentList.push({
            id: studentList.length + 1,
            name: request.body.name
        })
        result.send("Success")
    }
})

//Port Variable
const port = process.env.port || 5000
app.listen(port, () => { console.log(`Listening on port ${port}`) })