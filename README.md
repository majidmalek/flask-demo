# Flask on Heroku

This project is intended to help you tie together some important concepts and
technologies from the 12-day course, including Git, Flask, JSON, Pandas,
Requests, Heroku, and Bokeh for visualization.

The repository contains a basic Python/Flask web application that works on Heroku.

A [finished example](http://di-flask-demo.herokuapp.com/) demonstrates some basic functionality.

## Steps to deploy
- Git clone the existing repository.
- Create Heroku application with `heroku create <app_name>` or leave blank to
  auto-generate a name.
- heroku config:add BUILDPACK_URL=https://github.com/kennethreitz/conda-buildpack.git
- heroku config:add QUANDL_API_KEY='your Quandl API key'
- Deploy to Heroku: `git push heroku master`
- You should be able to see your site at `https://<app_name>.herokuapp.com`
