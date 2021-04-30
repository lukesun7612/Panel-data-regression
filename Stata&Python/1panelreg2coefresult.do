cd D:\result
center brakes range speed rpm acceleratorpedalposition enginefuelrate, prefix(z_) standardize

local v1 "z_brakes z_range z_speed z_rpm z_accelerator z_enginefuelrate i.date0 id2-id182" 
nbreg overspeed `v1', r nolog exposure(kilo)
estimates store xtnb_overspeed

nbreg highspeedbrake `v1', r nolog exposure(kilo)
estimates store xtnb_highspeedbrake

nbreg harshacceleration `v1', r nolog exposure(kilo)
estimates store xtnb_harshacceleration

nbreg harshdeceleration `v1', r nolog exposure(kilo)
estimates store xtnb_harshdeceleration

esttab * using coefresult.csv,replace drop(lnalpha) wide
esttab * using coefresult1.csv,replace cells(b) drop(z_brakes z_range z_speed z_rpm z_acceleratorpedalposition z_enginefuelrate _cons 1.date0 2.date0 3.date0 4.date0 5.date0 6.date0 lnalpha) plain