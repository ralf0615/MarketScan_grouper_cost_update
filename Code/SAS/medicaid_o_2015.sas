libname temp "/rpscan/u071439/Mark_Goodhart";

proc sql;
create table trash1 as select
    ENROLID,
    SVCDATE,
    PROC1,
    PROCGRP,
    PROCTYP,
    PROCMOD,
    max((STDPLAC=11)) as OFC_FLAG,
    max((STDPLAC=22)) as OTP_FLAG,
    max((STDPLAC=24)) as ASC_FLAG,
    SUM(PAY) as PHYSPAY
from 
    MDCD2015.medicaid_o_2015_v2
        (where=(
                FACPROF='P' and
                PAY>0       and
                missing(ENROLID)+missing(SVCDATE)+missing(PROC1)=0 and
                    (
                        PROCTYP='1' or PROCTYP='7' or PROCTYP='8'
                    )
                )
        )
group by
    ENROLID,
    SVCDATE,
    PROC1,
    PROCGRP; /*PROCGRP this is redundant only to save it in the file*/


proc sql;
create table trash2 as select
    ENROLID,
    SVCDATE,
    max(('99281'<=PROC1<='99285' or substr(REVCODE,1,3)='045' or REVCODE='0981')) as FLAGER,    
    SUM(PAY) as TOTPAY
from 
    MDCD2015.medicaid_o_2015_v2
        (where=(missing(ENROLID)+missing(SVCDATE)=0))
group by
    ENROLID,
    SVCDATE;

proc sql;
create table temp.otp1 as select
    a.*,
    b.TOTPAY
from 
    trash1 as a
inner join
    trash2 as b
on
   a.ENROLID=b.ENROLID and
   a.SVCDATE=b.SVCDATE
where
    b.FLAGER=0;

proc means data=temp.otp1 nway;
    class PROC1;
    var 
        OFC_FLAG
        OTP_FLAG
        ASC_FLAG 
        TOTPAY 
        PHYSPAY;
    output 
        out=temp.otp2(
            drop=_TYPE_
            rename=(_FREQ_=COUNT))
        mean=
        std=
        cv=
        /autoname;
run;

data temp.otp2;
set temp.otp2;
CPT_DESCRIPTION=substr(put(PROC1,$px.),7);
TOTPAY_CV=TOTPAY_CV/100;
PHYSPAY_CV=PHYSPAY_CV/100;
run;

proc means data=temp.otp1 nway;
    class PROCGRP;
    var 
        OFC_FLAG
        OTP_FLAG
        ASC_FLAG 
        TOTPAY 
        PHYSPAY;
    output 
        out=temp.otp3(
            drop=_TYPE_
            rename=(_FREQ_=COUNT))
        mean=
        std=
        cv=
        /autoname;
run;

data temp.otp3;
set temp.otp3;
PROCGRP_DESCRIPTION=put(PROCGRP,$procgrp.);
TOTPAY_CV=TOTPAY_CV/100;
PHYSPAY_CV=PHYSPAY_CV/100;
run;

proc export
data = temp.otp1
outfile="/rpscan/u071439/Mark_Goodhart/otp1.csv"
replace;
run;

proc export
data = temp.otp2
outfile="/rpscan/u071439/Mark_Goodhart/otp2.csv"
replace;
run;

proc export
data = temp.otp3
outfile="/rpscan/u071439/Mark_Goodhart/otp3.csv"
replace;
run;

