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

// LAB CODE -- inlined into infra/ui/ui.js

// State
var test_cases = {};
var current_test_case = null;

var candidate_names = [
    "Ash", "Brock", "Misty", "May", "Lt. Surge", "Erika", "Koga",
    "Sabrina", "Blaine", "Giovanni", "Lorelei", "Bruno", "Agatha",
    "Lance", "Gary", "Oak", "Elm", "Joy"];
var small_talent_names = [
    "Singing", "Dancing", "Comedy", "Acrobatics", "Magic", "Juggling", "Ventriloquy",
    "Piano", "Dog Tricks", "Miming", "Martial Arts", "Balancing"];
var big_talent_names = [
    "Singing", "Dancing", "Comedy", "Magic", "T4", "T5", 
    "T6", "T7", "T8", "T9", "T10", "T11", "T12", "T13",
    "T14", "T15", "T16", "T17", "T18", "T19", "T20",
    "T21", "T22", "T23", "T24", "T25", "T26", "T27"];
var talent_names = [];
var matrix = [];
var selected_candidates = [];

// UI button handlers
function handle_select(test_case_name) {
  // test case is already loaded in memory; need to switch to it
  $("#current_test").html(test_case_name);
  current_test_case = test_cases[test_case_name]
  matrix = current_test_case["matrix"]
  if (matrix[0].length <= 12) {
    talent_names = small_talent_names
  } else {
    talent_names = big_talent_names
  }
  render_matrix(matrix, []);
}

function handle_solve() {
  // RPC to server.py to run the user's code
  var solve_callback = function( solution ) {
    if (solution[0] != 'ok') {
      $("#lab_message").html("Your code raised an exception.");
        return;
    } else if (solution[1].length == 0) {
      $("#lab_message").html("Your code found no solution.");
    } else {
      $("#lab_message").html("The Talent Show is formed!");
    }

    // Render the solution
    render_matrix(current_test_case["matrix"], solution[1]);
  };
  invoke_rpc("/run_test", current_test_case, 5000, solve_callback);
}

// Initialization code (called when the UI is loaded)
var initialized = false;
function init() {
  if (initialized) return;
  initialized = true;
    
  /*
  // If using this, should add the following script to config.json:
  //   "https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS_HTML
  // and configure it as below:
  //
  // Init Latex rendering here
  MathJax.Hub.Config({
     TeX: {
       extensions: ["color.js"],
       Macros: {
         RR: '{\\bf R}',
         bold: ['{\\bf #1}', 1]
       }
     }
  });
  */
    
  // Load list of test cases
  var test_case_names_callback = function( test_cases_names ) {
    for (var i in test_cases_names) {
      var filename = test_cases_names[i];
      if (!(filename.match(/.*?[.]in/i))) continue;

      var test_case_callback = function( test_case ) {
        var first = Object.keys(test_cases).length == 0;
        var test_case_name = test_case.test;
        test_cases[test_case_name] = test_case;

        $("#test_cases").append(
          "<li class=\"mdl-menu__item\" onclick=\"handle_select('" +
          test_case_name +
          "')\">" +
          test_case_name +
          "</li>");

        // is it first? select it!
        if (first) handle_select(test_case.test);
      };
      invoke_rpc("/load_json", { "path": "cases/"+filename }, 0, test_case_callback);
    };
  };
  invoke_rpc("/ls", { "path": "cases/" }, 0, test_case_names_callback);
}
    
function render_matrix(matrix, solution) {
  selected_candidates = solution;
  var html = render_matrix_to_html(matrix);
  //$("#inner_matrix").text(html);
  $("#inner_matrix").html(html);
}

function render_matrix_to_html(matrix) {
  var html = '<table border="1">';
  var num_cols = 0;
  var num_rows = matrix.length;
  if (num_rows > 0) {
    num_cols = matrix[0].length;
  }
  else {
    num_cols = 0;
  }
  var r, c, i;
  for (r = 0; r < num_rows; r++) {
      if (r == 0) {
	  // add header row
	  html = html + '<tr>'
	  for (i = 0; i < num_cols; i++) {
	      if (i == 0) {
		  html = html + '<th>';
	      }
	      html = html + '<th>' + talent_names[i];
	  }
	  html = html 
      }

      html = html + '<tr>'
      // first column is candidate_name
      if (selected_candidates.indexOf(r) > -1) {
	  html = html + '<td bgcolor="yellow">';
      } else {
	  html = html + '<td>';
      }
      html = html + candidate_names[r];

      // rest of columns
      for (c = 0; c < num_cols; c++) {
	  if (selected_candidates.indexOf(r) > -1 && matrix[r][c] == 1) {
	      html = html + '<td bgcolor="yellow">X';
	  } else if (matrix[r][c] == 1) {
	      html = html + '<td>X';
	  } else {
	      html = html + '<td>';
	  }
      }
  }
  html = html + '</table>'
  return html;
}


/* OLD LATEX TABLE VERSION -- no longer used.


function render_matrix_mathjax(matrix, solution) {
  //var ans = JSON.stringify(solution);  // DEBUG (uncomment this div in index.html to use)
  //$("#solution_text").html(ans);
  selected_candidates = solution;

  var html = render_matrix_to_mathjax(matrix);
  $("#inner_matrix").html(html);
  MathJax.Hub.Queue(["Typeset",MathJax.Hub,"inner_matrix"]);
}

function render_matrix_to_mathjax(matrix) {
  var html = '\\(\\require{color}\\)';
  var num_cols = 0;
  var num_rows = matrix.length;
  if (num_rows > 0) {
    num_cols = matrix[0].length;
  }
  else {
    num_cols = 0;
  }
  var r, c, i;
  for (r = 0; r < num_rows; r++) {
    if (r == 0) {
      html = html + '\\begin{equation}\\begin{array}{|c|';
      for (i = 0; i < num_cols; i++) {
         html = html + 'c|';
      }
      html = html + '}';
      html = html + '\\hline ';
      for (i = 0; i < num_cols; i++) {
        html = html + '& \\text{' + talent_names[i] + '}';
      }
      html = html + '\\\\\\hline ';
    }
    if (selected_candidates.indexOf(r) > -1) {
      html = html + '\\colorbox{yellow}{' + candidate_names[r] + '}';
    } else {
      html = html + '\\text{' + candidate_names[r] + '}';
    }

    for (c = 0; c < num_cols; c++) {
      html = html + '&';
      if (selected_candidates.indexOf(r) > -1 && matrix[r][c] == 1){
        html = html + '\\colorbox{yellow}{$\\checkmark$}';
      } else if (matrix[r][c] == 1){
        html = html + '\\checkmark ';
      }
    }

    if (r == num_rows -1) {
      html = html + '\\\\\\hline \\end{array}\\end{equation} ';
    }
    else {
      html = html + '\\\\\\hline ';
    }
  }
  return html;
}


*/

