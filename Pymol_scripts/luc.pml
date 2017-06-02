# jap or tamara 
#
fetch 2d1s

sel dna, byres(n. CA)
select slu, resn slu
pseudoatom oo, slu
 
hide everything, solvent or (n. Na+K)
 
preset.ball_and_stick("oo")
 
#set_bond stick_color, 0xffff44, oo
#set_bond stick_transparency, 0.35, oo
 
color grey, oo and e. C
 
#set valence, 1, oo

 
ramp_new pRamp, oo, selection=dna, range=[1,10], color=hot

 
set surface_color, pRamp, dna
 
#show spheres, dna
#color white, dna
#color grey30, dna and e. C
#set sphere_scale, 0.99, dna
 
set ray_transparency_contrast, 0.20
set ray_transparency_oblique, 1.0
set ray_transparency_oblique_power, 20
 
show surface, dna
 
set surface_quality, 2
set light_count, 5
set ambient_occlusion_mode, 1
set ambient_occlusion_scale, 50
set ambient, 0.40
 
set transparency, 0.250
 
disable pRamp
 
set spec_power, 1200
set spec_reflect, 0.20
set ray_opaque_background, 0
set ray_shadow, 0

hide everything,oo
set fog,0

#ray
