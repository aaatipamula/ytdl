const express = require('express');
const router = express.Router()
const sqlite3 = require('sqlite3');
const fs = require('fs');
const { exit } = require('process');

router.get("/", (req, res) =>{
    res.send(403)
})

const query = (req_id) => {

    let db = new sqlite3.Database('./database/db.sqlite', sqlite3.OPEN_READONLY, (err) => {

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

router.route("/:reqid").get(
    (req, res) => {

        let reqid = req.params.reqid

        query(reqid)

        .then(response => {

            fs.access(`./downloads/webm/${response.idone}.webm`, fs.constants.F_OK, (err) => {

                if (err) {
                    console.log(err)
                    res.sendStatus(404)
    
                }else{
                    res.download(`./downloads/webm/${response.idone}.webm`, `${Buffer.from(response.idone, 'base64').toString()}.wemb`)
    
                }
            });
        })

        .catch(err => { console.log(err) })


    }
)

module.exports = router