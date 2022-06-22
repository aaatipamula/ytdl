const express = require('express')
const router = express.Router()

router.route("/:fileid").get(
    (req, res) => {
        res.send(`/downloads/audio/${req.params.fileid}`)
    }
)

module.exports = router