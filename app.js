var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const cp = require("child_process");
var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', function(req,res,next) {

  var data;
  var command = "cat data/output20191212_SF9-copia.txt";
  console.log(command);

    cp.exec(command,function(err,stdout,stderr){

      if(err){ 

        console.log('error');

      }else{

        var data = JSON.parse(stdout);

        var reducedData = new Array();

        for(var i = 0; i < data.length; i++){

            data[i].payload_raw = new Buffer(JSON.parse(JSON.stringify(data[i].payload_raw)),'base64').toString('ascii');

            reducedData.push({device_id:data[i].dev_id, raw:data[i].payload_raw, time:data[i].metadata.time});

        }


      }

      res.render('index', { title: 'Ônibus GPS' , data: JSON.stringify(reducedData) });

    }); 


});

app.listen(3000,function () {
  console.log('Example app listening on port 3000!');
});



module.exports = app;
