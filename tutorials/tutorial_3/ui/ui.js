"use strict";

// RPC wrapper
function invoke_rpc(method, args, timeout, on_done){
  $("#crash").hide();
  $("#timeout").hide();
  $("#rpc_spinner").show();
  //send RPC with whatever data is appropriate. Display an error message on crash or timeout
  var xhr = new XMLHttpRequest();
  xhr.open("POST", method, true);
  xhr.setRequestHeader('Content-Type','application/json; charset=UTF-8');
  xhr.timeout = timeout;
  xhr.send(JSON.stringify(args));
  xhr.ontimeout = function () {
    $("#timeout").show();
    $("#rpc_spinner").hide();
    $("#crash").hide();
  };
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      $("#rpc_spinner").hide();
      var result = JSON.parse(xhr.responseText)
      $("#timeout").hide();
      if (typeof(on_done) != "undefined"){
        on_done(result);
      }
    } else {
      $("#crash").show();
    }
  }
}

// Resource load wrapper
function load_resource(name, on_done) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", name, true);
  xhr.onloadend = function() {
    if (xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      on_done(result);
    }
  }
  xhr.send();
}

// Code that runs first
$(document).ready(function(){
    // race condition if init() does RPC on function not yet registered by restart()!
    //restart();
    //init();
    invoke_rpc( "/restart", {}, 0, function() { init(); } )
});

function restart(){
  invoke_rpc( "/restart", {} )
}

//  LAB CODE

// LAB CODE
// this is inlined into infra/ui/ui.js

var likes = null;
var dislikes = null;
var current_song = null;
var music = [];

function handle_like_button(){
  //$("#lab_message").html("handle_like_button..."); // debug
  like(current_song);
  $("#next").show();
  $("#like").hide();
  $("#dislike").hide();
  //show next
}

function handle_next_button(){
  //$("#lab_message").html("handle_next_button..."); // debug
  //get next recommendation
  play_next_recommended();
}

function handle_dislike_button(){
  //$("#lab_message").html("handle_dislike_button..."); // debug
  dislike(current_song);
  //get next recommendation
  play_next_recommended();
}

function play(song_id){
  current_song = song_id;
  //$("#lab_message").html("play song_id "+song_id+" url: "+music[song_id].url); // debug
  document.getElementById("metadata").innerHTML = music[song_id].title;
  player.loadVideoById({videoId: music[song_id].url});

  $("#next").hide();
  $("#like").show();
  $("#dislike").show();
}

function play_next_recommended(){
  var args = { "likes":    likes,
               "dislikes": dislikes };
  invoke_rpc("/next", args, 0, play);
}

function load_song_metadata(do_after){
 //fetch JSON data structure mapping IDs to song titles.
  $.getJSON("/resources/music.json", function(music_set) {
    music = music_set;
    do_after();
  });
}

function like(song_id){
  //add to like set
  likes.push(song_id);
}

function dislike(song_id){
  //add to dislike set
  dislikes.push(song_id);
}

function init(){
  var tag = document.createElement('script');
  tag.src = "https://www.youtube.com/iframe_api";
  var firstScriptTag = document.getElementsByTagName('script')[0];
  firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
}

var player;
function onYouTubeIframeAPIReady() {
  player = new YT.Player('player', {
    height: '300',
    width: '24',
    loop: 'true',
    videoId: 'M7lc1UVf-VE',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

function onPlayerReady(event) {
  load_song_metadata(function(){
    likes = [];
    dislikes = [];
    play(0);
  });

  event.target.playVideo();
}

var done = false;
function onPlayerStateChange(event) {
  if (event.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideo, 6000);
    done = true;
  }
}


