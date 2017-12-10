libname temp "/rpscan/u071439/Mark_Goodhart";

DATA temp.otp1_subset_2;
SET temp.otp1;
KEEP proc1 PHYSPAY;
run;

proc export
data = temp.otp1_subset_2
outfile="/rpscan/u071439/Mark_Goodhart/otp1_subset_2.csv"
replace;
run;
