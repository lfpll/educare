const Koa = require('koa')
const JSONStream = require('streaming-json-stringify');
const sql = require('sql-query').Query();
const Router = require('koa-router');
const app = new Koa()
const router = new Router();
	
//app.context.db = db();
const numSearch = (num_sum,fields)  =>{}
router.get('/docentes', (ctx, next) => {

	// SQL query creator
const create_query = function (params,table)
{
	let sqlSelect = sql.select();
	let querySql = sqlSelect.from('docentes')
	let limit = 100
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
  return querySql.where(params).limit(limit).build()
}
//app.context.db = db();
router.get('/docentes', (ctx, next) => {


	// SQL query creator
  const params = ctx.query

  // Generate a query for the SQL
 	let thisSql =  create_query(params,table='docentes')
 	console.log(thisSql)
});

app.use(router.routes()).use(router.allowedMethods());
app.listen(3000);
