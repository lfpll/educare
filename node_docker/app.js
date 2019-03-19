const Koa = require('koa')
const JSONStream = require('streaming-json-stringify');
const sql = require('sql-query').Query();
const Router = require('koa-router');
const app = new Koa()
const router = new Router();

//app.context.db = db();

router.get('/docentes', (ctx, next) => {

	// SQL query creator
	let sqlSelect = sql.select();
	querySql = sqlSelect.from('docentes')

  let limit = 100
  const params = ctx.query

  // Fields selected on the query
  if ('fields' in params)
  {
		let select = params['fields']
		querySql = querySql.select(select.split(','))
	  delete params['fields']
  }

  // Changing the limit
 	if ('limit' in params)
  {

  	limit = parseInt(params['limit'])
  	if (limit > 100) limit =100
  	delete params['limit']
  }
    // Generate a query for the SQL
  querySql = querySql.where(params).limit(limit).build()
});

app.use(router.routes()).use(router.allowedMethods());
app.listen(3000);