'''
GatunMap 
> wywietlać informację o sprawdzeniu aktualizacji bazy (pobranie nowych dancyh taksonomicznych i występowania ) z GBIFu
'''
import wx
from pygbif import species as species

#wybór rangi
ranga=''
zmienna = 0
def zaznaczenieradia(evt):
    global ranga
    global zmienna
    for i in range(len(lista_radio)):
        if lista_radio[i].GetValue():
            ranga=lista_rang[i]
            zmienna=i

#wybór z wyszukiwarki (aktualizacja, wyszukaj, wybor)
def aktualizacja(evt):
    #pobranie wartosci z wyszukiwarka1
    tempkrolestwa=[]
    wartosc=wyszukiwarka1.GetValue()
    for animal in lista_list[zmienna]:
        if wartosc in animal:
            tempkrolestwa.append(animal)
    Organization.Clear()
    Organization.InsertItems(tempkrolestwa,0)

def Wyszukaj(evt):
    okno=wx.Frame(Okno1, title="Wyszukiwanie", size=(500,500)) #Nowe okno po uzyciu przycisku
    panel=wx.Panel(okno,size=(500,500))
    okno.Center()
    okno.Show()

def Wybor(evt):
    wybor=Organization.GetSelection()
    wybor=Organization.GetString(wybor)
    wyszukiwarka1.SetValue(wybor)
   

#wyszukiwanie po wspolrzednych



app=wx.App()

#podstawowe okno aplikacji
Okno1=wx.Frame(None, wx.ID_ANY, title="GatunMap", size=(800,600), style=wx.CAPTION | wx.CLOSE_BOX)
Okno1.Center()
Panel=wx.Panel(Okno1, size=(800,600))


#POZIOM ORGANIZACJI 
#panel wyboru poziomu organizacji 
obramowanie=wx.Panel(Panel, pos=(30,80), size=(100,200)) #Stworzenie obramowania do radiobutton (można dodać styl)
obramowanie.SetBackgroundColour((250,250,250))

poziom_organizacji=wx.StaticText(Panel, label="Wybierz poziom organizacji:", pos=(40,60))
krolestwo = wx.RadioButton(obramowanie, label='Królestwo', pos=(15,15))
gromada = wx.RadioButton(obramowanie, label= 'Gromada', pos=(15,35))
klasa = wx.RadioButton(obramowanie, label= 'Klasa', pos=(15,55))
rzad = wx.RadioButton(obramowanie, label= 'Rząd', pos=(15,75))
rodzina = wx.RadioButton(obramowanie, label= 'Rodzina', pos=(15,95))
rodzaj = wx.RadioButton(obramowanie, label= 'Rodzaj', pos=(15,115))
gatunek = wx.RadioButton(obramowanie, label= 'Gatunek', pos=(15,135))

lista_radio = [krolestwo, gromada, klasa, rzad, rodzina, rodzaj, gatunek]
lista_rang = ["kingdom","phylum","class","order","family","genus","species"]


#wybieranie rangi do wyszukiwania
obramowanie.Bind(wx.EVT_RADIOBUTTON, zaznaczenieradia) #Przypisanie funkcji do przycisku


#WYSZUKIWANIE WPISYWANIE/DCLICK
#Listbox 
Organization=wx.ListBox(Panel, pos=(300,80), size=(200,300))
przycisk_wyszukaj=wx.StaticText(Panel, label="Wyszukaj", pos=(300,63))

#Okno do ktorego sie wpisuje wyszukiwanie
wyszukiwarka1=wx.TextCtrl(Panel,pos=(300,40), size=(200,20))

#Lista do wsadzenia do wyszukiwarki
kingdom_list=[]
phylum_list =[]
class_list =[]
order_list =[]
family_list =[]
genus_list =[]
species_list =[]
lista_list = [kingdom_list, phylum_list, class_list, order_list, family_list, genus_list, species_list] 

dict_result={} # tutaj sa dict dla kazdego z rang
for i in range(len(lista_rang)):
    for rangi in lista_rang:
        dict_all = species.name_lookup(rank=str(rangi))
        dict_result[rangi] = dict_all['results']
    
for i in range(len(dict_result)):
    for x in dict_result[lista_rang[i]]:
        rang_name = str(lista_rang[i])
        if rang_name in x: 
            if x[rang_name] not in lista_list[i]:
                lista_list[i].append(x[rang_name])

del(dict_all) #usuwa te glowne slowniki

tempkrolestwa=[]

Organization.InsertItems(lista_list[zmienna],0)
Organization.Bind(wx.EVT_LISTBOX_DCLICK, Wybor) #zrobienie eventu od podowjnego klikniecia w liscie


#Przypisanie, że jakas funkcja sie dzieje jak sie wpisuje w wyszukiwarka1
wyszukiwarka1.Bind(wx.EVT_KEY_UP, aktualizacja)


#PRZYCISK WYSZUKIWANIA
wyszukaj=wx.Button(Panel, wx.ID_ANY, "Wyszukaj", pos=(700,525)) #Zmiana pozycji przycisku itp
Okno1.Bind(wx.EVT_BUTTON, Wyszukaj, wyszukaj) #Przypisanie funkcji do przycisku




#moje testy
species.name_backbone(name='Poa', rank=ranga)
        
#AUTORZY
autorzy = wx.StaticText(Panel, label="Autorzy: Julia Denkewicz & Ada Ryszka", pos=(10,530))
font1 = wx.Font(10, wx.SWISS, wx.ITALIC, wx.NORMAL)
autorzy.SetFont(font1)
Okno1.Show()


#Okna dialogowe (do dalszych kroków)
# warning dialog
wx.MessageBox('Zapytanie nie mogło zostać zrealizowane', 'Warning', wx.OK | wx.ICON_WARNING)

# error dialog
wx.MessageBox('Operation could not be completed', 'Error', wx.OK | wx.ICON_ERROR)

app.MainLoop()

#Mamy pierwszego listboxa zrobić do wyboru poziomu taksonomicznego (Królestwo, gromada, klasa, rząd, rodzina, rodzaj)
#Drugi listbox ma uzwględniając wybór poziomu wywietlić listę organizmów (z możliwoscią wyszakania ich wpisując nazwy)

