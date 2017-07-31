def set_prop_val(nodes, ind_prop, val_prop):
	# texture
	if ind_prop == 0:
		nodes["Group"].inputs[1].default_value = val_prop / 10.0
	# albedo
	elif ind_prop == 1:
		nodes["Group"].inputs[2].default_value = val_prop / 10.0
	# specularity
	elif ind_prop == 2:
		nodes.get("Principled BSDF").inputs[5].default_value = val_prop
		# nodes["Group"].inputs[2].default_value = val_prop
	# roughness
	elif ind_prop == 3:
		nodes.get("Principled BSDF").inputs[7].default_value = val_prop / 10.0
		# nodes["Group"].inputs[1].default_value = val_prop
	# concavity
	elif ind_prop == 4:
		print('concavity not ready')