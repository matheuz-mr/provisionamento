import PySimpleGUI as sg

sg.theme('tema') 
#coluna com botões e inputs  
col = [     
            [sg.Text('Username              Password')],
            [sg.InputText(' ', size=(15,1),key='username'),sg.InputText(' ', size=(15,1),key='password')],
            [sg.Text('Tecnico                  Serial')],
            [sg.InputText('', size=(15,1),key='serial'),sg.InputText(' ', size=(15,1),key='nap')],
            [sg.Text('NAP                      Porta')],
            [sg.InputText('', size=(15,1),key='serial'),sg.InputText(' ', size=(15,1),key='nap')],
            [sg.Text('\r')],  
            [sg.Button(image_filename='remove.png',image_subsample=(5),button_color='#1C1C1C', key='remover'),
             sg.Button(image_filename='clean.png',image_subsample=(5),button_color='#1C1C1C',key='Limpar')],
            [sg.Button(image_filename='prov.png',image_subsample=(5),button_color='#1C1C1C', key='provisionar')]]
#coluna com output           
col2 = [
       [sg.Output(size=(90, 30),background_color='#000000',key='saida')],
        ]
#funções
def saida():
    a = values['username']
    print(a)
#tela principal
layout = [  
            [sg.Text('\r')],        
            [sg.Column(col,vertical_alignment='top',pad=(5,0)),sg.Column(col2,pad=(0,0))]
          ]
           
window = sg.Window('Provisionamento Vamos', layout,margins=(0,2))
#eventos
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Limpar':
        window.FindElement('username').Update('')
        window.FindElement('password').Update('')
        window.FindElement('serial').Update('')
        window.FindElement('nap').Update('')
    
    if event == 'provisionar':
        saida()   

window.close()

