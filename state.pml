load ~/Downloads/A5k_mod_refine_8.pdb
remove sol
hide lines, A5k_mod_refine_8
super A5k_mod_refine_8, test
show surface, test
show cartoon, A5k_mod_refine_8
set transparency, 0.35
color wheat, A5k_mod_refine_8
hide lines

extract lig, resn xop
as sticks, lig
show sticks, /test///248
color white, test
set stick_radius 0.15
set stick_ball, 1
set stick_ball_radius, 1.7
color grey, lig
zoom lig
