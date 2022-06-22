const express = require('express')
const router = express.Router()
const fs = require('fs')

router.get("/", (req, res) =>{
    res.send(403)
})

router.route("/:fileid").get(
    (req, res) => {

        let fileid = req.params.fileid

        fs.access(`downloads/audio/${fileid}.mp3`, fs.constants.F_OK, (err) => {

            if (err) {
                res.sendStatus(404)

            }else{
                res.download(`downloads/audio/${fileid}.mp3`, `${Buffer.from(fileid, 'base64').toString()}.mp3`)

            }
        });
    }
)

module.exports = router