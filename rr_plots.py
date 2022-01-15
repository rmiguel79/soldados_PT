# :tabSize=2:indentSize=2:noTabs=false:
'''Cria plots offline de velocidade e de progresso diário de RR do clã.
As velocidades são "normalizadas", ou seja, é descontado o efeito dos bónus diários
para se poder comparar efetivamente o "quanto se vence e participa" diariamente entre
dias e semanas diferentes.
'''
from plotly.offline import plot
import codecs
import numpy as np
import plotly.graph_objs as go

from rr_projecoes import pesos, vals

# # Objetivo definido para cada semana.
# lims = [20, 30, 65, 92, 65, 92]
# for _ in range(len(lims), len(vals)):
# 	lims.append(65)
# lims[-3] = 60
# lims[-2] = 60
# lims[-1] = 60
lims = [20, 30, 65, 92, 65, 92, 65, 65, 65, 65, 65, 65, 60, 60, 60]

data = []
velocidades_ys = []
for n,(semana,lim) in enumerate(zip(vals, lims)):
	semana_xs, semana_ys = [],[]
	for x,y in semana:
		semana_xs.append(x)
		semana_ys.append(y)
	
	semana_xs.append(semana_xs[-1]+1)
	semana_ys.append(lim*1000)
	
	velocidade_ys = []
	prv = 0.
	for a,b in zip(semana_ys, pesos):
		# Ao dividir pelo bónus diário, em "b", estamos a reduzir todos os valores à mesma
		# escala, como se não houvesse bónus diários, para se poder comparar velocidades
		# entre dias diferentes da semana.
		velocidade_ys.append((a-prv) / b)
		prv = a
	velocidades_ys.append(velocidade_ys[:-1])
	
	# Valores de RR diários (a acumular ao longo dos dias em cada semana).
	data.append(go.Scatter(
	  x=np.array(semana_xs) + (n*7),
	  y=np.array(semana_ys),
	  marker=dict(size=8),
	  mode='lines+markers',
	  name=f'RR na semana {n+1}',
	  text=(f'RR na semana {n+1}',),
	  hoverinfo='text',
	  visible=True,
	  ))
	
	# Velocidade diária, descartando bónus diários.
	data.append(go.Scatter(
	  x=np.array(semana_xs) + (n*7),
	  y=np.array(velocidade_ys),
	  marker=dict(size=8),
	  mode='lines+markers',
	  name=f'semana {n+1}: velocidade',
	  text=(f'semana {n+1}: velocidade',),
	  hoverinfo='text',
	  visible=False,
	  ))

# Para cada semana, calcula-se a velocidade média e faz-se um plot dela, para vermos
# como é que o clã vai evoluindo ao longo de semanas sucessivas.
medias_semanais = [sum(a) / len(a)  for a in velocidades_ys]
data.append(go.Scatter(
  x=np.arange(len(medias_semanais)) * 7. + 3.5,
  y=np.array(medias_semanais),
  marker=dict(size=8),
  mode='lines+markers',
  name=f'Evolução veloc.',
  text=(f'Evolução veloc.',),
  hoverinfo='text',
  visible=False,
  ))

layout = dict(
  title=dict(text='Conquistas de RR dos Soldados PT', x=0.5),
  xaxis=dict(title='Dias ao longo dos tempos'),
  yaxis=dict(title='RR'),
  updatemenus=[dict(
    active=0,
    bordercolor='#BEC8D9',
    buttons=[
      dict(
        args=[dict(visible=sum([[True,False] for _ in vals], []) + [False])],
        label='RR acumulados',
        method='update',),
      dict(
        args=[dict(visible=sum([[False,True] for _ in vals], []) + [False])],
        label='Velocidades diárias',
        method='update',),
      dict(
        args=[dict(visible=sum([[False,True] for _ in vals], []) + [True])],
        label='Veloc.+evolução',
        method='update',),
      dict(
        args=[dict(visible=sum([[False,False] for _ in vals], []) + [True])],
        label='Evolução do clã',
        method='update',),
      ],
    direction='down',
    showactive=True,
    type='buttons',
    )]
  )


fig = dict(data=data, layout=layout)

