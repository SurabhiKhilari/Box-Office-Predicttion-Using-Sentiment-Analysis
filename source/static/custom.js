$(function() {
  $(".loader__container").hide();
  $("#main-container").hide();
  $("button").click(function() {
    $("#main-container").show();
    $(".card-content").hide();
    form_data = $("form").serialize();
    $(".s003").hide();
    //Start the counter
    var clock = $(".counter").FlipClock({
      // ... your options here
      clockFace: "MinuteCounter"
    });

    //$(".loader__container").show();
    $.ajax({
      url: "/search",
      data: form_data,
      type: "POST",
      success: function(response) {
        //var time = clock.getFaceValue();
        //Stop the counter
        clock.stop();
        console.log("Clock is stopped and time is" + (clock.getTime() - 1));
        showSnackbar(clock.getTime().time);
        //unpack and load data
        $(".loader__container").hide();
        //$(".s003").show();
        showData(".movie-prediction");
        renderPrediction(response.prediction);
        drawchart(response.sentiment_array);
        showData(".wordcloud");
        $("#wordcloud").attr("src", response.wordcloud_image);
        showData(".top-comments");
        for (var key in response.top_comments) {
          let comment_data = response.top_comments[key];
          //console.log(comment_data.text);
          $("#top-comments").append(
            "<li class=" +
              '"list-group-item d-flex justify-content-between align-items-center"><span><img src="/static/assets/youtube_social_circle_red.png" class="youtube-icon"></span>' +
              comment_data.text +
              '<span class="badge badge-primary badge-pill">' +
              comment_data.likes +
              "</span> </li>"
          );
        }
        console.log(response);
      },
      error: function(error) {
        $(".loader__container").hide();
        $(".s003").show();
        console.log(error);
      }
    });

    //Make another call for movie info
    $.ajax({
      url: "/movieinfo",
      data: form_data,
      type: "POST",
      success: function(response) {
        //unpack and load data
        // $(".loader__container").hide();
        // $("#main-container").show();
        showData(".movie-info");
        showData(".poster");
        $("#movie-title").html(response.title);
        $("#movie-summary").html(response.overview);
        $("#poster").attr(
          "src",
          "https://image.tmdb.org/t/p/w500" + response.poster_path
        );
        console.log(response);
      },
      error: function(error) {
        $(".loader__container").hide();
        $(".s003").show();
        console.log(error);
      }
    });

    //Make another call for twitter data
    $.ajax({
      url: "/tweetsearch",
      data: form_data,
      type: "POST",
      success: function(response) {
        //unpack and load data
        $(".loader__container").hide();
        $("#main-container").show();
        //console.log(respose)
        showData(".top-tweets");
        //Add positive tweets
        for (var key in response[1]) {
          let comment_data = response[1][key];
          $("#top-tweets").append(
            "<li class=" +
              '"list-group-item d-flex justify-content-between align-items-center"><span><img src="/static/assets/Twitter_Social_Icon_Circle_Color.png" class="youtube-icon"></span>' +
              comment_data +
              " </li>"
          );
        }
        initMap(response[0]);
        console.log("retrived heatmap data");
        console.log(response);
      },
      error: function(error) {
        $(".loader__container").hide();
        $(".s003").show();
        console.log(error);
      }
    });
  });
});

