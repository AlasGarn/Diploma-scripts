for a in range(12):
	cmd.load(str(a+1)+"_nometa/"+str(a+1)+".pdb")
	cmd.load_traj(str(a+1)+"_nometa/meta.xtc",str(a+1))

