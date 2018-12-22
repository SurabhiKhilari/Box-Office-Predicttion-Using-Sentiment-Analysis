# Box-Office-Predicttion-Using-Sentiment-Analysis
Sentiment analysis on YouTube, Twitter, and TheMovieDB.

The application will:
●	perform sentiment analysis on upcoming movies using the YouTube comments on their trailers.
●	map the locations of the users tweeting about the movie trailer.
●	show the movie’s poster and its plot.
With correspondence to the user’s movie input, we will 
●	render visualizations 
●	predict how the movie will perform on the Box-Office.
Once user enters a movie title, our application will search the movie’s trailer and extract its streaming comments from YouTube, feeding them to our trained machine learning model for performing sentiment analysis and Box-Office prediction in real-time.
In parallel, it will also grab tweets about the movie trailer and create a heat map showing the tweet locations.
At the same time, we call the ThemovieDB API which uses its own database and  show the movie’s poster and its plot on our UI.

Run-Time Instructions
pip installs:
Install all dependencies needed by the application.
Go to root of directory and using terminal/cmd run command
pip install -r requirements.txt 
		       2)   Depending on the network, it may take some time to download all dependencies.
API account creations:
At first we need to create online accounts needed to grab the data from various sources.
Youtube Data API https://developers.google.com/youtube/v3/getting-started  -- (Free)
Twitter API https://twitter.com/login?redirect_after_login=https%3A%2F%2Fdeveloper.twitter.com%2Fen%2Fapply --(Free)
TheMovieDB API 
First sign up and then use following link to get API key (Free)
https://developers.themoviedb.org/3/getting-started/introduction (Free)
Opencage API 
Once, signed up, we are provided with api_key
https://opencagedata.com/api 
API Keys and their files:
1) Youtube Data API 
Follow instructions from Appendix A and create OAuth credentials.
These are not needed to be copied in config.py file as they reside in separate file.
                             2) Twitter API
                                  After signing up locate and copy the credentials consumer key, consumer secret,access token key,access token secret into appropriate placeholders in config.py
		3) MovieDB API key  
                                  Paste the api key in placeholder of config.py
                             4) Opencage API key
                                  Paste the api key in placeholder of config.py
      4.  Starting the webapp.
                             1) After all above steps are completed , open terminal/cmd in root folder of the app.
                             2) run command python app.py 
                             3) While running the app for the first time, google OAuth flow needs to be completed. A google sign in page will open where you should sign in with google account from which the project is created. A page with message ‘Authentication flow completed’ will be shown.
                             4) This is one time activity as long as newly generated Oauth credentials are stored on the system
                            5) In the browser address bar enter localhost:5000 , and app’s home page will appear.
                            6) For any subsequent web app usages, just use command python app.py in root directory.
                            7) Make sure the app is not already running before starting it. If it is, you will need to manually kill that process using commands like:
                                 ps -ef | grep python                                       and after locating pid of app.py process,
                                 kill -SIGKILL pid

	
	
    5.  Laptop Specifications needed:
                Laptop with RAM greater than equal to 8 GB is preferred due to execution time.
    6. Softwares needed:
               Any IDE such as VS Studio code will make running the app a pleasing experience.
Appendix

A. Creating Oauth Credentials for Youtube API:
After creating google console project, go to project dashboard.
From the left bar , select API credentials 
Click on Create credentials -> Oauth Client ID
Select Application type as web application
In the “Authorized Javascript Origins” list under Restrictions section, add following URLs separately :  http://localhost:8888 , http://localhost:8080
Add above two urls under “Authorized Redirect URIs” too
Click on crate.
Press Ok on OAuth Client screen
You will now see your credentials generated under OAuth 2.0 client IDs of credentials page.
Click on credential and download json
Copy the json to Project root directory (on the same level as app.py) and rename it to client_secrets.json
Now go to OAuth consent screen tab
Enter name of application as Box Office Prediction,enter mail and save it.

