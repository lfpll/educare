const rewire = require("rewire"),
	app  = rewire("./app");


test("Testing replacer of columns", ()=>
{
	const queryMultipleColumns = app.__get__("queryMultipleColumns")
	refOne = {"a":1};
	refTwo = {"a":1,"b":2};
	fieldOne = "a"
	fieldTwo = ["b","a"]

	const res_one = queryMultipleColumns(fieldOne,refOne)
	const res_two = queryMultipleColumns(fieldTwo,refTwo)
	expect(res_one).toEqual({"1":1})
	expect(res_two).toEqual({"2":1,"1":1})
})

// test("Testing query generator", () =>
// {
// 	jsonQueryOne = {'de':1}
// 	jsonQueryOne = {'limit':1}
// })

test("Testing function that replace keys of query", () =>
{
	const replaceObjectKeys = app.__get__("replaceObjectKeys")
	test_object = {'defic':1,'raca':2}
	repl_keys = {'defic':'deficiencia','raca':'TP_RACA','nada':'nada'}
	const res_objct = replaceObjectKeys(test_object,repl_keys)
	expect(res_objct).toEqual({'deficiencia':1,'TP_RACA':2})
})