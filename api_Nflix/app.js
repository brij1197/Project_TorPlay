const WebTorrent = require('webtorrent');
const express = require('express');
const app = express();
const fs = require('fs');
const op_sys = require('os');
const { win32 } = require('path');
app.use(express.json());
var exec = require('child_process').exec,
    child;

var localpath = "";

app.get("/torrent_file", (request, result) => {
    var magnet = request.body.magnet;
    const client = new WebTorrent();
    var file = []
    client.add(magnet, function(torrent) {
        localpath = torrent.path;

        torrent.files.forEach(element => {
            console.log(element.name);
            file.push({
                filename: element.name,
                filesize: element.length
            })
        });

        result.send(file);

        torrent.destroy(function() {
            console.log("Torrent destroyed");
        });

        client.destroy(function() {
            console.log("Client Destroyed");
            if (op_sys.platform == 'win32') {
                exec('rmdir /S /Q ' + localpath,
                    function(error, stdout, stderr) {
                        if (error !== null) {
                            console.log('exec error: ' + error);
                        }
                    });
            } else if (op_sys.platform == 'linux') {
                exec('rm -F ' + localpath,
                    function(error, stdout, stderr) {
                        if (error !== null) {
                            console.log('exec error: ' + error);
                        }
                    });
            }

        });
    })
})

//Port Variable
const port = process.env.port || 5000
app.listen(port, () => { console.log(`Listening on port ${port}`) })