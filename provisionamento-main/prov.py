import PySimpleGUI as sg
#TEMA LAYOUTS
sg.theme('tema') 
#COLUNA BOTÕES E INPUTS
col = [     
            [sg.Text('Username              Password')],
            [sg.InputText(' ', size=(15,1),key='username'),sg.InputText(' ', size=(15,1),key='password')],
            [sg.Text('Tecnico                  Serial')],
            [sg.InputText('', size=(15,1),key='tecnico'),sg.InputText(' ', size=(15,1),key='serial')],
            [sg.Text('NAP                      Porta')],
            [sg.InputText('', size=(15,1),key='nap'),sg.InputText(' ', size=(15,1),key='porta')],
            [sg.Text('\r')],  
            [sg.Button(image_filename='remove.png',image_subsample=(5),button_color='#1C1C1C', key='remover'),
             sg.Button(image_filename='clean.png',image_subsample=(5),button_color='#1C1C1C',key='Limpar')],
            [sg.Button(image_filename='prov.png',image_subsample=(5),button_color='#1C1C1C', key='provisionar')]]
#COLUNA OUTPUT           
col2 = [
       [sg.Output(text_color='#00FA9A',size=(115, 30),background_color='#000000',key='saida')],
        ]
#FUNÇÕES DO SISTEMA
def findnap():
    n = values['nap']
    if n[0:3] == 'nap':
        n = n.upper()
    data = open('data.txt')
    naps = data.readlines()
    for line in naps:
        nap = line[:9].replace(',','')
        position_barra = line[10:18].replace(',','' )
        vlan = line[19:22].replace(',','')
        position_hifen = line[22:30].replace(',','')
        ip = line[30:43].replace(',','')
        if nap == n:
             break
        
    print(nap)
    print(position_barra)
    print(vlan)
    print(position_hifen)
    print(ip)

#TELA PRINCIPAL
layout = [  
            [sg.Text('\r')],        
            [sg.Column(col,vertical_alignment='top',pad=(5,0)),sg.Column(col2,pad=(0,0))]
          ]
           
window = sg.Window('Provisionamento Vamos', layout,margins=(5,0))
#EVENTOS
while True:
    event, values = window.read()
#EVENTO FECHAR 
    if event == sg.WIN_CLOSED:
        break
#EVENTO DO BOTÃO LIMPAR INPUT E OUTPUT
    if event == 'Limpar':
        window.FindElement('username').Update('')
        window.FindElement('password').Update('')
        window.FindElement('tecnico').Update('')
        window.FindElement('serial').Update('')
        window.FindElement('nap').Update('')
        window.FindElement('porta').Update('')
        window.FindElement('saida').Update('')  
#EVENTO DO BOTÃO PROVISIONAMENTO
    if event == 'provisionar':
        findnap()   
window.close()

