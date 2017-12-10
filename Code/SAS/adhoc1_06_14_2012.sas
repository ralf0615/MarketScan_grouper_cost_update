/*
options comamid=tcp;
filename rlink "C:\Program Files\SAS\SAS 9.1\connect\saslink\tcpunix.scr";
%let sashost=nike.medstat.com;
signon sashost;
*/

/*
rsubmit;
proc contents data=arch2010.ccaeo101; run;

rsubmit;
proc print data=arch2010.ccaeo101 (obs=100);
var proctyp proc1 facprof stdplac;
format proctyp $proctyp. proc1 $px. procgrp procgrp.;
run;

rsubmit;
proc print data=arch2010.ccaeo101 (obs=500);
var enrolid svcdate proctyp proc1 facprof stdplac;
run;
*/

rsubmit;
options obs=10000;

libname temp "/rpscan2/u0086308/bcbs/temp";

proc format;
value $selectcpt
    10001-99200='yes'
    other='no';

proc sql;
create table trash1 as select
    ENROLID,
    SVCDATE,
    PROC1,
    PROCGRP,
    max((STDPLAC=11)) as OFC_FLAG,
    max((STDPLAC=22)) as OTP_FLAG,
    max((STDPLAC=24)) as ASC_FLAG,
    SUM(PAY) as PHYSPAY
from 
    arch2010.ccaeo101
        (where=(
                FACPROF='P' and
                PAY>0       and
                missing(ENROLID)+missing(SVCDATE)+missing(PROC1)=0 and
                PROCTYP='1' and put(PROC1,$selectcpt.)='yes'))
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
    arch2010.ccaeo101
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

enduyrsubmit;

libname ltemp "c:\PPROJECTS\TCC\BCBS\temp";
libname rtemp remote "/rpscan2/u0086308/bcbs/temp" server=sashost;

data ltemp.otp1;
set rtemp.otp1;
run;
data ltemp.otp2;
set rtemp.otp2;
run;
data ltemp.otp3;
set rtemp.otp3;
run;

signoff sashost;
