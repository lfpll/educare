const Koa = require('koa');
const Router = require('koa-router');
const app = new Koa();
const router = new Router();
const sql = require('sql-query').Query();
const envVars = require('./envs');
const {BigQuery} = require('@google-cloud/bigquery');

//app.context.db = db();

// Replace values on a list based on a object
const replaceVals = (fields,realObjVal)  =>{
  // Return the real value on SQL
  if (Array.isArray(fields))
  {
    return fields.map((key) => realObjVal[key.toLowerCase()]);
  }
  return realObjVal[fields];
}

// Transform fields passed to the column name queries on SQL
// Like meat,chicken,vegan
// Returns {chicken_food:1,cow_meat:1,vegan_food:1}
const queryMultipleColumns =(fields,envRelatObj) =>{ 
  let queryObj = {};

  // Check if it a single value
  if (!Array.isArray(fields))
  {
    const field = envRelatObj[fields.toLowerCase()];
    queryObj[field] = 1;
  }
  else
  {
  const columnReals = replaceVals(fields,envRelatObj);
  queryObj = columnReals.reduce((queryObj,value) => 
    {
      queryObj[value] = 1;
      return queryObj;
    },{})
  }
  return queryObj;
}

// SQL query creator from api querystring object
const createSelectQuery =  (params,table) =>
{ 
  const referenceColumns = envVars['realNameColumns']
  // Transforming query params to lower case
  const lowerParams = Object.keys(params).reduce((dest, key) => {
  dest[key.toLowerCase()] = params[key]
  return dest
  }, {});
  // Creating the SQL query generator
  let querySql;

  // Fields that will selected by the sql query
  let fields 
  if (typeof(lowerParams['fields']) == 'undefined' || lowerParams['fields'].length >10)
  {
    fields = ['sexo','raca','escolaridade']
  }
  else if ('fields' in lowerParams)
  {
    if (Array.isArray(lowerParams['fields'])){
      fields = lowerParams['fields'].map((val) => val.toLowerCase()); 
    }
    else{
      fields = lowerParams['fields'].toLowerCase()
    }

    delete lowerParams['fields'];
  }
  const select = replaceVals(fields,referenceColumns);
  querySql = sql.select().from(table).select(select);

  // Changing the limit of the SQL query
  let limit = 100;
  if ('limit' in lowerParams)
  {
    if (parseInt(lowerParams['limit']) < 100) limit = parseInt(lowerParams['limit']);
    delete lowerParams['limit'];
  }
  
  // Transform parameters of deficiencys into booleans that can relate on the SQL table
  // TODO implement a beter way if transParams
  let transfParams = lowerParams
  if ('defic' in lowerParams)
  {
    const deficSearch = queryMultipleColumns(lowerParams['defic'],envVars['defic']);
    delete lowerParams['defic'];
    transfParams = {...deficSearch,...lowerParams};
  } 
  // Replace the values on the query string for ones that are related to the SQL table  
  transfParams = Object.keys(transfParams)
  .reduce((destination, key) => {
    if (key in referenceColumns)
    {
      destination[referenceColumns[key]] = replaceVals(transfParams[key],envVars[key]);
    }
    else{
      destination[key] = transfParams[key]
    }
    return destination;
  }, {});

  // TODO Fix this if with undefined, kind of ugly
  // Returns the data as a SQL query if there is a deficiency or not
  return querySql.where(transfParams).limit(limit).build();
}
const queryBigQuery =  (query_string) =>
{

    // [START bigquery_query]
    // Import the Google Cloud client library
    const {BigQuery} = require('@google-cloud/bigquery');
  
    async function query(query_string) {
      // Queries the Shakespeare dataset with the cache disabled.
      // Create a client
      const bigqueryClient = new BigQuery();
  
      const options = {
        query: query_string,
        // Location must match that of the dataset(s) referenced in the query.
        location: 'US',
      };
  
      // Run the query as a job
      const [job] = await bigqueryClient.createQueryJob(options);
      console.log(`Job ${job.id} started.`);
  
      // Wait for the query to finish
      const [rows] = await job.getQueryResults();
  
      // Print the results
      return rows;
    }
    return query(query_string);
}
//app.context.db = db();
router.get('/docentes', async (ctx,next) => {

  const params = ctx.query

  // Array with the params that are wrongly used in the querystring
  const incorrectVals = Object.keys(params).filter((queryVal) => 
  {
    return (envVars.validInput.indexOf(queryVal.toLowerCase()) <= -1)
  })
  
  // Check if there are values not listed on the querystring
  if (incorrectVals.length  == 0)
  {    
    const query =  async (query_string) => {
      const bigqueryClient = new BigQuery();
  
      const options = {
        query: query_string,
        location: 'US',
      };
  
      // Run the query as a job
      const [job] = await bigqueryClient.createQueryJob(options);  
      // Wait for the query to finish
      const [rows] = await job.getQueryResults();
      // Print the results
      return rows;
    }
    const thisSql =  createSelectQuery(params,'educare-226818.CENSO.Docente_2017')
    const response = await queryBigQuery(thisSql)
    ctx.body = response
  }
  else
  {
    ctx.body = incorrectVals.join(', ') + "can't be used on search"
  }
});

app.use(router.routes()).use(router.allowedMethods());
const PORT = process.env.PORT || 8080;
app.listen(PORT)