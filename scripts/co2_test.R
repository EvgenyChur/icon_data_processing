




## forcing period
startyear <- 1901
endyear   <- 2015

## CO2 data
co2y<-read.table('C:/Users/evchur/Desktop/DATA/FORCING_QUINCY/DATA_CO2/GCP_co2_global.dat')
co2y_dC13<-read.table('C:/Users/evchur/Desktop/DATA/FORCING_QUINCY/DATA_CO2/delta13C_in_air_input4MIPs_GM_1850-2021_extrapolated.txt')
co2y_DC14<-read.table('C:/Users/evchur/Desktop/DATA/FORCING_QUINCY/DATA_CO2/Delta14C_in_air_input4MIPs_SHTRNH_1850-2021_extrapolated.txt')

swdown=172


for (year in c(startyear:endyear))
{
  co2<-rep(co2y[co2y[,1]==year,2],length(swdown))
  co2_dC13<-rep(co2y_dC13[(co2y_dC13[,1]-0.5)==year,2],length(swdown))
  if(latsite>30) C14lat=2
  if(latsite>-30&latsite<=30) C14lat=3
  if(latsite<=-30) C14lat=4
  co2_DC14<-rep(co2y_DC14[(co2y_DC14[,1]-0.5)==year,C14lat],length(swdown))
  year_out<-rep(year,length(swdown))
  forcing<-cbind(year_out,doy,hod,swdown,lwdown,tair,qair,press,rain,snow,wind,co2,co2_dC13,co2_DC14,nhx,noy,pdep)
  
}

