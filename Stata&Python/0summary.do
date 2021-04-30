cd D:\result

poisson overspeed brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store pois
zip overspeed brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zipois
nbreg overspeed brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store nbr
zinb overspeed brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zinbr
estimates stats pois zipois nbr zinbr 
outreg2 [pois zipois nbr zinbr ] using Event1.doc,replace tstat

poisson highspeedbrake brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store pois2
zip highspeedbrake brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zipois2
nbreg highspeedbrake brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store nbr2
zinb highspeedbrake brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zinbr2
estimates stats pois2 zipois2 nbr2 zinbr2 
outreg2 [pois2 zipois2 nbr2 zinbr2 ] using Event2.doc,replace tstat

poisson harshacceleration brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store pois3
zip harshacceleration brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zipois3
nbreg harshacceleration brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store nbr3
zinb harshacceleration brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zinbr3
estimates stats pois3 zipois3 nbr3 zinbr3 
outreg2 [pois3 zipois3 nbr3 zinbr3 ] using Event3.doc,replace tstat

poisson harshdeceleration brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store pois4
zip harshdeceleration brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zipois4
nbreg harshdeceleration brakes range speed rpm accelerator enginefuelrate,r nolog exposure(kilo)
estimates store nbr4
zinb harshdeceleration brakes range speed rpm accelerator enginefuelrate,r nolog inflate(_cons) exposure(kilo)
estimates store zinbr4
estimates stats4 pois4 zipois4 nbr4 zinbr4 
outreg2 [pois4 zipois4 nbr4 zinbr4 ] using Event4.doc,replace tstat