module.exports =
{
	// Name of the columns referenced on bigtable
	'realNameColumns':
	{
		'sexo':'TP_SEXO',
		'raca':'TP_COR_RACA',
		'escolaridade':'TP_ESCOLARIDADE',
		'cod':'CO_PESSOA_FISICA'
	},
	'validInput':['defic','sexo','escolaridade','raca','fields','limit'],
	'defic': {
		'ce':'IN_CEGUEIRA', // Cego
		'bv':'IN_BAIXA_VISAO', // Baixa Visão
		'su':'IN_SURDEZ', // Surdo
		'da':'IN_DEF_AUDITIVA', // Deficiencia auditiva
		'sc':'IN_SURDOCEGUEIRA',
		'fi':'IN_DEF_FISICA', // Deficiencia Fisisca
		'in':'IN_DEF_INTELECTUAL',
		'dm':'IN_DEF_MULTIPLA',
	},
	'sexo': {
		'm':'1',
		'f':'2'
	},
	'escolaridade':
	{
		'fi':1, // Fundamental incompleto
		'fc':2, // Fundamental Completo
		'ec':3, // Ensino médio completo
		'sc':4	// Superior Completo	
	},
	'raca':
	{
		'no':0, // Nao Declarado
		'bo':1, // Branco
		'po':2, // Preto
		'pa':3, // Pardo
		'ao':4, // Amarelo
		'ia':5  // Indigena
	}
}