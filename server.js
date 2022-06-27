const express = require('express');
const app = express();
const mp3Router = require('./routes/mp3');
const webmRouter = require('./routes/webm')

app.use('/mp3', mp3Router)
app.use('/webm', webmRouter)

router.get("/", (req, res) =>{
    res.send(403)
})

app.listen(8000)