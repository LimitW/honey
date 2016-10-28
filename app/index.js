//express

var express = require('express');
var bodyParser = require('body-parser');
var app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "X-Requested-With");
    res.header('Access-Control-Allow-Methods', 'GET, POST, DELETE');
    next();
});
process.on('uncaughtException', function (err) {
  console.log(err);
  console.log(err.stack);
});

var mysql = require('mysql');

var pool = mysql.createPool({
    host : 'localhost',
    user : 'root',
    password : 'root',
    port: '3306',
    database: 'honey'
});

app.get('/index', function(req, res){
    res.set({'Content-Type': 'text/json','Encodeing': 'utf8'});
    pool.getConnection(function(err, connection){
        if(err){
            console.log('[connect] - ' + err);
            res.send({"status": -1});
            return;
        }
        connection.query('select type, description, part, province, url, date_format(dt, "%Y-%m-%d") as dt from current where status = 0',
          function(err, rows){
            if(err){
                console.log('[query] - ' + err);
                res.send({"status": -1});
                return;
            }
            connection.release();
            var list = [];
            for(var i = 0; i < rows.length; ++i){
                list.push({
                  "type": rows[i].type,
                  "description": rows[i].description,
                  "part": rows[i].part,
                  "province": rows[i].province,
                  "url": rows[i].url,
                  "dt": rows[i].dt
                });
            }
            console.log('[query] - init success');
            res.send({"status": 0, "list": list});
        });
      });
});

app.post('/submit', function(req, res){
  res.set({'Content-Type': 'text/json','Encodeing': 'utf8'});
  var ls = req.body.targets, that = this;
  console.log(typeof(ls));
  var cnt = 0, len = ls.length;
  for(var i = 0; i < ls.length; ++i){
    (function(i){
      var cur_url = ls[i];
      pool.getConnection(function(err, connection){
        if(err){
            console.log('[connect] - ' + err);
            res.send({"status": -1});
            return;
        }
        connection.query('update current set status = 1 where url = "' + cur_url + '"', function(err, rows){
            if(err){
                console.log('[query] - ' + err);
                res.send({"status": -1});
                return;
            }
            connection.release();
            cnt++;
            if(cnt === len){
              console.log('[query] - submit success');
              res.send({"status": 0});
            }
        });
      });
    })(i);
  }
});

app.post('/history', function(req, res){
    res.set({'Content-Type': 'text/json','Encodeing': 'utf8'});
    pool.getConnection(function(err, connection){
        if(err){
            console.log('[connect] - ' + err);
            res.send({"status": -1});
            return;
        }
        dt = req.body.date;
        connection.query('select select type, description, part, province, url, date_format(dt, "%Y-%m-%d") as dt from current where dt = ?' , dt,  function(err, rows){
            if(err){
                console.log('[query] - ' + err);
                res.send({"status": -1});
                return;
            }
            connection.release();
            var list = [];
            for(var i = 0; i < rows.length; ++i){
                list.push({
                  "type": rows[i].type,
                  "description": rows[i].description,
                  "part": rows[i].part,
                  "province": rows[i].province,
                  "url": rows[i].url,
                  "dt": rows[i].dt
                });
            }
            console.log('[query] - get history success');
            res.send({"status": 0, "list": list});
        });
    });
});

//run app
app.listen(3000, function(){
    console.log('honey back-end is running..');
});
