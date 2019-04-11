const parse = require('csv-parse')
const assert = require('assert')
const fs = require('fs')
const sql = require('sql-query').Query();
const output = []

const queryInsert = sql.insert()

const parser = parse({
    delimiter: '|',
    columns: true
  })

// Use the readable stream api
parser.on('readable', function(){
    let record
    while (record = parser.read()) {
        output.push(record)
    }
})
// Catch any error
parser.on('error', function(err){
    console.error(err.message)
  })


fs.createReadStream("./sample.csv")
.on('data', function(data){
    try {
        //perform the operation
        parser.write(data)
    }
    catch(err) {
        //error handler
    }
})
.on('end',function(){
    c
    onsole.log('end')
    console.log(queryInsert.into('table1').set(output).build())
});  

