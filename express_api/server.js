const express = require('express');
const app = express();
const sqlite3 = require('sqlite3');
const fs = require('fs');
const { exit, execArgv } = require('process');

app.get("/", (req, res) =>{
    res.send(403)
})

const query = (req_id) => {

    let db = new sqlite3.Database('../database/db.sqlite', sqlite3.OPEN_READONLY, (err) => {

        if (err && err.code == "SQLITE_CANTOPEN") {
            console.log("Error: " + err)
            exit(1)

        } else if (err) {   
            console.log("Error: " + err)
            exit(2);
        }
    });

    return new Promise((resolve, reject) => {
        db.each(`SELECT * FROM ids WHERE reqids = '${req_id}'`, (err, row) => {

            if (err) {
                reject(err)
            } else {
                resolve(row)
            }
        });

        db.close()
    })
}

app.route("/:reqid").get(
    (req, res) => {

        let reqid = req.params.reqid

        query(reqid)

        .then(response => {
            
            const content_id = response.idone.split('$')

            fs.access(`../downloads/${content_id[1]}/${content_id[0]}.${content_id[1]}`, fs.constants.F_OK, (err) => {

                if (err) {
                    console.log(err)
                    res.sendStatus(404)
    
                }else{
                    res.download(`../downloads/${content_id[1]}/${content_id[0]}.${content_id[1]}`, `${Buffer.from(response.idone, 'base64').toString()}.${content_id[1]}`)
    
                }
            });
        })
    
        .catch(err => { console.log(err) })
    }
)

app.listen(8000, () => {
    console.log('Application running...')
});