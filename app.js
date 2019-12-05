var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var MongoClient = require('mongodb').MongoClient;

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'jade');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);
const cp = require("child_process");
// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

MongoClient.connect(url,function(err,client){

	var command = "curl -X GET --header 'Accept: application/json' --header 'Authorization: key ttn-account-v2.AXVZUWtEus1MMpVF8qGf8a7jQEbkU4sUA9sM3WsGkDI' 'https://bus_gps_data.data.thethingsnetwork.org/api/v2/query?last=7d'";

	var db = "onibus_gps_data_db";

	if(err) throw err;

	cp.exec(command,function(err,stdout,stderr){

		if(err){

			console.log("error");

		}else{

			var data = JSON.parse(stdout);

			client.db(db).collection('ttn-data').insertMany(data,{},function(err,result){

				if(err != null){

					console.log("Erro na inserção de documentos");
					console.log(err.message);

				}else{

					console.log(result.insertedCount," documentos inseridos com sucesso!");

				}

			});

		}

	});



});

module.exports = app;
