# -*- coding: utf-8 -*-
import HTMLParser,xbmcaddon,os,xbmc,xbmcgui,urllib,urllib2,re,xbmcplugin,sys,logging,json
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
__addon__ = xbmcaddon.Addon()
__cwd__ = xbmc.translatePath(__addon__.getAddonInfo('path')).decode("utf-8")
Addon = xbmcaddon.Addon()
user_dataDir = xbmc.translatePath(Addon.getAddonInfo("profile")).decode("utf-8")
import cache
if not os.path.exists(user_dataDir):
     os.makedirs(user_dataDir)

html_parser = HTMLParser.HTMLParser()

def get_params():
        param=[]
        if len(sys.argv)>=2:
          paramstring=sys.argv[2]
          if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param     

def addNolink( name, url,mode,isFolder, iconimage="DefaultFolder.png"):
 

          
          name='[COLOR aqua][I]'+name+'[/I][/COLOR]'
          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name)   })

          liz.setProperty("IsPlayable","false")
          liz.setProperty( "Fanart_Image", iconimage )
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)
###############################################################################################################        

def addDir3(name,url,mode,iconimage,fanart,description):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+urllib.quote_plus(description)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": description } )
        liz.setProperty( "Fanart_Image", fanart )
        art = {}
        art.update({'poster': iconimage})
        liz.setArt(art)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        
        return ok



def addLink( name, url,mode,isFolder, iconimage,fanart,description,data=''):

          u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+(name)+"&data="+str(data)+"&iconimage="+urllib.quote_plus(iconimage)+"&fanart="+urllib.quote_plus(fanart)+"&description="+(description)
 

          
         
         
          #u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
          liz = xbmcgui.ListItem( name, iconImage=iconimage, thumbnailImage=iconimage)

          liz.setInfo(type="Video", infoLabels={ "Title": urllib.unquote( name), "Plot": description   })
          art = {}
          art.update({'poster': iconimage})
          liz.setArt(art)
          liz.setProperty("IsPlayable","true")
          liz.setProperty( "Fanart_Image", fanart )
          
          xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz,isFolder=isFolder)


def read_site_html(url_link,cookies={}):
    import requests
    '''
    req = urllib2.Request(url_link)
    req.add_header('User-agent',__USERAGENT__)# 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30')
    html = urllib2.urlopen(req).read()
    '''
    headers = {

    'User-Agent': 'MOVIX-KODI',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    }
    html=requests.get(url_link,headers=headers,cookies=cookies)
    return html.content
def replace_all_names(name):
    na=name.replace('Home','ראשי').replace('Action','פעולה').replace('Comedy','קומדיה').replace('Crime','פשע').replace('Drama','דרמה').replace('Mystery','מיסטורין').replace('Thriller','מותחן')
    na=na.replace('From. Fiction','מדע בדיוני').replace('Horror','אימה').replace('Animation','אנימציה').replace('Fantasy','פנטסיה').replace('War','מלחמה').replace('Documentary','דוקומנטרי').replace('Family','משפחה').replace('Kids','ילדים').replace('Most Viewed','הנצפים ביותר').replace('Movies','סרטים').replace('Series','סדרות')
    return na
