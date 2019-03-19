const Koa = require('koa')
const JSONStream = require('streaming-json-stringify');
const sql = require('sql-query').Query();
var Router = require('koa-router');


const app = new Koa()
var router = new Router();

//app.context.db = db();

router.get('/docentes', (ctx, next) => {

	// SQL query creator
	let sqlSelect = sql.select();
	querySql = sqlSelect.from('docentes')

  let limit = 100
  const params = ctx.query

  
  if ('fields' in params)
  {
  		select = params['fields']
  		querySql = querySql.select(select.split(','))

  		delete params['fields']
  }
  if ('limit' in params)
  {
  	limit = params['limit']

  	delete params['limit']
  }
  // Generate a query for the SQL
 	querySql = querySql.where(params).limit(limit).build()
  console.log(querySql)
});

app.use(router.routes()).use(router.allowedMethods());
app.listen(3000);