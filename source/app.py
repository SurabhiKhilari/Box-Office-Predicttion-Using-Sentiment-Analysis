from flask import Flask, render_template, url_for, request, json, jsonify
from youtube_api import write_video_data
from prediction import predict
from moviedb import search_movie
from twitter_api import generate_heatmap_data
app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')


@app.route('/search', methods=['POST'])
def process_query():
    movie = request.form['searchterm']
    write_video_data(movie)
    prediction = predict()
    data = prediction[1].to_json(orient='columns')
    top_comments = prediction[3].to_json(orient='records')
    heatmap_data = []
    return jsonify({'status': 'OK', 'search': movie, 'prediction': prediction[0], 'sentiment_array': json.loads(data), 'wordcloud_image': prediction[2], 'top_comments': json.loads(top_comments), 'heatmap_data': heatmap_data})


@app.route('/movieinfo', methods=['POST'])
def get_movie_info():
    movie = request.form['searchterm']
    print("Movie name is: "+movie)
    movie_info = search_movie(movie)
    return jsonify(movie_info)


@app.route('/tweetsearch', methods=['POST'])
def searchTwitter():
    movie = request.form['searchterm']
    twitter_data = generate_heatmap_data(movie)
    #twitter_data = [[], []]
    return jsonify(twitter_data)


if __name__ == '__main__':
    app.run(debug=True)