def main_menu():
   
    if len(Addon.getSetting("username"))>0:
      cookie_member,ok=cache.get(testlogin,12,'real', table='id')
      if ok:
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Movix', 'ברוך הבא לקוח פרימיום'.decode('utf8'))).encode('utf-8'))
      else:
        xbmc.executebuiltin((u'Notification(%s,%s)' % ('Movix', 'כשלון בהתחברות!! בדוק פרטי חשבון'.decode('utf8'))).encode('utf-8'))
        cache.clear(['id'])
    html=read_site_html('http://movix.live/')
    regex='a href="(.+?)">(.+?)</a></li>'
    match=re.compile(regex).findall(html)
    all_img=[u'https://wsdg.com/wp-content/uploads/casa-cor-home-cinema-2009-3.jpg', u'http://www.movies-site.com/wp-content/uploads/2013/04/gi-joe-retaliation.jpeg', u'https://www.pitria.com/wp-content/uploads/2015/08/170.jpg?x27391', u'http://images.huffingtonpost.com/2015-11-18-1447856895-9700-gang.png', u'http://2.bp.blogspot.com/__J1uTFOVfZY/TRPuGg4iN_I/AAAAAAAAA58/572xDBA2q2E/s1600/gif_9_drama_masks.gif', u'http://www.jugrnaut.com/wp-content/uploads/mysterybox.jpg', u'http://www.billboard.com/files/media/Michael-Jackson-Thriller-3d-promo-billboard-1548.jpg', u'http://www.brostrick.com/wp-content/uploads/2017/02/best-quotes-from-pulp-fiction-gifs-scenes.jpg', u'https://www.hdwallpaper.nu/wp-content/uploads/2015/06/3D-skull-horror-wallpaper-2560x1600.jpg', u'https://s3.amazonaws.com/university-prod/uploads/attachments/354/original/motion.png?1444883111', u'http://www.publicdomainpictures.net/pictures/190000/velka/fantasy-landschaft-1471278439FaB.jpg', u'https://prod01-cdn04.cdn.firstlook.org/wp-uploads/sites/1/2017/05/Korean-war-mehdi-hasan-1493757632-feature-hero.jpg', u'https://i.ytimg.com/vi/f6ZmXM6ZT0c/hqdefault.jpg', u'http://www.onefamily.ie/wp-content/uploads/bulgarian-imge.jpg', u'http://www.brisbanekids.com.au/wp-content/uploads/2013/06/KidsBrush.jpg', u'https://www.outerplaces.com/images/user_upload/imdb-chart.jpg', u'https://raw.githubusercontent.com/DanielHadley/YouTubeNotMusic/master/YouTube.png', u'http://image.tmdb.org/t/p/original/fQHP3rzL8QYROBq8RHsCaLul51M.jpg', u'https://www.youthareawesome.com/wp-content/uploads/2015/05/Wholly-icons-wallpaper-twilight-series-2849585-1280-800.jpg']
    import requests
    headers = {

    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    }
    i=0
    for link,name in match:
     
      name=replace_all_names(name)
      if len(all_img)>i:
        f_img=all_img[i]
      else:
        f_img=' '
      i=i+1
      if 'ראשי' not in name:
        addDir3(name,link,2,f_img,f_img,name)
    
    addDir3('[COLOR aqua][I]חיפוש[/I][/COLOR]','www',5,' ',' ','חיפוש')
def search():
    search_entered =''
    keyboard = xbmc.Keyboard(search_entered, 'הכנס מילות חיפוש כאן')
    keyboard.doModal()
    if keyboard.isConfirmed():
           search_entered = keyboard.getText()
           
    else:
      sys.exit()
    url='http://movix.live/?s='+search_entered
    html=read_site_html(url)
    regex_pre='<div data-movie-id="(.+?)<span></span></a>'
    match_pre=re.compile(regex_pre,re.DOTALL).findall(html)
    for items in match_pre:
        regex='a href="(.+?)".+?img data-original="(.+?)".+?h2>(.+?)<.+?<p>(.+?)</p>'
        match=re.compile(regex,re.DOTALL).findall(items)
        regex_q='"mli-quality">(.+?)<'
        match_q=re.compile(regex_q).findall(items)
        if len(match_q)>0:
           quality=match_q[0]
        else:
           quality=' '
        for link,image,name,plot in match:
          if 'series' in url or 'series' in items.lower():
            addDir3( name, link,4, image,image,'[COLOR aqua]'+quality+'[/COLOR]\n'+html_parser.unescape(plot.decode('utf-8')).encode('utf-8'))
          else:
            addLink( name, link,3,False, image,image,'[COLOR aqua]'+quality+'[/COLOR]\n'+html_parser.unescape(plot.decode('utf-8')).encode('utf-8'))
    regex="<li class='active'>.+?<a rel='nofollow' class='page larger' href='(.+?)'"
    match=re.compile(regex).findall(html)
    if len(match)>0:
        addDir3('[COLOR aqua]עמוד הבא[/COLOR]',match[0],2,' ',' ','עמוד הבא')
