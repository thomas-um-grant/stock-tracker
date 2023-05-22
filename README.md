# <Stock Tracker>
 
 ![chart](chart.png)
 ![chart](stats.png)

## Description

I started this project as part of an interview, might actually continue on once graded!
This is a stock tracker, it tracks stocks using the Polygon API, I selected 3 stocks for version 1 (APPL, MSFT, TSLA).

I learned Vuejs(html / css / javascript) to develop my front end and Flask with python to develop my backend.
I also used Heroku to deploy it on a docker image.

## Table of Contents
- [Usage](#usage)
- [Next](#next)
- [Credits](#credits)

## Usage

You can check it out on: https://stock-tracker-for-alquant.herokuapp.com/
 
Run Flask backend separately for development:
  - in /server: flask run --port=5001 --debug
  
Run Vue frontend separately for development:
  - in /client: npm run dev
  
Run a Docker image locally:
  - docker build -t web:latest .
  - docker run -d --name stock-tracker-for-alquant -e "PORT=8765" -p 8007:8765 web:latest
  - docker stop stock-tracker-for-alquant
  - docker rm stock-tracker-for-alquant

## Next

Once graded, the plan is to move on with V2 version:
- Dynamically adding stocks
- Enabling period picker
- Working on the site robustness
- Building a real SQL DB to reduce API calls

## Credits

Thank you to a bunch of youtubers for getting me up to speed with front end tools,
especially @ChartJS-tutorials and @NetNinja, I might have underestimated the challenges frontend devs experience haha!
