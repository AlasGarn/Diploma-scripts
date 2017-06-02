

set use_shaders
set ray_shadows, 0
set stick_as_cylinders
set ribbon_as_cylinders
set line_as_cylinders
set nonbonded_as_cylinders
bg_color white
sele ions, resn NA+CL
remove ions
remove sol

show surface, test
show cartoon, test
set transparency, 0.35
hide lines

extract lig, resn xop
as sticks, lig

sele ac, all within 7 of resn XOP
sele ac2, br. ac
show sticks, ac2

show sticks, /test///248
color white, test
set stick_radius 0.15
set stick_ball, 1
set stick_ball_radius, 1.7
color grey, lig
zoom lig


cmd.volume_ramp_new('ramp138', [\
     -0.00, 0.00, 0.00, 0.00, 0.00, \
      0.07, 0.01, 0.00, 0.78, 0.27, \
      0.17, 0.00, 0.00, 0.00, 0.00, \
    ])

volume 123, mad, ramp138
