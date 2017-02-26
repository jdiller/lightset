# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for, jsonify
import logging
import json
import redis
import time
import datetime

app = Flask(__name__)
app.debug = True
r = redis.StrictRedis(host='localhost', port=6379, db=0)
logging.basicConfig(level=logging.DEBUG)
REDIS_KEY = 'manual_color'

@app.route("/")
def home():
    current_color = dict_to_color(r.hgetall(REDIS_KEY)) or 'FFFFFF'
    return render_template('index.html', current_color=current_color)


@app.route("/set", methods=['POST'])
def set():
    logging.debug(request.form)
    color = color_to_dict(request.form['color'])
    duration = int(request.form['duration'])
    r.hmset(REDIS_KEY, color)
    r.expire(REDIS_KEY, duration)
    return redirect(url_for('home'))

@app.route("/current")
def current():
    color = r.hgetall(REDIS_KEY)
    return jsonify(hex_color_dict_to_decimal(color))

def dict_to_color(colordict):
    if colordict is None or colordict == {}:
        return None
    return "{}{}{}".format(colordict['red'], colordict['green'], colordict['blue'])

def color_to_dict(colorstring):
    colorstring = colorstring.strip()
    if colorstring[0] == '#': colorstring = colorstring[1:]
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:]
    return {'red':r, 'green':g, 'blue': b}

def hex_color_dict_to_decimal(colordict):
    if colordict is None or colordict == {}:
        return {}
    r,g,b = (int(colordict['red'], 16),
             int(colordict['green'], 16),
             int(colordict['blue'], 16))

    return {'red':r, 'green':g, 'blue': b}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=9000)
