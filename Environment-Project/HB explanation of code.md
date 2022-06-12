## Explanation of my code for the team

## login_sign_up.py
User_logged_in = ‘id’ in session
All of the routes to the webpages include a user_logged_in variable which checks if there is data
in ‘session’ (a flask extension for temporarily saving user data) and returns this data if it’s 
present. Along with an ‘if’ statement on each html template using  Jinja Template Language 
(explained further under /login) this means that for each page a ‘login’ button is displayed if the 
user is logged in and a ‘logout’ button if they’re logged out.  

### Connect to db
In the file ‘connect to db’ I’ve imported mysql/connector. The function _connect_to_db uses 
mysql.connect to establish and return the connection to the database using the host name, root 
password and database name. The host name and password are stored here to link to MySQL. 
The _connect_to_db function takes the database name as parameter and uses this to connect 
to a particular database.
Both the ‘login_sign_up.py’ and ‘pollution_and_weather_links.py’ files use the database 
connector to link to the database ‘user_login_details.sql’ - passing the name of this database in 
as a parameter to establish the connection.

## Login_sign_up.py
In this file are the functions for creating an account for and signing into MeteoMapper. 

### /login
The ‘/login’ route gets the email and password from the login form. 
Verifies this by hashing the password and then passing the email and hashed password into the
the email_password_exists function and if this function returns None it means that the password
and email could not be verified and the user is prompted to try again or login using the sign up 
page - using flashed messages which is included in flask. These messages appear conditionally
on the login page - only when the email and password are incorrect this is achieved through use
of Jinja Template Language inside the double curly brackets in the html template. Jinja allows 
the evaluation of an expression, variable or function call and its integration into an html 
template. This means in the login.html template - these messages could be displayed using an if
condition which checks if they’re being run in the python script. 

If the email_password_exists function returns values other than None this means the email and 
password have been verified.  The email_password_exists function will return a two item list 
from the database of users. The first item is set as the session id and the second item is the 
user’s name and allocated to a separate variable. The user is then redirected to the ‘logged_in’ 
page where a welcome message is flashed, along with their name.

Session is a flask extension which has been imported into the files containing routes to different 
pages of the website. It is a piece of data, unique to the user which is stored on their server. In 
this case ’ id’ has been chosen as the unique identifier. It means that when the person is logged 
in and the ‘session’ is created - for as long as they are on the website, even though they click on
different pages, the website will know that they are logged in. It means that through verifying the
session, pages can display certain options or retrieve certain data using the id. It is temporary 
and is encrypted to prevent people from  copying the id and gaining access to information and 
pages they shouldn’t.

### /logged_in
The ‘logged_in route verifies whether there is any data allocated to ‘session’. If there is it 
extracts this from session and uses this ‘id’ (which is also the primary key on the parent user 
table in MySQL and used to link user information to child tables). The ‘id ‘ is used to query the 
searches table in MySQL using the ‘return_user_searches’ function which takes id as a 
parameter - uses this to query the MySQL searches table and return the searches for that 
particular user’. This is then stored within the variable info and returned by logged_in function. 
The ‘logged_in’ template is then retrieved and the ‘if statement’ embedded in the html iterates 
over the results of the searches and displays them for the user using the Jinja Template 
Language. 
If there is no data for ‘session’ and the user attempts to use the logged_in url to navigate to the 
page, the user is redirected to the ‘login’ page with an invitation to login. 

### /logout
Removes the information / data from ’session’ and redirects the user to the login page.

### def email_password_exists
This function takes an email and password as its parameters. It connects with the 
user_login_info database using the _connect_to_database function and uses the cursor to 
query the database using the email to retrieve the id, name and password stored against the 
email address. It then iterates over the result  using a ‘for loop’ using the indexes of the different
returned tuple to extract the id, name and password and assign them to separate variables. If no
id number is returned, the function returns None. Otherwise it then checks the database 
password (which is saved in hashed form for security) against the password passed to the 
function using Bcrypt().check_password_hash(,) which takes a password hash and a password 
as its parameters and checks them against each other. If the two don’t match it returns None. If 
they do match, it appends the id number and the name which can then be used by the login 
route and function. 

