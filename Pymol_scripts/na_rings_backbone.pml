set stick_radius, 0.1
set sphere_scale, .25
set fog,0
set opaque_background, 1
set cartoon_ring_width, 0.3



set cartoon_ladder_mode, 1
set cartoon_ring_finder, 3
set cartoon_ring_mode, 1
hide everything, all
select na, resn DT+U+DA+A+DG+G+DC+C+DG5+DG3+T+G+A+C
select back_b1, n. C1'+C2'+O2'+C3'+O3'+C4'+O4'+C5'+O5'+P and na 
select back_b2, n. C1'+C2'+O2'+C3'+O3'+C4'+O4'+C5'+O5'+P+N1+N9 and na 
select rings, na and not back_b1 and not (e. H or n. Op1 or n. op2)

color white,back_b2
set cartoon_ring_color, gray60, resn DT+U+DT5+DT3+T
set cartoon_ring_color, gray30, resn DG+G+DG5+DG3
set cartoon_ring_color, gray20, resn DA+A+DA5+DA3
set cartoon_ring_color, gray70, resn DC+C+DC5+DC3

show cartoon, rings
show sticks,  back_b2
show spheres, n. P

set ray_trace_mode, 4

set light_count,10
set spec_count,1
set shininess, 10
set specular, 0.05
set ambient,0
set direct,0
set reflect,1.5
set ray_shadow_decay_factor, 20.1
set ray_shadow_decay_range, 0.1
set 
bg_color white 

