const Koa = require('koa')
const JSONStream = require('streaming-json-stringify');
const sql = require('sql-query').Query();
const Router = require('koa-router');
const app = new Koa()
const router = new Router();
const envVars = require('./envs')
	
//app.context.db = db();

// Substitute the value through the really one used on the database
const realCols = (fields,realObjVal)  =>{
  // Return the real value on SQL
  if (Array.isArray(fields))
  {
    return fields.map((key) => realObjVal[key])
  }
  return realObjVal[fields]
}

// Transform fields passed to the column name queries on SQL
// Like meat,chicken,vegan
// Returns {chicken_food:1,cow_meat:1,vegan_food:1}
const queryMultipleColumns = (fields,envRelatObj) =>
{ 
  let queryObj = {}
  if (!Array.isArray(fields))
  {
    const field = envRelatObj[fields]
    queryObj[field] = 1
  }
  else
  {
  const columnReals = realCols(fields,envRelatObj);
  queryObj = columnReals.reduce((queryObj,value) => 
    {
      queryObj[value] = 1;
      return queryObj;
    },{})
  }
  return queryObj
}

// SQL query creator from api querystring object
const createQuery = function (params,table)
{ 
  // Transforming params to key with lower case
  // TODO fix bug where query deletes same keys with different case
  const lowerParams = Object.keys(params)
  .reduce((destination, key) => {
    destination[key.toLowerCase()] = params[key];
    return destination;
  }, {});

  // Creating the SQL query generator
  let sqlSelect = sql.select();
  let querySql = sqlSelect.from(table)

  // Fields that will selected
  if ('fields' in lowerParams)
  {
    let select = lowerParams['fields']
    querySql = querySql.select(select.split(','))
    delete lowerParams['fields']
  }

  // Changing the limit of the SQL query
  let limit = 100
  if ('limit' in lowerParams)
  {
    if (parseInt(lowerParams['limit']) < 100) limit = parseInt(lowerParams['limit'])
    delete lowerParams['limit']
  }

  // Transform parameters of deficiencys
  let transf_params = lowerParams
  if ('defic' in lowerParams)
  {
    const deficSearch = queryMultipleColumns(lowerParams['defic'],envVars['defic'])
    delete lowerParams['defic']
    transf_params = {...lowerParams,...deficSearch}
  } 



  return querySql.where(transf_params).limit(limit).build()
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