### /sign_up
If a post request is made the sign_up function retrieves the sign up information from the form on
the sign_up page. It uses the check_email() function which takes email as a parameter, to 
check where the email address exists already. If the check_email function doesn’t return None 
then the user is alerted that the email exist using flashed messages. The user also gets a 
message if the email or name length are too short, the password is too short or the two 
passwords don’t match. If all the required criteria are satisfy then the account is created - 
meaning that the name, password and email are passed as parameters to the 
insert_user_into_db() function where the password is hashed and then they are all inserted 
into the  user_account table/

### insert_user_into_db(name, password, email) 
This function takes name, password and email as parameters. It hashes the password being 
passed to it as a parameter, for security so the actual password is not inserted into the 
database. It uses the _connect_to_db() function to connect to the user_login_details database 
and then creates a cursor and uses it to query the database using cursor.execute. The query is 
an insert statement which inserts the name, password and email taken as parameters, into the 
user_account table. It then commits this using cursor.commit
check_email(email)

### This function takes email as a parameter. It uses the _connect_to_db() function to connect to 
the user_login_details database and then creates a cursor and uses it to query the database 
using cursor.execute to  select an id number using the email passed as a parameter. Using the 
cursor, it then assigns the result to a variable ‘id_num’ and returns this variable. If there is no 
email, this variable will remain as ‘none’ if there is, a number will have been returned and 
assigned to this variable. 

## Pollution and Weather 

### /Weather
SAMANTA’S API CALLS 

### /save_search
City is set as a global variable within the call to the weather api, in the /weather route. This 
means that when the .get request retrieves the name of the city typed into the search bar and 
assigns it to the city variable, it is globally available and can be used in the /save_search route. 
The save search route is linked to save search the link in the /weather html page. It checks 
whether the user is logged in using ‘session’, calls the insert_city_into_db() function to insert 
the current city into the relevant table in the database and returns a message informing the user
that that the city has been saved. If the person is not logged in it returns a message inviting 
them to login.

### insert_city_into_db(id, chosencity)
Takes an id and city name as parameters. Uses the _connect_to_db() function to open a 
cursor and query the user_login_details database. It inserts the city name and id into 
saved_searches within this database table by calling the stored procedure  InsertCity()  and 
passing in the city name and id as parameters. Commits this information and closes the cursor 
and connection. 

### return_user_searches(id)
Takes an id number as a parameter, Uses the _connect_to_db() function to open a cursor and 
query the saved_searches table in the user_login_details database. The query selects any 
City names stored against the specified id number. A ‘for loop’ extracts this information and 
appends it to a list. The cursor and connection are closed and the information is returned by the 
function. 

### def delete_user_searches(City, id):
Takes an id and city name as parameters. Uses the _connect_to_db() function to open a 
cursor and query the user_login_details database. It deletes the city name and id from 
saved_searches within this database,  using a delete statement and passing in the city name 
and id as parameters. Commits this information and closes the cursor and connection. 

### /<string:item>
This route is linked to the saved search items listed on the logged in page. It is a dynamic url 
(explained under /delete/<string:item>) which essentially means that the name of the item (city) 
can be passed to the url. This is then passed to the search(item) function and assigned to the 
variable cit (city). A call to the open weather api is made using the city name and an api key. 
The information from the api is stored in ‘data’ and returned by the function, to  be accessed by 
the and the data is displayed by the logged_in page which is rendered by the function and the if 
statement using the Jinja Template Language on the page. If the call to the api fails then a 
message is flashed saying that the city information cannot be displayed and the logged in page 
is rendered. 

### /delete/<string:item>
This route is linked to the delete link which appears next to any saved searches on the 
‘logged_in’ page. It’s a dynamic url which means it can generate a custom route depending on 
what information is passed into it at the time the link is clicked. In this case the ‘item’ string - 
which corresponds to the city name displayed beside the delete button, is passed into the url. 
This ‘item’ is then taken from the url by being passed from the route in the back end, to the 
delete function and then assigned to the variable, mycity. The session ‘id’ is also assigned to a 
variable. These can then be passed into the delete_user_searches(city, id) as parameters 
allowing it to select these records from the database and delete them. The updated list is then 
returned using the return_user_searches(id) function, the logged_in html page is rendered 
and the data is displayed by the if statement using the Jinja Template Language on the page.  

