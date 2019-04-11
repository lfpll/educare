var rewire = require("rewire");
var app  = rewire("./app");
const sql = require('sql-query').Query();


test("Testing replacer of columns", ()=>
{
	const queryMultipleColumns = app.__get__("queryMultipleColumns")
	refOne = {"a":1};
	refTwo = {"a":1,"b":2};
	fieldOne = "a";
	fieldTwo = ["b","a"];

	const respOne = queryMultipleColumns(fieldOne,refOne);
	const respTwo = queryMultipleColumns(fieldTwo,refTwo);
	expect(respOne).toEqual({"1":1});
	expect(respTwo).toEqual({"2":1,"1":1});
})


// This is the testing of the function that builds the query 
// 1 - One case of each
// 	1.1 - Test multiple lower case and upper case
//  1.2 - Remenber the types o each 
// 2 - Multiple cases of eacj
// 3 - Special querys, like using limit 
// 4 - Multitple random cases
test("Testing build SQL query",() =>
{	
	const createSelectQuery = app.__get__("createSelectQuery");
	const sexoAmostra  = {'SEXO':['M','F']};
	const defaultParameters = ['TP_SEXO','TP_COR_RACA','TP_ESCOLARIDADE']
	const deficAmostra = { 'Defic': [ 'ce', 'bv' ]};
	const esclAmostra  = {'escolaridade':['FI','FC','SC']};
	// const racaAmostra  = {'raca':['PO','AO']};
	const limit ={'limit':67};
	const fieldsAmostra = {'fields':['raca','escolaridade']};

	
	const table = 'docentes'
	const respSexo = {'TP_SEXO':[1,2]};
	const respDefic = {'IN_CEGUEIRA':1,'IN_BAIXA_VISAO':1};
	const respEscl = {'TP_ESCOLARIDADE':[1,2,4]};
	// const respoRaca = {'TP_COR_RACA':[2,4]};
	const respFields = ['TP_COR_RACA','TP_ESCOLARIDADE']

	
	const sqlDefic = sql.select().from(table).select(defaultParameters).where(respDefic).limit(67).build();
	const queryDefic = createSelectQuery({...deficAmostra,...limit},'docentes')
	expect(sqlDefic).toEqual(queryDefic);

	const sqlSexo = sql.select().from(table).select(defaultParameters).where(respSexo).limit(100).build();
	const querySexo = createSelectQuery(sexoAmostra,'docentes')
	expect(sqlSexo).toEqual(querySexo)

	const sqlSexoUnq = sql.select().from(table).select(defaultParameters).where(respEscl).limit(100).build();
	const querySexoUnq = createSelectQuery(esclAmostra,'docentes')
	expect(sqlSexoUnq).toEqual(querySexoUnq)

	const sqlSexoEsclDefic = sql.select().from(table).select(defaultParameters).where({...{'IN_CEGUEIRA':1},...respEscl,...respSexo}).limit(100).build();
	const querySexoEsclDefic = createSelectQuery({...{'defic':'CE'},...esclAmostra,...sexoAmostra},'docentes')
	expect(sqlSexoEsclDefic).toEqual(querySexoEsclDefic)

	const sqlWithFields = sql.select().from(table).select(respFields).where({...{'IN_CEGUEIRA':1},...respEscl,...respSexo}).limit(100).build();
	const queryWithFields = createSelectQuery({...fieldsAmostra,...{'defic':'CE'},...esclAmostra,...sexoAmostra},'docentes')
	expect(sqlWithFields).toEqual(queryWithFields)
})