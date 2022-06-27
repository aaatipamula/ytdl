const express = require('express');
const app = express();
const audioRouter = require('./routes/audio');

app.use('/audio', audioRouter)

app.listen(8000)