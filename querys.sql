

drop table DOCENTE_REFERENCIA

-- Create the reference table
create table docente_referencia
as(
	select distinct docente2017.nome_var as novo_nome,docente_tables.desc_var as descricao,docente_tables.nome_var as velho_nome
	from docente2017
	JOIN (
		select docente2007."nome da variável" as nome_var,docente2007."descrição da variável" as desc_var,'docente2007' as table_name,categoria from docente2007 union all
		select docente2008."nome da variável" as nome_var,docente2008."descrição da variável" as desc_var,'docente2008' as table_name,categoria from docente2008 union all
		select docente2009."nome da variável" as nome_var,docente2009."descrição da variável" as desc_var,'docente2009' as table_name,categoria from docente2009 union all
		select docente2010."nome da variável" as nome_var,docente2010."descrição da variável" as desc_var,'docente2010' as table_name,categoria from docente2010 union all
		select docente2011."nome da variável" as nome_var,docente2011."descrição da variável" as desc_var,'docente2011' as table_name,categoria from docente2011 union all
		select docente2012."nome da variável" as nome_var,docente2012."descrição da variável" as desc_var,'docente2012' as table_name,categoria from docente2012 union all
		select docente2013."nome da variável" as nome_var,docente2013."descrição da variável" as desc_var,'docente2013' as table_name,categoria from docente2013 union all
		select docente2014."nome da variável" as nome_var,docente2014."descrição da variável" as desc_var,'docente2014' as table_name,categoria from docente2014 union all
		select docente2015."nome da variável" as nome_var,docente2015."descrição da variável" as desc_var,'docente2015' as table_name,categoria from docente2015 union all
		select docente2016."nome da variável" as nome_var,docente2016."descrição da variável" as desc_var,'docente2016' as table_name,categoria from docente2016
	) as docente_tables
	ON LOWER(docente_tables.desc_var) = LOWER(docente2017.desc_var) and docente2017.nome_var != docente_tables.nome_var
)
drop table docentes_nf
-- Find the values that aren't in the reference
create table docentes_nf
as (
	select distinct nome_var as nome_var,desc_var as desc_var
	from (
		select docente2007."nome da variável" as nome_var,docente2007."descrição da variável" as desc_var,'docente2007' as table_name,categoria from docente2007 union all
		select docente2008."nome da variável" as nome_var,docente2008."descrição da variável" as desc_var,'docente2008' as table_name,categoria from docente2008 union all
		select docente2009."nome da variável" as nome_var,docente2009."descrição da variável" as desc_var,'docente2009' as table_name,categoria from docente2009 union all
		select docente2010."nome da variável" as nome_var,docente2010."descrição da variável" as desc_var,'docente2010' as table_name,categoria from docente2010 union all
		select docente2011."nome da variável" as nome_var,docente2011."descrição da variável" as desc_var,'docente2011' as table_name,categoria from docente2011 union all
		select docente2012."nome da variável" as nome_var,docente2012."descrição da variável" as desc_var,'docente2012' as table_name,categoria from docente2012 union all
		select docente2013."nome da variável" as nome_var,docente2013."descrição da variável" as desc_var,'docente2013' as table_name,categoria from docente2013 union all
		select docente2014."nome da variável" as nome_var,docente2014."descrição da variável" as desc_var,'docente2014' as table_name,categoria from docente2014 union all
		select docente2015."nome da variável" as nome_var,docente2015."descrição da variável" as desc_var,'docente2015' as table_name,categoria from docente2015 union all
		select docente2016."nome da variável" as nome_var,docente2016."descrição da variável" as desc_var,'docente2016' as table_name,categoria from docente2016
	) as docente_tables
	where docente_tables.nome_var not in 
	(
	 	select velho_nome
	 	from docente_referencia
	 	union all
	 	select novo_nome
		from docente_referencia
		union all
		select nome_var
		from docente2017
	)
)

alter table docentes_nf add column novo_nome varchar(800)
update docentes_nf
set novo_nome = docente2017.nome_var 
from docente2017
where replace(lower(docentes_nf.desc_var),'superior completo','superior') = lower(docente2017.desc_var)

update docentes_nf
set novo_nome = docente2017.nome_var 
from docente2017
where replace(lower(docentes_nf.desc_var),'formação/complementação pedagógica do curso superior','formação/complementação pedagógica do curso') = lower(docente2017.desc_var)


update docentes_nf
set novo_nome = docente2017.nome_var 
from docente2017
where replace(lower(docentes_nf.desc_var),'código do distrito da escola','código completo do distrito da escola') = lower(docente2017.desc_var)

update docentes_nf
set novo_nome = docente2017.nome_var 
from docente2017
where replace(lower(docentes_nf.desc_var),'código da turma','código único da turma') = lower(docente2017.desc_var)
update docentes_nf
set novo_nome = docente2017.nome_var 
from docente2017
where replace(lower(docentes_nf.desc_var),'escolaridade superior completo com e sem licenciatura','escolaridade superior') = lower(docente2017.desc_var)


update docentes_nf
set novo_nome = docente2017.nome_var 
from docente2017
where replace(replace(lower(docentes_nf.desc_var),' ',''),'-','') =replace(replace(lower(docente2017.desc_var),' ',''),'-','')

update docentes_nf
set novo_nome = docente2017.nome_var
from docente2017
where replace(docentes_nf.nome_var,'ID_','IN_') = docente2017.nome_var 

update docentes_nf
set novo_nome = docente2017.nome_var
where nome_var = 'ID_DIDATICA_METODOLOGIA'


select distinct *  
from docentes_nf
where novo_nome is null and not lower(desc_var) like '%nome%'
order by nome_var




select distinct nome_var as nome_var,desc_var as desc_var, table_name,categoria
from (
    select docente2007."nome da variável" as nome_var,docente2007."descrição da variável" as desc_var,'docente2007' as table_name,categoria from docente2007 union all
    select docente2008."nome da variável" as nome_var,docente2008."descrição da variável" as desc_var,'docente2008' as table_name,categoria from docente2008 union all    
    select docente2009."nome da variável" as nome_var,docente2009."descrição da variável" as desc_var,'docente2009' as table_name,categoria from docente2009 union all
    select docente2010."nome da variável" as nome_var,docente2010."descrição da variável" as desc_var,'docente2010' as table_name,categoria from docente2010 union all
    select docente2011."nome da variável" as nome_var,docente2011."descrição da variável" as desc_var,'docente2011' as table_name,categoria from docente2011 union all
    select docente2012."nome da variável" as nome_var,docente2012."descrição da variável" as desc_var,'docente2012' as table_name,categoria from docente2012 union all
    select docente2013."nome da variável" as nome_var,docente2013."descrição da variável" as desc_var,'docente2013' as table_name,categoria from docente2013 union all
    select docente2014."nome da variável" as nome_var,docente2014."descrição da variável" as desc_var,'docente2014' as table_name,categoria from docente2014 union all
    select docente2015."nome da variável" as nome_var,docente2015."descrição da variável" as desc_var,'docente2015' as table_name,categoria from docente2015 union all
    select docente2016."nome da variável" as nome_var,docente2016."descrição da variável" as desc_var,'docente2016' as table_name,categoria from docente2016
) as docente_tables
where 