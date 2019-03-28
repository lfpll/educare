
const rewire = require("rewire"),
	app  = rewire("./app");
test("Testing replacer of columns", ()=>
{
	const queryMultipleColumns = app.__get__("queryMultipleColumns")
	test_one = {"a":1};
	test_two = {"a":1,"b":2};
	field_one = "a"
	field_two = ["b","a"]

	const res_one = queryMultipleColumns(field_one,test_one)
	const res_two =queryMultipleColumns(field_two,test_two)
	expect(res_one).toEqual({"1":1})
	expect(res_two).toEqual({"2":1,"1":1})
})
