const queryBigQuery =  (query_string) =>
{

    // [START bigquery_query]
    // Import the Google Cloud client library
    const {BigQuery} = require('@google-cloud/bigquery');
  
    async function query(query_string) {
      // Queries the Shakespeare dataset with the cache disabled.
        console.log(query_string)
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

queryBigQuery('select nu_ano_censo from `educare-226818.CENSO.Docente_2017` limit 10').then((rows) => console.log(rows))