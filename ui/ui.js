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

// this is inlined into infra/ui/ui.js

var images = {};

function set_filter(filter) {
  $("#filter").html(filter);
}

function set_image(image_name) {
  $("#image_name").html(image_name);
}

function add_image(image_name, image) {
  if (image_name in images){
    return;
  }

  images[image_name] = image;

  // Add option to select this image
  $("#img_select_options").append($("<li class=\"mdl-menu__item\" onclick=\"set_image('" + image_name + "')\">" + image_name+ "</li>"));

  // Render a canvas
  var canvas = $("<canvas>");
  var canvas_obj = canvas[0];
  var ctx = canvas_obj.getContext("2d");
  ctx.canvas.width = image.width;
  ctx.canvas.height = image.height;
  var image_data = ctx.createImageData(image.width, image.height);

  for (var i=0; i<(image.height*image.width); i++) {
    if (image.pixels[i] > 255 | image.pixels[i] < 0){
      image_data.data[0+i*4] = 255;
      image_data.data[1+i*4] = 0;
      image_data.data[2+i*4] = 0;
    } else {
      image_data.data[0+i*4] = image.pixels[i];
      image_data.data[1+i*4] = image.pixels[i];
      image_data.data[2+i*4] = image.pixels[i];
    }
    image_data.data[3+i*4] = 255;
  }
  ctx.putImageData(image_data,0,0);

  var image_dom = $("<div></div>");
  image_dom.append($("<p>" + image_name + "</p>"));
  image_dom.append(canvas);
  image_dom.append($("<hr>"));
  $("#images").append(image_dom);
}

function apply_filter(filter_name, image_name) {
  var applied_filter = function( image ){
    var new_name = filter_name+ "(" + image_name + ")";
    add_image(new_name, image );
    set_image(new_name);
  };
  invoke_rpc("/apply_filter", { "filter": filter_name, "image": images[image_name] }, 10000, applied_filter);
}

/*
  When the page is loaded, fetch the list of
 filters implemented by lab.py

  Also fetch the list of all
  images (resources/images/*.json) available.
*/
function init(){
  // enumerate filters
  var list_filters = function( filters ) {
    for (var i in filters) {
      var filter = filters[i];
      $("#filters").append($("<li class=\"mdl-menu__item\" onclick=\"set_filter('" + filter + "')\">" + filter + "</li>"));
    }
    set_filter(filters[0]);
  };
  invoke_rpc("/list_filters", {}, 0, list_filters);

  // enumerate images
  var list_images = function( image_names ) {
    for (var i in image_names) {
      var image_filename = image_names[i];
      if (!(image_filename.match(/.*?[.]json/i))){
        continue;
      }
      var image_name = image_filename.slice(0, -5);

      var load_image = (function (name){
        return function( image ){
          add_image( name, image );
          set_image( name );
        }
      })(image_name);
      invoke_rpc("/load_json", { "path": "resources/images/"+image_filename }, 0, load_image);
    }
  };
  invoke_rpc("/ls", { "path": "resources/images/" }, 0, list_images);
}