### /User_Log
This route is linked to the ‘Go to Log Page’ link on the logged_in page. It assigns the session 
(id) to a variable. It uses the _connect_to_db() function to open a cursor and query the 
user_login_details database - specifically the table containing the logged searches for the 
user. It does this by passing in the session id into the name of the table in the query. It then 
iterates over the results of the query and returns this in the ‘info’ variable, to be iterated over by 
the Jinja Template Language on the “User_Log” html template which is rendered and returned 
by the function. It closes the connection to the database and closes the cursor. 

### /Log_Result/<string:result>
This route is linked to the ‘Log Result’ hyperlink on the ‘logged_in’ page, which appears when 
the search results for a saved search are displayed on the page.  - using Jinja to create an if 
statement that wraps around the link. It uses a dynamic url to capture the city name from data in
the saved search and pass this into a url. This is then passed to the log_result function, 
assigned to a variable and used in a Try clause in a call to the api. The session (id) is also 
assigned to a variable. The results of the api call are also assigned to variables. The function 
then checks if a table for this user already exists using the check_table_exists function, 
passing in the session id as a parameter. It creates a table if one does not already exist not, 
using the creste_weather_table() function and passing in the session id as a parameter. It then
inserts the id and the variables assigned to the results of the api call, in to the 
insert_into_weather_table() function as parameters. These parameters correspond to columns
on the table into which the data is to be inserted. If the table exists (the function returns a value 
other than None), then only the insert_into_weather_table function is called. Then the function
redirects the user to the logged_in page. If there is an error whilst executing this function, an 
except clause catches this and returns a message to the user explaining that a result was 
unable to be logged and the user is redirected to the logged_in page.

### check_table_exists(id):
Takes an id number as a parameter. Within a ‘try’ clause, uses the _connect_to_db() function 
to open a cursor and query any weather table which contains this id in its name. Any data 
retrieved is extracted from the cursor using a list comprehension and then assigned to a ‘table’ 
variable which is returned by the function. The cursor and connection are closed. If the table 
does not exist, then this query fails and is caught by the except form which assigns ‘table’ the 
value of ‘None’ and returns ‘’table’. 

### create_weather_table(id)
Takes an id number as a parameter.Uses the _connect_to_db() function to open a cursor and 
execute a stored procedure called CreateWeatherLog() which is explained in more detail in the
database section but which creates a unique table using the id passed into the function as a 
parameter. This change is committed and the cursor and connection are closed.
def insert_into_weather_table(id,Countrycode, cityname, temp, pressure, 
humidity)

Takes id and various weather related data as parameters. Uses the _connect_to_db() function 
to open a cursor and execute a stored procedure called InsertWeatherLog which is explained 
more under database but which takes the same parameters as this .py function and inserts 
them in to a weather table assigned to this particular user, as well as the date and time, so they 
can log the information taken from the weather api. This change is committed and the cursor 
and connection are closed.

### /delete_log/<string:log_index>
This route is linked to the log items displayed on the  user_log.html page. It has a dynamic url, 
into which is passed the unique index number for the log entry. This is then passed into the 
delete_log() function and then assigned to a variable. The session (id) is also assigned to a 
variable within the function. These are then passed to the delete_record() function which takes 
id and index as parameters and uses them to identify and delete the log. When the record is 
deleted a ‘record deleted’ message is flashed
def delete_record(id, index)
Takes an id and index number as parameters. Uses the _connect_to_db() function to open a 
cursor and query the user_login_details database. It deletes the log record from the weather 
table assigned to that user. The query identifies the right table using the id number and the right 
log entry using the unique index which is assigned to each log. It commits this information and 
closes the cursor and connection. 

