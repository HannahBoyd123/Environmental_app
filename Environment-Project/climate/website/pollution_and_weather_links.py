from flask import render_template, request, redirect, url_for, session, flash, abort, Blueprint
import json
import requests
import urllib.request
from connect_to_db import _connect_to_db

pollution_and_weather_links = Blueprint('pollution_and_weather_links', __name__)

pollution_and_weather_links.secret_key = 'Kettle123!'

def tocelcius(temp):
    return str(round(float(temp) - 273.16, 2))

city = 'London'

@pollution_and_weather_links.route('/weather', methods=['POST', 'GET'])
def weather():
    user_logged_in = 'id' in session
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    if request.method == 'POST':
        global city
        city = request.form['city']
    else:
        city = 'london'

    try:
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid=' + api_key).read()
    except:
        flash('please enter valid city name')
        data = None
        return render_template('weather.html', data=data)

    list_of_data = json.loads(source)

    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + '_' + str(list_of_data['coord']['lat']),
        "temp": str(list_of_data['main']['temp']) + 'k',
        "temp_cel": tocelcius(list_of_data['main']['temp']) + 'C',
        "pressure": str(list_of_data['main']['pressure']),
        "humidity": str(list_of_data['main']['humidity']),
        "cityname": str(city),
    }
    return data and render_template('weather.html', data=data, user_logged_in=user_logged_in)

#save the current weather search to the user's profile
@pollution_and_weather_links.route("/save_search", methods=['POST', 'GET'])
def save_search():
    if 'id' in session:
        sessionid = session['id']
        mycity = city
        insert_city_into_db(sessionid, mycity)
        flash(f'{city} saved to profile')
        return redirect(url_for('pollution_and_weather_links.weather'))
    else:
        flash('please login to save searches')
    return redirect(url_for('pollution_and_weather_links.weather'))


#inserts city into database
def insert_city_into_db(id, chosencity):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("call InsertCity(%s, %s)", (id, chosencity))
    connected.commit()
    cursor.close()
    connected.close()


#returns a list of the user's saved searches, saved in the database - called by the /logged_in route
def return_user_searches(id):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("SELECT City FROM saved_searches WHERE id = %s ", (id,))
    info = [City[0] for City in cursor]
    cursor.close()
    connected.close()
    return info



#saves the weather information for the saved searches on the logged in page
@pollution_and_weather_links.route("/<string:item>", methods=["GET"])
def search(item):
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    cit = item
    try:
        source = urllib.request.urlopen(
            'http://api.openweathermap.org/data/2.5/weather?q=' + cit + '&appid=' + api_key).read()

        list_of_data = json.loads(source)

        data = {
            "country_code": str(list_of_data['sys']['country']),
            "coordinate": str(list_of_data['coord']['lon']) + '-' + str(list_of_data['coord']['lat']),
            "temp": str(list_of_data['main']['temp']) + 'k',
            "temp_cel": tocelcius(list_of_data['main']['temp']) + 'C',
            "pressure": str(list_of_data['main']['pressure']),
            "humidity": str(list_of_data['main']['humidity']),
            "cityname": str(cit),
        }
        info = return_user_searches(session['id'])

        return render_template('logged_in.html', info=info, data=data)
    except:
        info = None
        data = None
        flash('unable to display search')
        return render_template('logged_in.html', info=info, data=data)

#route for deleting searches from logged in page
@pollution_and_weather_links.route("/delete/<string:item>", methods=["GET", "POST"])
def delete(item):
    if 'id' in session:
        sessionid = session['id']
        mycity = item
        delete_user_searches(mycity, sessionid)
        return_user_searches(sessionid)
        flash(f'{mycity} deleted')
    return redirect(url_for("login_sign_up.logged_in"))

#deletes the specified search from the database using City and id as identifiers
def delete_user_searches(City, id):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("DELETE FROM saved_searches WHERE City = %s and id = %s", (City, id))
    connected.commit()
    cursor.close()
    connected.close()


#link to user log page and connection to database to stored logs
@pollution_and_weather_links.route("/User_Log", methods=["GET", "POST"])
def user_log():
    try:
        sessionid = session['id']
        connected = _connect_to_db('user_login_details')
        cursor = connected.cursor()
        cursor.execute("SELECT * FROM weather_%s order by City", (sessionid,))
        info =[log for log in cursor]
        cursor.close()
        connected.close()
        return render_template("User_Log.html", info=info)
    except: return render_template("User_Log.html")

