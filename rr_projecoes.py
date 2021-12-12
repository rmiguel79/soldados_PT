# :tabSize=2:indentSize=2:noTabs=false:
discord_old='discord.gg/dHWfrDBnmG'
discord_old='https://discord.gg/dHWfrDBnmG'
discord='https://discord.gg/kbA3F8qssg'
discord='discord.gg/kbA3F8qssg'
whatsapp='chat.whatsapp.com/BwFpogIrlca6VBSkDYePga'
lim_sem =65000.
bonus=(0., 0.2, 0.4, 0.6, 1., 3., 5.)
pesos=[1.+a for a in bonus]

vals=((
	(1, 1831.),
	(2, 4028.),
	(3, 6592.),
	(4, 9304.),
	(5, 12604.),
	), (
	(1, 2140.),
	(2, 5525.),
	(3, 8715.),
	(4, 13075.),
	(5, 19815.),
	), (
	(1, 4834.),
	(2, 10004.),
	(3, 15229.),
	(4, 23454.),
	(5, 32483.),
	(6, 56635.),
	),(
	(1, 4659.),
	(2, 10961.),
	(3, 19387.),
	(4, 28897.),
	(5, 39923.),
	(6, 59803.),
	),(
	(1, 7698.),
	(2, 15736.),
	(3, 26607.),
	(4, 36701.),
	(5, 50777.),
	),(
	(1, 8702.),
	(2, 16838.),
	(3, 26453.),
	(4, 37467.),
	(5, 48721.),
	(6, 77231.),
	),(
	(1, 8871.),
	(2, 19180.),
	(3, 29059.),
	(4, 39280.),
	(5, 55526.),
	),(
	(1, 9915.),
	(2, 21813.),
	(3, 34090.),
	(4, 45541.),
	(5, 63057.),
	),(
	(1, 9973.),
	(2, 21140.),
	(3, 33358.),
	(4, 48679.),
	),(
	(1, 9521.),
	(2, 19589.),
	(3, 32667.),
	(4, 43184.),
	(5, 61786.),
	),(
	(1, 11177.),
	(2, 22491.),
	(3, 36356.),
	(4, 54099.),
	),(
	(1, 10928.),
	(2, 23729.),
	(3, 38318.),
	(4, 54432.),
	))

if __name__ == '__main__':
	# Evitar andar a ver todas as semanas até hoje
	num_semanas_removidas = 0
	if 1==1:
		num_semanas_removidas = len(vals) - 1
		vals = (vals[-1],)
	
	# Projeções
	for n,semana in enumerate(vals):
		print(f'semana {n + num_semanas_removidas + 1}')
		for dia, atual in semana:
			print(f'  projeção ao dia {dia}')
			atual_por_unidade = atual / sum(pesos[:dia])
			projs = []
			for a in range(dia, len(pesos)+1):
				val = atual_por_unidade * sum(pesos[:a])
				print(f'    dia {a} - rr esperado {val:5.0f}')
				projs.append(val)
	
	prv_b = projs.pop(0)
	
	# minimos diários como meta
	if 1==0:
		for a in range(7):
			print(f'''\
	Hoje precisávamos ter atingido {lim_sem*sum(pesos[:a+1])/sum(pesos):.0f}'''.replace('\n\t', '\n').strip())
	
	# mínimo no dia atual
	if 1==0:
		print(f'{lim_sem*sum(pesos[:vals[-1][-1][0]])/sum(pesos)}')
	
	# histórico da semana e previsão da meta
	if 1==1:
		hist = ''
		for a in range(len(vals[-1])):
			hist += f'\n{vals[-1][a][1]:5.0f}({100.*vals[-1][a][1]/(lim_sem*sum(pesos[:a+1])/sum(pesos)):.0f})%'
		hist += f'\n{lim_sem/1000.:.0f}k'
		s = f'Histórico da semana:{hist}\n{discord}'
		print(f'\n{len(s)}')
		print(s)
		
		prv_a,prv_b = 0,prv_b
		for a,b in zip(range(vals[-1][-1][0]+1, 8), projs):
			if float(b) > lim_sem:
				break
			prv_a,prv_b = a,b
		inst_meta = (a-1) + (lim_sem - prv_b) / (b - prv_b)
		dias = 'na_2a_feira na_3a_feira na_4a_feira na_5a_feira na_6a_feira no_sábado no_domingo'.split()
		dias = [c.replace('_',' ') for c in dias]
		dia_idx = int(inst_meta)
		horas = ((inst_meta - dia_idx) * 24.) + 9.
		if horas >= 24.:
			horas -= 24.
			dia_idx += 1
	
	s = f'''\
	Hoje prevemos alcançar {projs[0]:.0f} ({int(projs[-1])*100./lim_sem:.0f}% da linha mínima) e chegar à meta {dias[dia_idx]} pelas {horas:.0f}h
	Info pa novos membros,temos canal d discord
	{discord}'''.replace('\n\t', '\n').strip()
	print(f'\n{len(s)}')
	print(s)



