# clusters all points in time series that are less than 0.4 (presumably the distance between reacting atoms)
# and outputs the frame with minimal distance within each cluster

#### WARNING!!! ####
#### make sure you remove the bad trasitions from restarts in COLVAR ####

library(apcluster)
setwd('AB/hists/')

  AB=c("a46R","a46S","a43R","a43S","a49R","a49S","a216R","a21S","a7R","a7S","a1R","a1S")
 for (a in AB) {
   print(AB)
   driver <- read.table(paste('driver', AB, ".out.ready", sep=""))

  
  colvar = read.table(paste('COLVAR', AB, ".ready", sep=""))
  colnames(colvar) = c('time','d.x','d2','bias',"ext",'uw', 'lw','x', 'y', 'z')
  colvar = colvar[1:nrow(driver),]
  
  driver = cbind(driver, colvar[5])
  driver = cbind(driver, colvar[2])
  colnames(driver) = c('time','a52y','xi','ang','ang2','d1', 'd2','d3', 'a1', 'a2','a3','fe','d.x')
  # leave only the reaction-favorable frames
  driver_cut = driver[ driver$a52y < 1.0 &
                         #driver$fe > 20 &
                         driver$d.x > -1.2 &
                 driver$ang > pi/1.5 &  
             #    driver$ang2 > pi/1.5 & 
                  driver$a1 < pi/1.5 &
                  driver$a2 < pi/1.5 &
                  driver$a3 < pi/1.5 #&
                #   driver$d1 < driver$a52y &
                # driver$d2 < driver$a52y &
                # driver$d3 < driver$a52y 
              ,]
plot(driver$d.x[seq(1,nrow(driver),20)], type = 'l')
plot(driver$a52y[seq(1,nrow(driver),20)], type = 'l')
print(length(driver_cut))}
  # check if the filtered traj contains any frames at all

  # use time stamps to get fes coordinates: d.x, d2, xi, x2 for A5 from COLVAR
  coords = colvar[driver_cut$time, c('d.x','d2')]
  # read fes and find closest points
  fes = read.table(paste("HILLS", AB, ".fes", sep=""))

  fes = cbind(fes[,1:2], fes[,3])
  colnames(fes) = c("d2","d.x","fe")

  
  getclose <- function(x){ # x is a row 
    d = 100 # distance to closest point
    d.x = x[1]
    d2 = x[2]
    for (i in 1:nrow(fes)){
      d_new = sqrt(sum((fes[i,2:1] - x)^2)) # the d2 and d.x columns are swapped in COLVAR/FES
      if (d_new < d) { 
        d = d_new;
        fe = fes[i,3];
      }
    }
    print(x)
    return(fe)
  }

# apply
  
fre = apply(coords, 1, getclose)

driver_cut = cbind(driver_cut,fre)

 # driver_cut = cbind(driver_cut[1],(driver_cut[11] - min(fes[,3])))

  hi = cbind(driver_cut[1], driver_cut[12])
  hi$fre = hi$fre - min(fes[,3])

  hist(hi$fre, 
       #breaks = 20, 
       main = paste("Гистограмма распределения комплексов по энергии.", AB), 
       xlab = "Энергия, кДж/моль",
    #   xlim = range(0:80),
       ylab = "Число комплексов",
       ylim = range(0:200),
       col = "red")



  # ap cluster the remaining time series to get groups of frames
  cl <- apcluster(negDistMat(r=2), hi, q=0.7)

  frames = NULL  
  # choose frames with mininal distance
  for (cls in cl@clusters){
    hii = hi[names(cls),] # get the cluster from hi
    frame = rownames(hii[hii$fre == min(hii$fre),])[1] # get time from row with min energy within cluster
  print(frame)
    frames=c(frames,
             frame)
  }


  plot(cl, hi, main="Clusters", xlab='time, ps', ylab='free energy')
  points(-10*driver$d.x, type = 'l')
  #output
  
  #fr = data.frame(frames, rep(1,length(frames)))
  
  out = cbind(driver[1],rep(0,nrow(driver)))
  out[frames,2] = 5
  #out2 = match(out[[1]],fr[[1]])
  #out2 = cbind(out[1],out2)
  #out2[is.na(out2[2]),2] = 0
  
  write.table(out, file = 'pre-reaction-frames.xvg', sep = '\t', row.names = F, col.names = F)


