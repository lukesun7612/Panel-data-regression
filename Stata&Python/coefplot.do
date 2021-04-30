cd D:\result
center brakes range speed rpm acceleratorpedalposition enginefuelrate BRAKES RANGE SPEED RPM ACC EN, prefix(z_) standardize

nbreg overspeed z_brakes z_range z_speed z_rpm z_accelerator z_enginefuelrate,r nolog exposure(kilo)
estimates store nbr_overspeed

nbreg highspeedbrake z_brakes z_range z_speed z_rpm z_accelerator z_enginefuelrate,r nolog exposure(kilo)
estimates store nbr_highspeedbrake

nbreg harshacceleration z_brakes z_range z_speed z_rpm z_accelerator z_enginefuelrate,r nolog exposure(kilo)
estimates store nbr_harshacceleration

nbreg harshdeceleration z_brakes z_range z_speed z_rpm z_accelerator z_enginefuelrate,r nolog exposure(kilo)
estimates store nbr_harshdeceleration

nbreg OVERSPEED z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN i.date0 ID2-ID182, r nolog exposure(KILO)
estimates store xtnb_overspeed

nbreg HIGHSPEEDBRAKE z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN i.date0 ID2-ID182, r nolog exposure(KILO)
estimates store xtnb_highspeedbrake

nbreg HARSHACCELERATION z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN i.date0 ID2-ID182, r nolog exposure(KILO)
estimates store xtnb_harshacceleration

nbreg HARSHDECELERATION z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN i.date0 ID2-ID182, r nolog exposure(KILO)
estimates store xtnb_harshdeceleration

coefplot nbr_overspeed,bylabel(overspeed)||nbr_highspeedbrake,bylabel(highspeedbrake)|| nbr_harshacceleration,bylabel(harshacceleration)||nbr_harshdeceleration,bylabel(harshdeceleration)||, drop(_cons) byopts(xrescale) xline(0, lp(dash) lc(black*0.3)) 

coefplot (xtnb_overspeed, keep(z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN)),bylabel(overspeed)||(xtnb_highspeedbrake, keep(z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN)),bylabel(highspeedbrake)||(xtnb_harshacceleration, keep(z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN)),bylabel(harshacceleration)||(xtnb_harshdeceleration, keep(z_BRAKES z_RANGE z_SPEED z_RPM z_ACC z_EN)),bylabel(harshdeceleration)||,byopts(xrescale) xline(0, lp(dash) lc(black*0.3)) 
 

