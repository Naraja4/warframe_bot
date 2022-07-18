from asyncio import tasks
import requests
import urllib3, discord, json
from discord.ext import tasks

urllib3.disable_warnings()

#discord bot token
TOKEN = ''

def requestShellShockData():
    URL='https://api.warframe.market/v1/items/shell_shock/orders'
    response=requests.get(URL, verify=False)
    return response.json()

def requestRelicsData(type):
   URL="https://api.warframestat.us/items/search/"+type
   response=requests.get(URL, verify=False)
   return response.json()

def requestRelicsDrop(type):
   URL="https://api.warframestat.us/drops/search/"+type
   response=requests.get(URL, verify=False)
   return response.json()

def requestItemDrop(type):
   URL="https://api.warframestat.us/drops/search/"+type
   response=requests.get(URL, verify=False)
   return response.json()

def requestfissureData():
    URL='https://api.warframestat.us/pc/fissures'
    response=requests.get(URL, verify=False)
    return response.json()

def reliclist(type):
    axiList=requestRelicsData(type)
    axisListdef=[]
    j=0
    for i in range(len(axiList)):
        
        if axiList[i]['category']=='Relics':
            j+=1
            if j==4:
                t=axiList[i]['name']
                t=t.removesuffix(' Radiant')
                axisListdef.append(t)
                j=0
    
    return axisListdef

def NOTvaulted(type):
    notvaultedrelics=requestRelicsDrop(type)
    notvaultedrelicsdef=[]

    for i in range(len(notvaultedrelics)):
        
        t=notvaultedrelics[i]['item']

        if type=='meso' or type=='lith':
            parameter=4
        else:
            parameter=3

        if t[0:parameter]==type.capitalize():
            t=t.removesuffix(' (Radiant)')
            t=t.removesuffix(' Relic')
            if t not in notvaultedrelicsdef:
                notvaultedrelicsdef.append(t)
    
    return notvaultedrelicsdef

def RelicLocation(relic,type):
    notvaultedrelics=requestRelicsDrop(type)
    locations=[]
    chances=[]

    for i in range(len(notvaultedrelics)):
        
        if notvaultedrelics[i]['item']==relic:
            locations.append(notvaultedrelics[i]['place'])
            chances.append(notvaultedrelics[i]['chance'])
    
    return locations, chances

def ItemLocation(type):
    items=requestItemDrop(type)
    locations=[]
    chances=[]

    for i in range(len(items)):
        
            locations.append(items[i]['place'])
            chances.append(items[i]['chance'])
    
    return locations, chances

def IsItemVaulted(type):

    locations,chances=ItemLocation(type)
    relics=NOTvaulted('lith')
    relics+=NOTvaulted('meso')
    relics+=NOTvaulted('neo')
    relics+=NOTvaulted('axi')

    for i in range(len(locations)):
        t=locations[i]
        if t.endswith(' Relic'):
              t = t[:-6]
        if t in relics:
            return False
    
    return True


def IsVaulted(relic,type):
    notvaulted=NOTvaulted(type)
    if relic in notvaulted:
        return False
    else:  
        return True