def scrape_site(url):
    html=read_site_html(url)
    regex_pre='<div data-movie-id="(.+?)<span></span></a>'
    match_pre=re.compile(regex_pre,re.DOTALL).findall(html)
    for items in match_pre:
        regex='a href="(.+?)".+?img data-original="(.+?)".+?"qtip-title">(.+?)<.+?<p>(.+?)</p>'
        match=re.compile(regex,re.DOTALL).findall(items)
        regex_q='"mli-quality">(.+?)<'
        match_q=re.compile(regex_q).findall(items)
        if len(match_q)>0:
           quality=match_q[0]
        else:
           quality=' '
        for link,image,name,plot in match:
          if 'series' in url or 'סדרות' in url:
            addDir3( name, link,4, image,image,'[COLOR aqua]'+quality+'[/COLOR]\n'+html_parser.unescape(plot.decode('utf-8')).encode('utf-8'))
          else:
            addLink( name, link,3,False, image,image,'[COLOR aqua]'+quality+'[/COLOR]\n'+html_parser.unescape(plot.decode('utf-8')).encode('utf-8'))
    regex="<li class='active'>.+?<a rel='nofollow' class='page larger' href='(.+?)'"
    match=re.compile(regex).findall(html)
    if len(match)>0:
        addDir3('[COLOR aqua]עמוד הבא[/COLOR]',match[0],2,' ',' ','עמוד הבא')
def get_episodes(name,url,image,plot):
    html=read_site_html(url)
    regex_pre='<div class="tvseason">.+?<strong>(.+?)</strong>(.+?)</ul>'
    match_pre=re.compile(regex_pre,re.DOTALL).findall(html)
    for title,items in match_pre:
        addNolink( title, 'www',99,False, iconimage="DefaultFolder.png")
        regex='<a href="(.+?)">(.+?)</'
        match=re.compile(regex,re.DOTALL).findall(items)
        for link,names in match:
            addLink( names.replace('\n',''), link,3,False, image,image,plot)
def fix_q(quality):
    f_q=100
    if '2160' in quality:
      f_q=1
    if '1080' in quality:
      f_q=2
    elif '720' in quality:
      f_q=3
    elif '480' in quality:
      f_q=4
    elif 'hd' in quality.lower() or 'hq' in quality.lower():
      f_q=5
    elif '360' in quality or 'sd' in quality.lower():
      f_q=6
    elif '240' in quality:
      f_q=7
    return f_q

