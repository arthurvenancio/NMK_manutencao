import os as rem
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.image import Image
from numpy import log
from pymongo import MongoClient
from datetime import datetime,timedelta
from math import e
import matplotlib.pyplot as plt

client = MongoClient("mongodb+srv://arthur:teste@cluster0.bvzog.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.get_database('empresa')
os=db.ordem_servico

mes_selecionado=3

def minutos_totais(valor_datetime):
        valor_datetime_str=str(valor_datetime)
        valor_str=valor_datetime_str.replace(':',' ').split()
        if valor_str[1]=='days,':
                valor_horas_totais=(float(valor_str[0])*(60*24))+(float(valor_str[2])*60)+((int(valor_str[3])))
        else:
                valor_horas_totais=(float(valor_str[0]))*60+((float(valor_str[1])))
        return float(valor_horas_totais)

def horas_totais(valor_datetime):
        valor_datetime_str=str(valor_datetime)
        valor_str=valor_datetime_str.replace(':',' ').split()
        if valor_str[1]=='days,':
                valor_horas_totais=int(valor_str[0])*24+int(valor_str[2])+((float(valor_str[3])/60))
        else:
                valor_horas_totais=int(valor_str[0])+((float(valor_str[1])/60))
        return str(valor_horas_totais)

def data_usuario (dia,mes,ano,hora,minuto,segundos):
        data_evento=dia+mes+ano+' '+hora+':'+minuto+':'+segundos
        data_datetime=datetime.strptime(data_evento,"%d%m%Y %H:%M:%S")
        data_timestamp=datetime.timestamp(data_datetime)
        return data_timestamp

Builder.load_string("""
<Gerenciador>:
    TelaMenu:
        name:'menu'
    CadastroOs:
        name:'cadastroOs'
    TelaCadastroEquipamentos:
        name:'cadastroEquipamento'
    TelaListaEquipamentos:
        name:'listaEquipamento'
    TelaEquipamentoIndividual:
        name:'equipamentoIndividual'
    TelaGrafico:
        name:'grafico'
    TelaGrafico2:
        name:'grafico2'
    CadastroOp:
        name:'cadastroOp'
    TelaEquipamentoInventario:
        name:'inventario'
    SelecaoIndividual:
        name:'selecao'
    
<TelaMenu>:
    GridLayout:
        cols:1
        padding:0.05*self.width,0.1*self.height
        spacing : 0.04*self.height
        Label: 
            text:'MENU INICIAL'
            font_size: '16'
        Button:
            text:'Cadastro de Manutenção'
            font_size: '20'
            on_release: app.root.current = 'cadastroOs'
        Button:
            text:'Cadastro de Operação'
            font_size: '20'
            on_release: app.root.current = 'cadastroOp'
        Button:
            text:'Cadastro de Equipamentos'
            font_size: '20'
            on_release: app.root.current = 'cadastroEquipamento'
        Button:
            text:'Lista de Equipamentos'
            font_size: '20'
            on_release: app.root.current = 'listaEquipamento'
        Button:
            text:'Sair'
            font_size: '18'
            on_release: app.stop()
            
<CadastroOs>:
    BoxLayout:
        orientation:'vertical'
        anchor_y:'bottom'
        ActionBar:
            ActionView:
                ActionPrevious:
                    title:'Cadastro de OM'
                    on_release:app.root.current = 'menu'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
    GridLayout:
        cols:1
        padding:0.05*self.width,0.1*self.height
        spacing : 0.04*self.height
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            id:box_tag
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            Button:
                text:'Iniciar Manutenção'
                font_size: '20sp'
                on_press:root.inicio()
                size_hint_x:0.7
            BoxLayout:
                orientation: 'horizontal'
                id:confirmação
                size_hint_x: 0.3
        BoxLayout:
            size_hint_y: 0.01
            Label:
                id:inicio
                text:''
                size_hint_y: None
                size: self.texture_size
                color:0,0,0,1
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            Button:
                text:'Finalizar Manutenção'
                font_size: '20sp'
                on_press:root.fim()
                on_release:root.apagar()
        BoxLayout:
            size_hint_y: 0.01
            Label:
                id:fim
                text:''
                size_hint_y: None
                size: self.texture_size
                color:0,0,0,1
<CadastroOp>:
    BoxLayout:
        orientation:'vertical'
        anchor_y:'bottom'
        ActionBar:
            ActionView:
                ActionPrevious:
                    title:'Cadastro de Operação'
                    on_release:app.root.current = 'menu'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
    GridLayout:
        cols:1
        padding:0.05*self.width,0.1*self.height
        spacing : 0.04*self.height
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            id:box_tag
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            Button:
                text:'Iniciar Operação'
                font_size: '20sp'
                on_press:root.inicio()
                size_hint_x:0.7
            BoxLayout:
                orientation: 'horizontal'
                id:confirmação
                size_hint_x: 0.3
        BoxLayout:
            size_hint_y: 0.01
            Label:
                id:inicio
                text:''
                size_hint_y: None
                size: self.texture_size
                color:0,0,0,1
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            Button:
                text:'Finalizar Operação'
                font_size: '20sp'
                on_press:root.fim()
                on_release:root.apagar()
        BoxLayout:
            size_hint_y: 0.01
            Label:
                id:fim
                text:''
                size_hint_y: None
                size: self.texture_size
                color:0,0,0,1
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: 0.3
            Button:
                text:'Falha na Operação'
                font_size: '20sp'
                on_press:root.falha()
                on_release: root.apagar()
        BoxLayout:
            size_hint_y: 0.01    
            Label:
                id:falha
                text:''
                size_hint_y: None
                size: self.texture_size
                color:0,0,0,1
<TelaCadastroEquipamentos>:
    BoxLayout:
        orientation:'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                    title:'Cadastro de Equipamentos'
                    on_release:app.root.current = 'menu'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
    GridLayout:
        cols:1
        padding:0.05*self.width,0.1*self.height
        spacing : 0.04*self.height
        BoxLayout:
            size_hint_y:0.375
            Label:
                text:'TAG de equipamento'
            TextInput:
                id:TAG
        BoxLayout:
            size_hint_y:0.375
            Label:
                text:'Nome do equipamento'
            TextInput:
                id:nome
        BoxLayout:
            size_hint_y:0.375
            Label:
                text:'Preço de Compra'
            TextInput:
                id:preço_de_compra
                text:'XXXX.XX'
        BoxLayout:
            size_hint_y:0.375
            Label:
                text:'Nome de Fornecedor'
            TextInput:
                id:fornecedor
        BoxLayout:
            size_hint_y:0.375
            Label:
                text:'Anos para Depreciação Total'
            TextInput:
                id:anos_de_depreciação
        BoxLayout:
            size_hint_y:0.375
            Label:
                text:'Inicio de Operação'
            Spinner:
                id:dia_i_op
                text:'Dia'
                values:("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31")
            Label:
                text:'/'
                size_hint_x: None
                size: self.texture_size
            Spinner:
                id:mes_i_op
                text:'Mês'
                values:("1","2","3","4","5","6","7","8","9","10","11","12")
            Label:
                text:'/'
                size_hint_x: None
                size: self.texture_size
            BoxLayout:
                orientation:'vertical'
                Label:
                    text:'Ano'
                    size_hint_y: None
                    size: self.texture_size
                TextInput:
                    id:ano_i_op
        BoxLayout:
            size_hint_y:0.25
            Button:
                text:'Cadastrar'
                on_press: root.cadastro()
                on_release: root.apagar()

<TelaListaEquipamentos>:
    BoxLayout:
        orientation:'vertical'
        ScrollView:
            BoxLayout:
                padding:0.05*self.width,0.1*self.height
                spacing : 0.04*self.height
                id:boxEq
                orientation:'vertical'
                size_hint_y:None
                height:self.minimum_height
        ActionBar:
            ActionView:
                ActionPrevious:
                    title:'Lista de Equipamentos'
                    on_release:app.root.current = 'menu'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
<BotaoEquipamento>:
    size_hint_y:None
    height:150
    Button:
        id:botao_equipamento
        text:''
        on_press:
            app.root.get_screen('equipamentoIndividual').ids.titulo_equipamento_individual.title=self.text
            app.root.get_screen('inventario').ids.titulo_equipamento_inventário.title=self.text
            app.root.get_screen('selecao').ids.titulo_seleção.title=self.text
        on_release:app.root.current = 'selecao'

<TelaEquipamentoIndividual>:
    BoxLayout:
        orientation:'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                    id:titulo_equipamento_individual
                    title:""
                    on_release:app.root.current = 'selecao'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
        BoxLayout:
            orientation:'vertical'
            padding:0.05*self.width,0
            spacing : 0.04*self.height
            BoxLayout:
                orientation:'horizontal'
                Label:
                    text:'Ultima manutenção realizada em:'
                    font_size: 20
                Label:
                    text:''
                    id:data_ultima_os
                    font_size: 25
            BoxLayout:
                orientation:'horizontal'
                Label:
                    text:'Previsão de ocorrência de próxima falha:'
                    font_size: 20
                Label:
                    text:'ATUALIZANDO'
                    id:data_proxima_os
                    font_size: 25
            BoxLayout:
                orientation:'vertical'
                Label:
                    text:'Disponibilidade'
                    size_hint_y: None
                    size: self.texture_size
                Label:
                    id:valor_disponibilidade
                    text:'ATUALIZANDO'
                    font_size:25
            BoxLayout:
                orientation:'horizontal'
                BoxLayout:
                    orientation:'vertical'
                    Label:
                        text:'MTTR'
                        size_hint_y: None
                        size: self.texture_size
                    Label:
                        id:valor_mttr
                        text:'ATUALIZANDO'
                        font_size:25
                BoxLayout:
                    orientation:'vertical'
                    Label:
                        text:'MTBF'
                        size_hint_y: None
                        size: self.texture_size
                    Label:
                        id:valor_mtbf
                        text:'ATUALIZANDO'
                        font_size:25
            BoxLayout:
                orientation:'vertical'
                Button:
                    id:imagem
                    text:'ATUALIZANDO'
                    on_press:app.root.current='grafico'
                    font_size:22

<TelaGrafico>:
    BoxLayout:
        orientation:'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                    title:"Gráfico de Manutenção"
                    on_release:app.root.current = 'equipamentoIndividual'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
                ActionButton:
                    text:'Mudar Gráfico'
                    on_release:app.root.current='grafico2'
                ActionButton:
                    text:'Mês Anterior'
                    on_press:root.voltar()
                    on_press:root.on_leave()
                    on_release:app.root.get_screen('equipamentoIndividual').on_enter()
                    on_release:root.on_pre_enter()

                    on_release:
                ActionButton:
                    text:'Próximo Mês'
                    on_press:root.avançar()
                    on_press:root.on_leave()
                    on_release:app.root.get_screen('equipamentoIndividual').on_enter()
                    on_release:root.on_pre_enter()

        BoxLayout:
            orientation:'horizontal'
            id:imagem
<TelaGrafico2>:
    BoxLayout:
        orientation:'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                    title:"Gráfico de Manutenção"
                    on_release:app.root.current = 'equipamentoIndividual'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
                ActionButton:
                    text:'Mudar Gráfico'
                    on_release:app.root.current='grafico'
        BoxLayout:
            orientation:'horizontal'
            spacing : 0.04*self.height
            padding:0.05*self.width,0
            id:imagem2
<TelaEquipamentoInventario>:
    BoxLayout:
        orientation:'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                    id:titulo_equipamento_inventário
                    title:''
                    on_release:app.root.current = 'selecao'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
        BoxLayout:
            orientation:'vertical'
            padding:0.05*self.width,0
            spacing : 0.04*self.height
            BoxLayout:
                orientation:'horizontal'
                Label:
                    font_size:28
                    text:'Fornecedor'
                Label:
                    text:''
                    font_size:30
                    id:fornecedor
            BoxLayout:
                orientation:'horizontal'
                Label:
                    font_size:28
                    text:'Valor de Compra'
                BoxLayout:
                    orientation:'horizontal'
                    Label:
                        font_size:30
                        text:'R$'
                    Label:
                        text:''
                        font_size:30
                        id:valor_de_compra
            BoxLayout:
                orientation:'horizontal'
                Label:
                    font_size:28
                    text:'Valor com Depreciação'
                BoxLayout:
                    orientation:'horizontal'
                    Label:
                        font_size:30
                        text:'R$'
                    Label:
                        font_size:30
                        text:''
                        id:valor_atualizado
<SelecaoIndividual>:
    BoxLayout:
        orientation:'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                    id:titulo_seleção
                    title:''
                    on_release:app.root.current = 'listaEquipamento'
                ActionButton:
                    text:'Sair'
                    on_release:app.stop()
        BoxLayout:
            orientation:'vertical'
            padding:0.05*self.width,0
            spacing : 0.04*self.height
            BoxLayout:
                orientation:'vertical'
                Label:
                    text:''
                    size_hint_y:0.15
                Button:
                    text:'Indicadores'
                    on_release:app.root.current = 'equipamentoIndividual'
                    font_size:35
            BoxLayout:
                orientation:'vertical'
                Button:
                    text:'Informações de Inventário'
                    on_release:app.root.current = 'inventario'
                    font_size:35
                Label:
                    text:''
                    size_hint_y:0.15

""")

class Gerenciador(ScreenManager):
   pass


class TelaGrafico(Screen):
    def on_pre_enter(self):
        global mes_selecionado
        imagem=Image(source="gráfico.png",allow_stretch=True)
        imagem.reload()
        self.ids.imagem.add_widget(imagem)
    def on_leave(self):
         self.ids.imagem.clear_widgets()
    def avançar(self):
        global mes_selecionado
        mes_selecionado=mes_selecionado+1
        print(mes_selecionado)
    def voltar(self):
        global mes_selecionado
        mes_selecionado=mes_selecionado-1
        print(mes_selecionado)

class TelaGrafico2(Screen):
    def on_pre_enter(self):
        imagem2=Image(source='gráfico_mtbf.png',allow_stretch=True)
        imagem2.reload()
        self.ids.imagem2.add_widget(imagem2)
        imagem2.reload()
    def on_leave(self):
         self.ids.imagem2.clear_widgets()


class TelaMenu(Screen):
    pass


class CadastroOs(Screen):
    def on_pre_enter(self):
        tags_equipamentos=[]
        for indice in os.find({"tipo":"Equipamento"}):
            tags_equipamentos.append(f"{indice['tag']}:  {indice['nome']}")
        
        cOs=self.ids.box_tag
        titulo=Label(text='TAG de equipamento',font_size='20sp')
        self.tagOs=Spinner(text="Clique aqui",values=tags_equipamentos)
        cOs.add_widget(titulo)
        cOs.add_widget(self.tagOs)
    def on_leave(self):
        self.ids.box_tag.clear_widgets()
    def inicio(self):
        self.ids.confirmação.clear_widgets()
        self.ids.inicio.text=str(datetime.timestamp(datetime.now()))
        self.ids.confirmação.add_widget(Image(source='ampulheta.png',allow_stretch=True))
    def fim(self):
        self.ids.fim.text=str(datetime.timestamp(datetime.now()))
        
        tagEq=self.tagOs.text.split(':',1)
        
        dadosOS={
            'tag':tagEq[0],
            'Inicio':self.ids.inicio.text,
            'fim':self.ids.fim.text,
            'tipo':'OS',
        }
        return os.insert_one(dadosOS)

class CadastroOp(Screen):
    def on_pre_enter(self):
        tags_equipamentos=[]
        for indice in os.find({"tipo":"Equipamento"}):
            tags_equipamentos.append(f"{indice['tag']}:  {indice['nome']}")
        
        cOs=self.ids.box_tag
        titulo=Label(text='TAG de equipamento',font_size='20sp')
        self.tagOs=Spinner(text="Clique aqui",values=tags_equipamentos)
        cOs.add_widget(titulo)
        cOs.add_widget(self.tagOs)
    def on_leave(self):
        self.ids.box_tag.clear_widgets()
    def inicio(self):
        self.ids.confirmação.clear_widgets()
        self.ids.inicio.text=str(datetime.timestamp(datetime.now()))
        self.ids.confirmação.add_widget(Image(source='ampulheta.png',allow_stretch=True))
    def fim(self):
        self.ids.fim.text=str(datetime.timestamp(datetime.now()))
        
        tagEq=self.tagOs.text.split(':',1)
        
        dadosOP={
            'tag':tagEq[0],
            'Inicio':self.ids.inicio.text,
            'fim':self.ids.fim.text,
            'falha':0,
            'tipo':'OP',
        }
        return os.insert_one(dadosOP)

    def falha(self):
        self.ids.falha.text=str(datetime.timestamp(datetime.now()))

        tagEq=self.tagOs.text.split(':',1)
        
        dadosOP={
            'tag':tagEq[0],
            'Inicio':self.ids.inicio.text,
            'fim':self.ids.falha.text,
            'falha':1,
            'tipo':'OP',
        }
        return os.insert_one(dadosOP)
    def apagar(self):
        self.ids.falha.text=''
        self.ids.inicio.text=''
        self.ids.fim.text=''
        self.tagOs.text="Clique aqui"
        self.ids.confirmação.clear_widgets()

class TelaCadastroEquipamentos(Screen):
    def cadastro(self):
        nome=self.ids.nome.text
        tag=self.ids.TAG.text
        
        preço_de_compra=float(self.ids.preço_de_compra.text.replace(',','.'))
        fornecedor=self.ids.fornecedor.text
        
        dia=self.ids.dia_i_op.text
        mes=self.ids.mes_i_op.text
        ano=self.ids.ano_i_op.text
        inicio_op=data_usuario(dia,mes,ano,'9','0','0')

        anos_de_depreciação=int(self.ids.anos_de_depreciação.text)
        

        EQ={
            'nome':nome,
            'tag':tag,
            'preço_de_compra':preço_de_compra,
            'fornecedor':fornecedor,
            'tipo':'Equipamento',
            'data':inicio_op,
            'anos_de_depreciação':anos_de_depreciação,
        }
        return os.insert_one(EQ)

    def apagar (self):
        self.ids.nome.text=''
        self.ids.TAG.text=''
        self.ids.preço_de_compra.text='XXXX.XX'
        self.ids.dia_i_op.text='Dia'
        self.ids.mes_i_op.text='Mês'
        self.ids.ano_i_op.text=''
        self.ids.fornecedor.text=''
        self.ids.anos_de_depreciação.text=''


class BotaoEquipamento(BoxLayout):
    def __init__(self,text='',**kwargs):
        super().__init__(**kwargs)
        self.ids.botao_equipamento.text = text

class TelaListaEquipamentos(Screen):
    def on_pre_enter(self):
        for indice in os.find({'tipo':'Equipamento'}):
            self.ids.boxEq.add_widget(BotaoEquipamento(text=f"{indice['tag']}:  {indice['nome']}"))
    def on_leave(self):
        self.ids.boxEq.clear_widgets()

class TelaEquipamentoInventario(Screen):
    def on_pre_enter(self):
        nome=self.ids.titulo_equipamento_inventário.title
        tag=str(nome).split(':',1)
        equipamento=os.find_one({'tipo':'Equipamento','tag':tag[0]})
        
        self.ids.fornecedor.text=str(equipamento['fornecedor'])

        tempo_depreciação=float(equipamento['anos_de_depreciação'])*365*24*60*60
        inicio=float(equipamento['data'])
        preço_de_compra=float(equipamento['preço_de_compra'])
        self.ids.valor_de_compra.text=str(preço_de_compra)
        agora=float(datetime.timestamp(datetime.now()))

        preço_atual=round(preço_de_compra-((preço_de_compra/(tempo_depreciação))*(agora-inicio)))
        if preço_atual<0:
            preço_atual=0
        
        self.ids.valor_atualizado.text=str(preço_atual)

class SelecaoIndividual(Screen):
    pass

class TelaEquipamentoIndividual(Screen):
    def on_leave(self):
         self.ids.data_proxima_os.text='ATUALIZANDO'
         self.ids.valor_disponibilidade.text='ATUALIZANDO'
         self.ids.valor_mttr.text='ATUALIZANDO'
         self.ids.valor_mtbf.text='ATUALIZANDO'
         self.ids.imagem.text='ATUALIZANDO'
    def on_pre_enter(self):
        nome=self.ids.titulo_equipamento_individual.title
        tag=str(nome).split(':',1)
        for indice in os.find({'tipo':'OS','tag':str(tag[0])}):
                inicio_timestamp=indice['Inicio']
                inicio=datetime.fromtimestamp(inicio_timestamp)
                data_inicio=inicio.strftime("%d/%m/%Y")
        self.ids.data_ultima_os.text=data_inicio
        self.ids.imagem.text='ATUALIZANDO'

        try:
            rem.remove("gráfico.png")
            rem.remove('gráfico_mtbf.png')
        except:
            pass
    def on_enter(self):
        nome=self.ids.titulo_equipamento_individual.title
        tag=str(nome).split(':',1)
        tempo_parada=timedelta(hours=0)
        n_os=0
        marcação=[]
        data=[]
        tempo=[]
        valores=[]
        timestamp_om_i=[]
        timestamp_om_t=[]
        agora=datetime.now()
        equip_selecionado=os.find_one({'tipo':'Equipamento','tag':str(tag[0])})
        
        #SOMANDO DURAÇÃO DAS MANUTENÇÕES
        for indice in os.find({'tipo':'OS','tag':str(tag[0])}):
                inicio_timestamp=indice['Inicio']
                termino_timestamp=indice['fim']
                
                timestamp_om_i.append(int(inicio_timestamp))
                timestamp_om_t.append(int(termino_timestamp))
                
                inicio=datetime.fromtimestamp(inicio_timestamp)
                termino=datetime.fromtimestamp(termino_timestamp)

                data_inicio=inicio.strftime("%d/%m/%Y")

                duração=termino-inicio
                
                tempo_parada=tempo_parada+duração
                n_os=n_os+1
                #MARCAÇÃO DE TEMPO
                marcação.append(inicio)
                data_inicio=inicio.strftime("%d/%m/%Y")
                data.append(data_inicio)
                tempo.append(minutos_totais(duração))
        
        #SOMANDO DURAÇÃO DE OPERAÇÕES
        horas_rodadas=0
        for indice in os.find({'tipo':'OP','tag':str(tag[0])}):
            inicio_op=float(indice['Inicio'])
            fim_op=float(indice['fim'])
            horas_rodadas=horas_rodadas+((fim_op-inicio_op)/(60*60))

        #DATA DA ÚLTIMA MANUTENÇÃO REALIZADA
        self.ids.data_ultima_os.text=data_inicio

        #CÁLCULO DE MTBF
        MTBF=round((horas_rodadas-float(horas_totais(tempo_parada)))/n_os,2)
        self.ids.valor_mtbf.text=f'{MTBF} horas'

        #CÁLCULO DE MTTR
        valor_MTTR=tempo_parada/n_os
        valor_MTTR_separado=str(valor_MTTR).split(':',2)
        MTTR=round(float(horas_totais(valor_MTTR)),2)
        self.ids.valor_mttr.text=f'{valor_MTTR_separado[0]}h {valor_MTTR_separado[1]}min {valor_MTTR_separado[2]}s'
        
        #CÁLCULO DE DISPONIBILIDADE
        disponibilidade=round((float(MTBF)/(float(MTBF)+float(MTTR)))*100,2)
        self.ids.valor_disponibilidade.text=f'{disponibilidade}%'

        #PREVISÃO DE PRÓXIMA MANUTENÇÃO PREVENTIVA
        prev_mtbf=datetime.fromtimestamp(int(float(0.9*MTBF/8)*86400)+termino_timestamp)
        horas_conf_60=int((-1*MTBF)*(log(0.6))*60*60)
        if prev_mtbf<datetime.fromtimestamp(fim_op+horas_conf_60):
            prev_mtbf=datetime.fromtimestamp(fim_op+horas_conf_60)
        self.ids.data_proxima_os.text=prev_mtbf.strftime("%d/%m/%Y")

        #ORGANIZAÇÃO DE DATAS DE MANUTENÇÕES
        for i in range(len(tempo)):
            valores.append([marcação[i],data[i],tempo[i]])
        valores_ordenados=sorted(valores)

        #SEPARAÇÃO DE DATAS E DURAÇÕES NOS EIXOS DO GRÁFICO
        eixo_x=[]
        eixo_y=[]
        for i in range(len(tempo)):
                data_inteira=str(valores_ordenados[i][1])
                data_separada=data_inteira.split('/')
                data_revisada=data_separada[0]+'/'+data_separada[1]
                eixo_x.append(data_revisada)
                eixo_y.append(valores_ordenados[i][2])

        #SEPARAR POR MÊS
        meses=[[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12]]
        for i in range(len(eixo_x)):
            mes=eixo_x[i].split('/')
            for j in range(len(meses)):
                if meses[j][0]==int(mes[1]):
                    meses[j].append([eixo_x[i],eixo_y[i]])

        #DEFINIÇÃO DE EIXOS DOS GRÁFICOS
        eixo_x_real=[]
        eixo_y_real=[]
        global mes_selecionado
        for i in range(len(meses[mes_selecionado])-1):
            eixo_x_real.append(meses[mes_selecionado][i+1][0])
            eixo_y_real.append(meses[mes_selecionado][i+1][1])
            

        #PLOTAGEM DO GRÁFICO DE HISTÓRICO DE MANUTENÇÕES        
        fig, ax = plt.subplots()
        ax.bar(eixo_x_real, eixo_y_real,color='red')
        ax.set(xlabel='Data de Manutenção Corretiva (2022)', ylabel='Duração da manutenção (min)',
            title=f'Duração de OMs da{tag[1]}')
        for tick in ax.get_xticklabels():
            tick.set_rotation(50)
        #SALVANDO IMAGEM DO GRÁFICO DE HISTÓRICO DE MANUTENÇÕES
        fig.savefig("gráfico.png")

        #DECLARAÇÃO DE VARIÁVEIS PARA GRÁFICO DE VARIAÇÃO DE MTBF
        dias_mtbf_movel=[equip_selecionado['data']]
        tempo_parada_movel=[]
        n_parada_movel=[]
        om=0
        #DETERMINAÇÃO DO VETOR DE DIAS DE VERIFICAÇÃO DO MTBF 'dias_mtbf_movel'
        while dias_mtbf_movel[len(dias_mtbf_movel)-1]<datetime.timestamp(agora):
            dias_mtbf_movel.append(dias_mtbf_movel[len(dias_mtbf_movel)-1]+(30*24*60*60))

        for j in dias_mtbf_movel:
            om_real=0
            duração_movel_real=timedelta(hours=0)
            for i in range(len(timestamp_om_i)):
                if timestamp_om_i[i]<=j:
                    a=datetime.fromtimestamp(timestamp_om_i[i])
                    b=datetime.fromtimestamp(timestamp_om_t[i])
                    duração_movel_real=duração_movel_real+b-a
                    om_real=om_real+1
            tempo_parada_movel.append(duração_movel_real)
            n_parada_movel.append(om_real)

        #QUANTIDADE DE TEMPO DA PROGRESSÃO DO MTBF
        tempo_op_movel=[]
        for i in range(len(dias_mtbf_movel)):
            acumulo=0
            operação=os.find({'tipo':'OP','tag':str(tag[0])})
            final_operação=[]
            inicio_operação=[]

            for j in operação:
                final_operação.append(j['fim'])
                inicio_operação.append(j['Inicio'])
            for k in range(len(final_operação)):
                if float(final_operação[k])<float(dias_mtbf_movel[i]):
                    acumulo=acumulo+((float(final_operação[k])-float(inicio_operação[k]))/(60*60))
            
            tempo_op_movel.append(acumulo)
        
        #CÁLCULO MTBF MÓVEL
        mtbf_movel=[]
        for i in range(len(tempo_op_movel)):
            try:
                valor_mtbf_movel=(float(tempo_op_movel[i])-float(horas_totais(tempo_parada_movel[i])))/n_parada_movel[i]
            except:
                valor_mtbf_movel=0
            dia_mtbf_datetime=datetime.fromtimestamp(dias_mtbf_movel[i])
            dia_mtbf=dia_mtbf_datetime.strftime("%d/%m")
            
            mtbf_movel.append([valor_mtbf_movel,dia_mtbf])
        
        #PLOTAGEM DO GRÁFICO DE PROGRESSÃO DO MTBF
        eixo_i=[]
        eixo_j=[]
        for i in range(len(mtbf_movel)):
            eixo_i.append(mtbf_movel[i][1])
            eixo_j.append(mtbf_movel[i][0])
        
        fig, bx = plt.subplots()
        bx.bar(eixo_i, eixo_j)

        bx.set(xlabel='Data de Verificação (2022)', ylabel='Valor de MTBF (horas)',
            title=f'Progressão do MTBF de {tag[1]}')

        fig.savefig("gráfico_mtbf.png")

        #ATUALIZAÇÃO DO BOTÃO DE VIZUALIZAÇÃO DE GRÁFICOS
        self.ids.imagem.text='Ver Gráfico'
            

class NMK_ManutençãoApp(App):
    def build(self):
        return Gerenciador()
        
if __name__ == '__main__':
    NMK_ManutençãoApp().run()