hdr = '''<!DOCTYPE html>
  <html>
  <head>
    <meta content="text/html; charset=utf-8" />
    <script src="https://cdn.plot.ly/plotly-latest.min.js"> </script>
    <style>
      table {
        border-collapse: collapse;
        font-family: Tahoma, Geneva, sans-serif;
        }
      table td {
        padding: 15px;
        }
      table thead td {
        background-color: #54585d;
        color: #ffffff;
        font-weight: bold;
        font-size: 13px;
        border: 1px solid #54585d;
        }
      table tbody td {
        color: #636363;
        border: 1px solid #dddfe1;
        text-align: right;
        }
      table tbody tr {
        background-color: #f9fafb;
        }
      table tbody tr:nth-child(odd) {
        background-color: #ffffff;
        }
      </style>
    </head>
  <body style="font:16px Verdana,Arial; margin:25px; background:#fff">
    '''.replace('\n  ', '\n')

fld_hdr = '''\
  <details style="margin-left:18px"> <summary>%s</summary>
    <div style="margin-left:34px">
'''

tbl_hdr = '''\
      <br />
      <table>
        <thead>
          <tr> <td>Semana</td> <td>2a(3a)</td> <td>3a(4a)</td> <td>4a(5a)</td> <td>5a(6a)</td> <td>6a(sab)</td> <td>sab(dom)</td> <td>dom(2a)</td> </tr>
          </thead>
        <tbody>
'''

tbl_tpl = '          <tr> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> </tr>\n'

tbl_ftr = '''\
          </tbody>
        </table>
      <br />
'''

fld_ftr = '''\
      </div>
    </details>
'''

ftr = '''\
    </body>
  </html>
  '''.replace('\n  ', '\n')

my_div = plot(fig, include_plotlyjs=False, output_type='div')
# my_div = my_div.replace(', {"showLink": true, "linkText": "Export to plot.ly"}', '')
# my_div = my_div.replace(', {"linkText": "Export to plot.ly", "showLink": true}', '')
# my_div = my_div.replace('style="height: 100%; width: 100%;"', 'style="height: 750px; width: 1500px;"')

with open('rr_plots.html', 'w', encoding='utf-8') as fw:
	fw.write(hdr)
	fw.write(my_div)
	fw.write('\n  <br />\n  Clique nas linhas abaixo para aceder às tabelas com os valores:\n')
	
	fw.write(fld_hdr % 'Valores de RR diários acumulados')
	fw.write(tbl_hdr)
	velocidades_ys = []
	for n,(semana, lim) in enumerate(zip(vals, lims)):
		ys = [str(n+1)]
		veloc_ys = [str(n+1)]
		prv = 0.
		for a,b in zip(semana, pesos):
			ys.append('%d' % a[1])
			veloc_ys.append('%d' % ((a[1]-prv) / b))
			prv = a[1]
		ys.append(str(lim*1000))
		for a in range(len(ys)-1, 7):
			ys.append('-')
		for a in range(len(veloc_ys)-1, 7):
			veloc_ys.append('-')
		fw.write(tbl_tpl.format(*ys))
		velocidades_ys.append(veloc_ys)
	fw.write(tbl_ftr)
	fw.write(fld_ftr)
	
	fw.write(fld_hdr % 'Velocidades excluindo bónus diários (ignorando o último dia)')
	fw.write(tbl_hdr)
	for veloc_ys in velocidades_ys:
		fw.write(tbl_tpl.format(*veloc_ys))
	fw.write(tbl_ftr)
	fw.write(fld_ftr)
	
	fw.write(fld_hdr % 'Velocidades médias semanais excluindo bónus diários')
	fw.write('''\
      <br />
      <table>
        <thead>
          <tr> <td>Semana</td> <td>Velocidade média</td> </tr>
          </thead>
        <tbody>
''')
	for n,m in enumerate(medias_semanais):
		fw.write('          <tr> <td>{}</td> <td>{}</td> </tr>\n'.format(n+1, int(m)))
	fw.write(tbl_ftr)
	fw.write(fld_ftr)
	
	fw.write(ftr)                  
print('rr_plots.html escrito.')