// Draw Sentiment Chart
function drawchart(chartdata) {
  console.log(chartdata.comment_date);
  labels = [];
  sentiments = [];
  neg_sentiments = [];
  pos_sent_total = 0;
  neg_sent_total = 0;
  for (var key in chartdata.comment_date) {
    //console.log(chartdata.comment_date[key]);
    labels.push(chartdata.comment_date[key]);
  }
  for (var key in chartdata.sentiment) {
    //console.log(chartdata.sentiment[key]);
    pos_sent_total += chartdata.sentiment[key];
    sentiments.push(chartdata.sentiment[key]);
  }
  for (var key in chartdata.neg_sentiment) {
    //console.log(chartdata.sentiment[key]);
    neg_sent_total += chartdata.neg_sentiment[key];
    neg_sentiments.push(chartdata.neg_sentiment[key]);
  }
  //console.log(chartdata.sentiment);
  line_chart_data = {
    labels: labels,
    datasets: [
      {
        data: sentiments,
        label: "Positive Sentiment",
        borderColor: "#3e95cd",
        fill: false
      },
      {
        data: neg_sentiments,
        label: "Negative Sentiment",
        borderColor: "#f44242",
        fill: false
      }
    ]
  };
  pie_chart_data = {
    labels: ["Positive Sentiment", "Negative Sentiment"],
    datasets: [
      {
        data: [pos_sent_total, neg_sent_total],
        label: "Positive Sentiment",
        backgroundColor: ["#3e95cd", "#f44242"],
        fill: false
      }
    ]
  };

  showData(".line-chart");
  showData(".pie-chart");
  //draw the line chart
  new Chart(document.getElementById("line-chart"), {
    type: "line",
    data: line_chart_data,
    options: {
      title: {
        display: true,
        text: "Sentiments over Time"
      }
    }
  });
  //draw the pie chart
  new Chart(document.getElementById("pie-chart"), {
    type: "pie",
    data: pie_chart_data,
    options: {
      title: {
        display: true,
        text: "Sentiments Distribuition"
      }
    }
  });
}

function initMap(heatmap_data) {
  var testData;
  if (
    heatmap_data == undefined ||
    heatmap_data[0] == null ||
    (heatmap_data[0] == null) == undefined
  ) {
    testData = {
      max: 8,
      data: [
        { lat: 24.6408, lng: 46.7728, count: 3 },
        { lat: 50.75, lng: -1.55, count: 5 },
        { lat: 52.6333, lng: 1.75, count: 5 },
        { lat: 48.15, lng: 9.4667, count: 5 },
        { lat: 52.35, lng: 4.9167, count: 5 },
        { lat: 60.8, lng: 11.1, count: 5 },
        { lat: 43.561, lng: -116.214, count: 1 },
        { lat: 35.8278, lng: -78.6421, count: 1 }
      ]
    };
  } else {
    testData = { max: 8, data: heatmap_data };
  }
  console.log("testdata");
  console.log(testData);
  var baseLayer = L.tileLayer(
    "http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      attribution: "Yogesh Prabhukhanolkar",
      maxZoom: 18
    }
  );

  var cfg = {
    // radius should be small ONLY if scaleRadius is true (or small radius is intended)
    radius: 10,
    maxOpacity: 0.8,
    // scales the radius based on map zoom
    scaleRadius: true,
    // if set to false the heatmap uses the global maximum for colorization
    // if activated: uses the data maximum within the current map boundaries
    //   (there will always be a red spot with useLocalExtremas true)
    useLocalExtrema: true,
    // which field name in your data represents the latitude - default "lat"
    latField: "lat",
    // which field name in your data represents the longitude - default "lng"
    lngField: "lng",
    // which field name in your data represents the data value - default "value"
    valueField: "count"
  };

  var heatmapLayer = new HeatmapOverlay(cfg);

  var map = new L.Map("map-container", {
    center: new L.LatLng(25.6586, -80.3568),
    zoom: 4,
    layers: [baseLayer, heatmapLayer]
  });

  heatmapLayer.setData(testData);

  // make accessible for debugging
  layer = heatmapLayer;
}

//css handling functions
function showData(root) {
  let hide_selector = "div" + root + ">.card-loader";
  let show_selector = "div" + root + ">.card-content";
  console.log(hide_selector + " : " + show_selector);
  $(hide_selector).hide();
  $(show_selector).show();
}

function renderPrediction(prediction) {
  let selector = $(".movie-prediction-results");
  $(".movie-prediction").addClass("prediction-" + prediction);
  if (prediction == 1) {
    selector.html("SuperHit");
  } else if (prediction == 2) {
    selector.html("Flop");
  } else if (prediction == 3) {
    selector.html("Semi-Hit");
  } else if (prediction == 4) {
  }
}
//display
function showSnackbar(elapsed_time) {
  // Get the snackbar DIV
  console.log("In snackbar");
  var x = document.getElementById("snackbar");

  // Add the "show" class to DIV
  x.className = "show";
  $("#snackbar").html(
    "We completed the prediction for your movie in:" + elapsed_time + " seconds"
  );

  // After 10 seconds, remove the show class from DIV
  setTimeout(function() {
    x.className = x.className.replace("show", "");
  }, 15000);
}