def play(name,url,image,plot):
    import resolveurl
    cookie_member={}
    if len(Addon.getSetting("username"))>0:
      cookie_member,ok=cache.get(testlogin,12,'real', table='id')
      logging.warning(cookie_member)
    html=read_site_html(url,cookies=(cookie_member))
   
    regex='div id="tab(.+?)".+?<iframe.+?src="(.+?)"'
    match=re.compile(regex,re.DOTALL).findall(html)
   
     
    all_links=[]
    all_names=[]
   
    all_t=[]
    for q_tab,links in match:
      regex='//(.+?)/'
      match_s=re.compile(regex).findall(links)[0]
      regex_q='div class="les-content"><a href="#tab%s">(.+?)<'%q_tab
      
      q_pre=re.compile(regex_q).findall(html)
      if len(q_pre)>0:
        q=q_pre[0]
      else:
        q='0'
      qu=fix_q(q)
      if 'youtube' in match_s:
        
        all_t.append(('[COLOR teal][I]טריילר[/I][/COLOR]',qu,q,links))
      else:
        
        all_t.append((match_s,qu,q,links))
      
      
    regex='<div class="btn-group btn-group-justified embed-selector">(.+?)<script>'
    match_in_pre=re.compile(regex,re.DOTALL).findall(html)
    for items in match_in_pre:
        regex_pre='a href="(.+?)".+?<span class="lnk lnk-dl">(.+?)</span'
        match_in=re.compile(regex_pre,re.DOTALL).findall(items)
        
        for links,q in match_in:
          regex='//(.+?)/'
          match_s=re.compile(regex).findall(links)[0]

          qu=fix_q(q)
          all_t.append((match_s,qu,q,links))
    if len(all_t)==0:
       xbmcgui.Dialog().ok('Movix', 'אין מקורות')
       sys.exit()
    if len(all_t)>1:
       all_t=sorted(all_t, key=lambda x: x[1], reverse=False)
       for match_s,qu,q,links in all_t:
         all_names.append(match_s+' - '+q)
         all_links.append(links)
       ret=xbmcgui.Dialog().select("בחר מקור", all_names)
       if ret!=-1:
         f_link=all_links[ret]
       else:
        sys.exit()
    else:
        f_link=all_t[0][3]
    if 'gounlimited' in f_link:
       x=read_site_html(f_link)
       regex="<script type='text/javascript'>(.+?)</script>"
       match=re.compile(regex,re.DOTALL).findall(x)
       from jsunpack import unpack
       holder = unpack(match[0])
       regex='sources.+?"(.+?)"'
       match=re.compile(regex).findall(holder)
       link=match[0]
    else:
    
       link =resolveurl.resolve(f_link)
    video_data={}
    video_data['title']=name
    video_data['icon']=image
    video_data['plot']=(plot)
    video_data[u'mpaa']=unicode('heb')
    listItem = xbmcgui.ListItem(video_data['title'], path=link) 
    listItem.setInfo(type='Video', infoLabels=video_data)


    listItem.setProperty('IsPlayable', 'true')
    ok=xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=listItem)
def testlogin(url):
    import requests

    
    logging.warning('start_login')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
        'Accept': '*/*',
        'Accept-Language': 'he,he-IL;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'http://movix.live/',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    
    x=requests.get('http://movix.live/',headers=headers).content
    regex='name="register-security" value="(.+?)"'
    sec=re.compile(regex).findall(x)[0]
    data = [
      ('pt_user_login', Addon.getSetting("username")),
      ('pt_user_pass', Addon.getSetting("Password_sdr")),
      ('action', 'pt_login_member'),
      ('login-security', sec),
      ('_wp_http_referer', '/'),
    ]

    response = requests.post('http://movix.live/wp-admin/admin-ajax.php', headers=headers,  data=data)
    ok=True
    if url=='test':
        if 'Login successful' in response.content:
            xbmcgui.Dialog().ok('Movix', 'התחברת בהצלחה')
        else:
           xbmcgui.Dialog().ok('Movix', 'כישלון! בדוק פרטי התחברות')
           
    if 'Login successful' not in response.content:
      ok=False
      
    cook={}
    if ok:
        for key, morsel in response.cookies.items():
                cook[key] = morsel
   
    
    return cook,ok
def ClearCache():
   
    cache.clear(['id'])
    xbmc.executebuiltin((u'Notification(%s,%s)' % ('Movix', 'נוקה'.decode('utf8'))).encode('utf-8'))

params=get_params()

url=None
name=None
mode=None
iconimage=None
fanart=None
description=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass
try:        
        mode=int(params["mode"])
except:
        pass
try:        
        fanart=urllib.unquote_plus(params["fanart"])
except:
        pass
try:        
        description=urllib.unquote_plus(params["description"])
except:
        pass
   


if mode==None or url==None or len(url)<1:
        main_menu()
elif mode==2:
        scrape_site(url)
elif mode==3:
        play(name,url,iconimage,description)
elif mode==4:
        get_episodes(name,url,iconimage,description)
elif mode==5:
        search()
elif mode==6:
    ClearCache()
elif mode==9:
      testlogin(url)
      
xbmcplugin.setContent(int(sys.argv[1]), 'movies')


xbmcplugin.endOfDirectory(int(sys.argv[1]))

