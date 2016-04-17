set more off
cd "C:\Users\Ben\Desktop\DisasterReporting\DisasterReporting\Reports"
insheet using dbMergeRen.csv,comma clear
save "Stata\dbMergeBoth",replace
insheet using dbMergeOwn.csv,comma clear
append using "Stata\dbMergeBoth"
save "Stata\dbMergeBoth",replace
use "Stata\dbMergeBoth",clear
local a=""
generate owned=type_of_occupancy=="Own as primary residence"
generate multifamily=type_of_residence=="Multi-Family"
generate singlefamily=type_of_residence=="Single Family"
generate earthquake=type_of_disaster=="Earthquake"
generate fire=type_of_disaster=="Fire"
generate flood=type_of_disaster=="Flooding"
generate hurricane=type_of_disaster=="Hurricane/Tropical storm"
generate mudslide=type_of_disaster=="Mud/Landslide"
generate other=type_of_disaster=="Other"
generate tornado=type_of_disaster=="Tornado"
generate typhoon=type_of_disaster=="Typhoon"
foreach y of varlist owned-typhoon{
local a "`a' `y'"
}
foreach x of varlist sewage minor10_0 minor10_1 minor10_2 major20_0 major20_1 major20_2 major30_0 major30_1 major30_2 major30_3 major40_0 major40_1 major40_2 major50_0 major50_1 major50_2 major60_0 major60_1 major74_0 major74_1 major74_2 destroyed80_0 destroyed80_1 destroyed80_2 destroyed80_3 destroyed80_4 destroyed90_0 destroyed90_1 destroyed100_0 destroyed100_1 water_damage water_mobilehome water_mobilehome_major_plywood water_mobilehome_major_nonplywoo water_mobilehome_destroyed water_conventionalhome_major water_conventionalhome_destroyed {
local b=substr("`x'",1,30)
gen `b'_1=`x'==1
local a "`a' `b'_1"
}
display "`a' predisaster_value" 
glm perdam `a' predisaster_value, link(logit) family(binomial) robust nolog
predict phat
mat b=e(b)
forv x=1/51{
display b[1,`x']
}
generate fema_grant_estimate = phat*predisaster_value
replace fema_grant_estimate=31900 if fema_grant_estimate>31900
histogram fema_grant_estimate
