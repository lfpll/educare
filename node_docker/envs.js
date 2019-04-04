module.exports =
{
	// Name of the columns referenced on bigtable
	'name_columns':
	{
		'sexo':'TP_SEXO',
		'raca':'TP_COR_RACA',
		'escolaridade':'TP_ESCOLARIDADE'

	},
	'vals_correct':['defic','sexo','escolaridade','raca'],
	'defic': {
		'CE':'IN_CEGUEIRA',
		'BV':'IN_BAIXA_VISAO',
		'SU':'IN_SURDEZ',
		'DA':'IN_DEF_AUDITIVA',
		'SC':'IN_SURDOCEGUEIRA',
		'FI':'IN_DEF_FISICA',
		'IN':'IN_DEF_INTELECTUAL',
		'DM':'IN_DEF_MULTIPLA',
	},
	'sexo': {
		'M':1,
		'F':2
	},
	'escolaridade':
	{
		'FI':1,
		'FC':2,
		'EC':3,
		'SC':4		
	},
	'raca':
	{
		'ND':0,
		'BA':1,
		'PR':2,
		'PA':3,
		'AM':4,
		'IN':5
	}
}