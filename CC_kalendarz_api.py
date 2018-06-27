#kalendarz
#http://www.coincalendar.info/api-documentation/
#https://api.coinmarketcal.com/
#https://coindar.org/en/api

#get data from api coindar.org
#https://coindar.org/api/v1/events?Year=2017&Month=10

import CC_get_app_patch
application_path = CC_get_app_patch.pobierz_app_patch()

import time
import datetime

import requests
import re

import wx
import wx.html2

import operator


class MyHtmlFrame(wx.Panel):
    
    def __init__(self, parent):
        wx.Panel.__init__ ( self, parent, id = wx.ID_ANY, pos = wx.DefaultPosition, size = wx.Size( 300,120 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL,  )

        self.html_view = wx.html2.WebView.New(self)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html_view, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.wyswietlanie() 

    def get_data(self):
        coindar_events_up_to_date = []
        r = requests.get(url='https://coindar.org/api/v1/lastEvents')
        coindar_events = r.json()
        now = datetime.datetime.now()
        
        
        for event in coindar_events:
            #time.sleep(0.5)
            coindar_caption = event['caption']
            coindar_proof = event['proof']
            coindar_public_date = event['public_date']
            coindar_start_date = event['start_date']
            coindar_end_date = event['end_date']
            coindar_coin_name = event['coin_name']
            coindar_coin_symbol = event['coin_symbol']
            
            #print(coindar_start_date)
            start = coindar_start_date
            podzielone = start.split('-')
            #print(podzielone)

            #dodanie dnia jezeli nie istnieje
            if len(podzielone) == 2:
                podzielone.append('00')

            rok = podzielone[0]
            miesiac = podzielone[1]
            dzien = podzielone[2]
            dzien = dzien[0:2]

            if len(miesiac) == 1:
                miesiac = '0'+miesiac

            sorter = int(rok+miesiac+dzien)
            
            miesiac = int(miesiac)
            rok = int(rok)

            if rok >= now.year and miesiac >= now.month:
                if int(str(sorter)[-2:]) >= now.day or str(sorter)[-2:]=='00':

                    event = {
                        'wydarzenie':coindar_caption,
                        'start':coindar_start_date,
                        'koniec':coindar_end_date,
                        'coin':coindar_coin_name,
                        'coin_symbol':coindar_coin_symbol,
                        'sorter':sorter              
                        }
                    coindar_events_up_to_date.append(event)

        coindar_events_up_to_date.sort(key=operator.itemgetter('sorter'))

        print('koniec ')
        #print(coindar_events_up_to_date)
        return coindar_events_up_to_date


    def wyswietlanie(self):
        html = wx.html2.WebView.New(self)
        if "gtk2" in wx.PlatformInfo:
            html.SetStandardFonts()
        coindar_events_up_to_date = self.get_data()
        
        source1 = ''
        source3 = ''
        for event in coindar_events_up_to_date:
            #print(event)
            wydarzenie = event['wydarzenie']
            start = event['start']
            koniec = event['koniec']
            
            if koniec == '':
                pass
            else:
                koniec = 'koniec: ' + str(koniec)

            coin = event['coin']
            coin_symbol = event['coin_symbol']

            from pathlib import Path


            image = Path(u''+application_path+ '/cryptoicons128/'+coin_symbol.lower()+'.png')
            if image.is_file():
                image = u''+application_path+ '/cryptoicons128/'+coin_symbol.lower()+'.png'
            else:
                image = u''+application_path+ '/cryptoicons128/icci_kolo_160.png'

            sorter = str(event['sorter'])
            #print(sorter)
            #print('sorter [0:2]',sorter[0:6])
            last_2_sorter = sorter[6:8]

            #if last_2_sorter != '00':
            source = '<hr /><p>&nbsp;</p><table style="height: 169px; margin-left: auto; margin-right: auto; width: 603px;"><tbody><tr><td style="width: 143px; text-align: center;"><img src="'+ image +'" alt="" width="128" height="128" /></td><td style="width: 446px;"><h2 style="text-align: center;"><span style="color: #0000ff;"><strong>' + coin + '</strong></span>&nbsp;<span style="color: #0000ff;">' + coin_symbol + '</span></h2><h1 style="text-align: center;"><span style="color: #00ff00;"><strong>' + wydarzenie + '</strong></span></h1><h2 style="text-align: center;"><span style="color: #ffcc00;">' + start + koniec + '</span></h2></td></tr></tbody></table>'

            #print(source)

            source1 += source


        source_html = source1
        self.html_view.SetPage(source_html, "")
            



if __name__ == '__main__':
    app = wx.App()

    frame = MyHtmlFrame(None)
    frame.Show()
    app.MainLoop()


