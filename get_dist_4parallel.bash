
x0=`grep "225XOP      P" $1 | awk '{print $4}'`;  
y0=`grep "225XOP      P" $1 | awk '{print $5}'`; 
z0=`grep "225XOP      P" $1 | awk '{print $6}'`; 
x1=`grep "148TYR.*OH" $1 | awk '{print $4}'`;
y1=`grep "148TYR.*OH" $1 | awk '{print $5}'`;
z1=`grep "148TYR.*OH" $1 | awk '{print $6}'`;
dist=`echo "sqrt(($x0 - $x1)*($x0 - $x1) + ($y0 - $y1)*($y0 - $y1) + ($z0 - $z1)*($z0 - $z1))" | bc -l` 
echo "$1 $dist" >> dist
