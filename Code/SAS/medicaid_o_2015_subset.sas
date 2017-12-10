libname temp "/rpscan/u071439/Mark_Goodhart";

DATA temp.otp1_subset;
SET temp.otp1;
KEEP proc1 proctyp procmod;
run;

proc export
data = temp.otp1_subset
outfile="/rpscan/u071439/Mark_Goodhart/otp1_subset.csv"
replace;
run;
