libname temp "/rpscan/u071439";

proc format;
value $selectcpt
10001-99200='yes'
other='no';

proc sql;

create table temp.trash1 as
select
PROC1,
PROCMOD,
count(PROCMOD) as count
from
MDCD2015.medicaid_o_2015_v2
(where=(
FACPROF='P' and
PAY>0       and
missing(ENROLID)+missing(SVCDATE)+missing(PROC1)=0 and
PROCTYP='1' and put(PROC1,$selectcpt.)='yes'))
group by PROC1, PROCMOD;

proc export
data = temp.trash1
outfile="/rpscan/u071439/trash1.csv"
replace;
run;


