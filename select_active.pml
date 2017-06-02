
#
# 1) load your protein
# 2) remove the ligand
# 3) do APBS stuff
# 4) load the ligand as a
# 5) run this script
# 6) choose an orientation
# 7) save as png

bg_color white
set surface_quality, 2
set transparency, 0.15
hide lines

set ambient, 0
set shininess, 10
set direct, 1
set light_count, 1
set specular, 0
extract lig,resn xop
sele site, all within 10 of lig
sele site, br. site and not lig 

sele close_res, not lig within 4 of lig and not e. H
sele close_res, br. close_res

hide everything, not site
show sticks, lig
set stick_radius, 0.25, lig
set stick_radius, 0.175
show sticks, resi 33 and c. L
show sticks, close_res

label close_res and n. cb, "%s-%s%s" % (chain, one_letter[resn], resi)
set label_color, white
set label_position,[0,1,25]
set label_size, 20
show cartoon, site
set cartoon_side_chain_helper, 1
set h_bond_from_proton, 1
distance hbs, lig, site, mode=2

