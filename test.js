const sqlite3 = require('sqlite3');

const query = (req_id) => {

    let db = new sqlite3.Database('./database/db.sqlite', sqlite3.OPEN_READONLY, (err) => {

        if (err && err.code == "SQLITE_CANTOPEN") {
            console.log("Error: " + err)
            exit(2)

        } else if (err) {   
            console.log("Error: " + err)
            exit(2);
        }
    });

    return new Promise((resolve, reject) => {
        db.each(`SELECT * FROM videoids WHERE date = '${req_id}'`, (err, row) => {

            if (err) {
                reject(err)
            } else {
                resolve(row)
            }

        });

        db.close()
    
    })

}

query()
    .then(result => { console.log(result) })
    .catch(err => console.log(err))