#city information logging function - call to api stored in log
@pollution_and_weather_links.route("/Log_Result/<string:result>", methods=["GET", "POST"])
def log_result(result):
    api_key = '48a90ac42caa09f90dcaeee4096b9e53'
    cit = result
    sessionid = session['id']
    try:
        source = urllib.request.urlopen(
        'http://api.openweathermap.org/data/2.5/weather?q=' + cit + '&appid=' + api_key).read()

        list_of_data = json.loads(source)

        country_code = list_of_data['sys']['country'],
        temp_cel = tocelcius(list_of_data['main']['temp']),
        pressure = list_of_data['main']['pressure'],
        humidity = list_of_data['main']['humidity'],
        cityname = cit

        if check_table_exists(sessionid) == None:
            create_weather_table(sessionid)
            insert_into_weather_table(sessionid, "".join(country_code), cityname, "".join(temp_cel), pressure[0],
                                      humidity[0])
            return redirect(url_for('login_sign_up.logged_in'))
        else:
            insert_into_weather_table(sessionid, "".join(country_code), cityname, "".join(temp_cel), pressure[0],
                                      humidity[0])
            return redirect(url_for('login_sign_up.logged_in'))
    except:
        flash('unable to log result')
        return redirect(url_for('login_sign_up.logged_in'))

#checks whether a weather logging table already exists for a user based on id
def check_table_exists(id):
    try:
        connected = _connect_to_db('user_login_details')
        cursor = connected.cursor()
        cursor.execute("SELECT * FROM weather_%s", (id,))
        table = [data for data in cursor]
        cursor.close()
        connected.close()
        return table
    except:
        table = None
        return table

#creates a weather table assigned to a user

def create_weather_table(id):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("call CreateWeatherLog(%s)", (id,))
    connected.commit()
    cursor.close()
    connected.close()

#inserts weather api data into table to be called at a later date

def insert_into_weather_table(id,Countrycode, cityname, temp, pressure, humidity):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("call InsertWeatherLog(%s, %s, %s, %s, %s, %s)", (id, Countrycode, cityname, temp, pressure, humidity))
    connected.commit()
    cursor.close()
    connected.close()

#deletes a log fom the weather table usin the log_index which is passed to the url
@pollution_and_weather_links.route("/delete_log/<string:log_index>", methods=["GET", "POST"])
def delete_log(log_index):
    sessionid = session['id']
    indx = log_index
    delete_record(sessionid, indx)
    flash(f'record {indx} deleted')
    return redirect(url_for("pollution_and_weather_links.user_log"))

#function for deleting record fom weather table
def delete_record(id, index):
    connected = _connect_to_db('user_login_details')
    cursor = connected.cursor()
    cursor.execute("DELETE FROM weather_%s WHERE indx = %s", (id, index))
    connected.commit()
    cursor.close()
    connected.close()

#link on weather html page which links to the pollution api - extracts the city name and coordinates, calls the polution api
#and displays this info on pollution page
@pollution_and_weather_links.route('/pollution/<string:cityname>/<string:coordinate>')
def pollution(cityname, coordinate):

    cityname  = cityname
    lonlat = coordinate.split("_")

    try:

        api_key = '48a90ac42caa09f90dcaeee4096b9e53'
        lat = float(lonlat[1])
        lon = float(lonlat[0])

        source = "http://api.openweathermap.org/data/2.5/air_pollution/forecast?lat={}&lon={}&appid={}".format(lat,
                                                                                                               lon,
                                                                                                          api_key)
        response = requests.get(source)

        list_of_pollution = response.json()

        data = {
            "coordinate": str(list_of_pollution['coord']),
            "pollution": str(list_of_pollution["list"][0]['main']),
            "CO": str(list_of_pollution["list"][0]['components']["co"]),
            "PM2_5": str(list_of_pollution["list"][0]['components']["pm2_5"]),
            "PM10": str(list_of_pollution["list"][0]['components']["pm10"])
        }


    except:
        return flash('unable to display pollution data')
    return render_template('pollution.html', data=data, cityname=cityname)