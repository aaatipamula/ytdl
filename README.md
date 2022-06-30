# YouTube Downloader Project

Backend API, and Interface bot for Discord

## Project Info

**Author**: Aniketh Aatipamula <br>
**Project Start Date**: , 2022 <br>
**Contributors**: N/A <br> <br>

**Project Origin**: This project originated as a way to allow people to download YouTube videos without having to use a sketchy website. I combined that individual project with previous projects on Discord bots and this project was born.<br> <br> 

**Project Description**: This project aims to provide a way for people to download the audio from YouTube videos. Through the use of the Discord API for Bots for client interfacing and express.js for serving up the files this project downloads audio and hosts it for 24 hours to serve up to the user.<br>

This repo is split into two parts. The contents of the `./discord_bot/` folder containe all the code needed to interface with the application. Currently the only interface for the application is through the messaging service Discord. By using the *download* command one can provide a url for a youtube video and a format they would like to download the audio in which will then download the audio and provide a link to the API for file download as the average file size of the download exceeceds discords limitations on file size.<br>

The second part of this project is the API. Due to size limitations on Discord file uploads a simple Javascript API was made using express.js. It only returns files if a valid request code is put into the url otherwise it will return a 404. 

## Project Notes

**Python Dependencies**: This project requires that a handful of non-standard Python modules be installed. <br>
This includes:
- discord.py
- yt_dlp 

<br>

**Node Dependencies**: This project requires that a handful of non-standard Node modules be installed. <br>
This includes:
- express
- sqlite3