### /pollution/<string:cityname>/<string:coordinate>
This is linked to the ‘see pollution data’ link in the weather.html page. It is a dynamic url which 
takes the city name and the longitude and latitude from the weather data displayed on the page 
after the call to the api. It then passes these two strings to the pollution() function as variables. 
The city name is assigned to a variable and the coordinates are split on the hyphen and 
extracted from the resulting list using indexes, then assigned to two different variables (‘lon’ and 
‘lat’). In a try clause, these ‘longitude’ and ‘latitude’ variables are used in the call to the open 
weather api that returns pollution as it can’t be searched using city name. The data from the api 
call is extracted and assigned to dictionary called ‘data’ which is then returned by the function, 
along with the city name variable so that they can all be displayed on the pollution.html page 
which is rendered by the function. If the call to the api fails, an except clause displays a 
message to the user explaining that pollution information can’t be displayed. 

## Database

The MySQL file contains the queries for creating the user_login_details database, the 
user_account table and the saved_searches table where the user searches are stored. It also 
queries to create stored procedures for inserting new City entries into the saved_searches 
table and for creating and updating tables for each client where logs of the weather api calls can
be stored.

### Tables

### user_account table
The user_account table contains columns for the id, name, email address and hashed 
passwords of users. The varchar() limitation on the password column is set to 60 characters as 
an error was generated previously when a hashed password was too long to be inserted into the
table. There is a primary key on id so that user information can be linked, using this to other 
tables in the database - using the concept of normalisation - so all information is stored in 
specifically designated tables but still linked together. The primary key is set to auto_increment 
and NOT NULL so that a new id will be generated each time a new user is created. This id is 
also used for the flask ‘session’ in the main app so that the user has a unique identifier to follow 
them as they navigate the website.
Saved_searches table
The saved_searches table contains columns for the id of users and also stores the cities that 
they have searched. This table is then called and displayed by a function in the main app when 
the user logs in. The id column is designated as a foreign key so that searches can be linked 
together by user and can be linked to the id of the user in the user_account.

### Stored Procedures

### InsertCity (Checkid int, InsertCity varchar(25))
This is a stored procedure which takes an id(integer) and city(string) as its parameters first 
checkers whether a city has already been saved by a particular user using a SELECT statement
with the parameters passed in as id and City respectively, counts any entries and assigns this to
a variable. If the variable is 0 then a record with these two values doesn’t exist and is inserted 
into the database with the use of an INSERT statement. A stored procedure makes it easier to 
replicate this process exactly and minimises the amount of SQL that needs to be written in the 
function in the .py file as it can be called and parameters passed in from a python function into 
the SQL query written inside this function.

### CreateWeatherLog(Checkid int)
This is a stored procedure which takes an id number as an argument. It then uses this to create 
named weather_ + the id number. This means that when somebody wants to create a log for 
the data from a particular city, their id number can be passed into this stored procedure and a 
unique table generated which can then be called by a function in a .py document in the project 
file and displayed for the user when they go to their log page. The table has a column for the id 
of the user which is then assigned as a Foreign Key. There are also columns to record the 
weather information received by the api in the main file including country code, city, 
temperature, pressure and humidity. There is also a column to store the date and time of the 
entry and an index for the entry in the table to make it possible to identify the record when the 
delete function is called in the .py file. The way that MySQL works - the id number can’t be 
passed as the name of the table unless the query is broken up into individual parts and then 
concatenated. Otherwise the table is literally named ‘checkid’ after the variable. This is why the 
‘create table’ query is written in individual parts, then concatenated, then prepared, then 
executed within the procedure. 

### InsertWeatherLog(Checkid int, CountryCode varchar(4), CityName varchar(25), 
Temperature decimal, press int, humidity int)
The InsertWeatherLog procedure takes a number of different parameters which correspond to 
the information taken when a call is made to the weather api - namely the country code, name 
of city, temperature, pressure and humidity and also the id number of the user to be inserted 
into this column. These are then passed into an insert statement which adds them to the table 
which corresponds to the user. The table is selected using the id number which is passed in as 
the first variable to the stored procedure and then into the part of the insert table procedure 
which specifies the table. Again the id number can’t be passed as the name of the table unless 
the query is broken up into individual parts, therefore the ‘create table’ query is written in 
individual parts then, concatenated, prepared and executed within the procedure. Within the 
procedure the now() function is called automatically in the datetime column and the ‘indx’ 
column automatically increments, in order to log the date and time of the insertion of the 
information into the table and create a unique value for that particular row of data. 

### I've also added the unittests to the unittest file