client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    channel=message.channel
    if message.content.startswith('lith'):
        await channel.send(' | '.join(NOTvaulted(message.content)))
    if message.content.startswith('meso'):
        await channel.send(' | '.join(NOTvaulted(message.content)))
    if message.content.startswith('neo'):
        await channel.send(' | '.join(NOTvaulted(message.content)))
    if message.content.startswith('axi'):
        await channel.send(' | '.join(NOTvaulted(message.content)))

    if message.content.startswith('all lith'):
        await channel.send(' | '.join(reliclist(message.content[4:])))
    if message.content.startswith('all meso'):
        await channel.send(' | '.join(reliclist(message.content[4:])))
    if message.content.startswith('all neo'):
        await channel.send(' | '.join(reliclist(message.content[4:])))
    if message.content.startswith('all axi'):
        await channel.send(' | '.join(reliclist(message.content[4:])))
    
    if message.content[:1]=='v':
        relic=message.content[2:]
        relic=relic.capitalize()

        if relic[0]=='L':
            relic='Lith '+ relic[2:].capitalize()
            result=IsVaulted(relic,'lith')
        
        if relic[0]=='M':
            relic='Meso '+ relic[2:].capitalize()
            result=IsVaulted(relic,'meso')
        
        if relic[0]=='N':
            relic='Neo '+ relic[2:].capitalize()
            result=IsVaulted(relic,'neo')
        
        if relic[0]=='A':
            relic='Axi '+ relic[2:].capitalize()
            result=IsVaulted(relic,'axi')
        
        if result==False:
            await channel.send('NOT vaulted')
        else:
            await channel.send('Vaulted')
    
    if message.content[:1]=='w':
        relic=message.content[2:]
        relic=relic.capitalize()
        t=''

        if relic[0]=='L':
            relic='Lith '+ relic[2:].capitalize()+' Relic'
            location,chance=RelicLocation(relic,'lith')
        
        elif relic[0]=='M':
            relic='Meso '+ relic[2:].capitalize()+' Relic'
            location,chance=RelicLocation(relic,'meso')
        
        elif relic[0]=='N':
            relic='Neo '+ relic[2:].capitalize()+' Relic'
            location,chance=RelicLocation(relic,'neo')
        
        elif relic[0]=='A':
            relic='Axi '+ relic[2:].capitalize()+' Relic'
            location,chance=RelicLocation(relic,'axi')
        
        for i in range(len(location)):
            string=location[i]+' | '+str(chance[i])+'%\n'

            if len(t)<1900:
                t+=string
            else:   
                await channel.send(t)
                t=''
        
        await channel.send(t)
    
    if message.content[:1]=='f':
        relic=message.content[2:]
        t=''

        location,chance=ItemLocation(relic)
            
        for i in range(len(location)):
            string=location[i]+' | '+str(chance[i])+'%\n'

            if len(t)<1900:
                t+=string
            else:   
                await channel.send(t)
                t=''
        
        await channel.send(t)
    
    if message.content[:1]=='i':
        relic=message.content[2:]

        result=IsItemVaulted(relic)
            
        if result==False:
            await channel.send('NOT vaulted')
        else:
            await channel.send('Vaulted')

@tasks.loop(seconds=10)
async def fissure():
    with open('fisuras.json', "rb") as f: 
        data = json.load(f)
    
    channel = await client.fetch_channel(981292041529073700)
    t=requestfissureData()
    temp=[]

    for i in range(len(t)):
        temp.append(t[i]['nodeKey'])
        if t[i]['nodeKey'] not in data:
            if t[i]['missionKey']=='Disruption' and t[i]['isStorm']==False:
                msg='Hay una disrupción **'+t[i]['tier']+'**.'+' Termina en: **'+t[i]['eta']+'**.'
                await channel.send(msg)
                data.append(t[i]['nodeKey'])
                with open("fisuras.json", "w") as jsonFile:
                    json.dump(data,jsonFile)

            elif t[i]['missionKey']=='Capture' and t[i]['isStorm']==False:
                msg='Hay una captura **'+t[i]['tier']+'** en **'+t[i]['nodeKey']+'**.'+' Termina en: **'+t[i]['eta']+'**.'
                await channel.send(msg)
                data.append(t[i]['nodeKey'])
                with open("fisuras.json", "w") as jsonFile:
                    json.dump(data,jsonFile)

            elif t[i]['missionKey']=='Extermination' and t[i]['isStorm']==False:
                msg='Hay un exterminio **'+t[i]['tier']+'** en **'+t[i]['nodeKey']+'**.'+' Termina en: **'+t[i]['eta']+'**.'
                await channel.send(msg)
                data.append(t[i]['nodeKey'])
                with open("fisuras.json", "w") as jsonFile:
                    json.dump(data,jsonFile)
    
    for node in data:
        if node not in temp:
            msg='La fisura **'+node+'** ha terminado.'
            await channel.send(msg)
            data.remove(node)
            with open("fisuras.json", "w") as jsonFile:
                json.dump(data,jsonFile)


fissure.start()
        

client.run(TOKEN)