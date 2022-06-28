# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 11:05:15 2021

@author: mahon
"""

from bs4 import BeautifulSoup
import urllib.request
import re
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains

url='https://www.foxnews.com/search-results/search?q=Opinion'
urls=[]
driver = webdriver.Chrome("C:/Users/mahon/Documents/Python Scripts/chromedriver.exe")
time.sleep(2)
driver.get(url)

search_type_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[2]/button'
type_menu=driver.find_element_by_xpath(search_type_xpath)
type_menu.click()

text_type_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[2]/ul/li[1]/label'
text_type=driver.find_element_by_xpath(text_type_xpath)


begin_month_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[1]/button'
begin_day_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[2]/button'
begin_year_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[3]/button'

end_month_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/button'
end_day_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div[2]/button'
end_year_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div[3]/button'

topics=['opinion','politics','hannity','house','ingrham','tucker','healthcare',
        'aca','cavuto','democrats','republicans','u.s','','congress','mcconnell',
        'pelosi','guns','trump','biden','obama','religon','virus','riots',
        'economy','trade','war','military','senate','committee','2012 election',
        '2016 election','2020 election','qanon','freedom','racist','racism','president',
        'civil rights','Op-Ed','ducey','duffy','gingrich','geraldo','socialism','pirro',
        'doocey','rove','bengazi','hilary','romney','manchin','shumer','mccarthey','ryan','boehner',
        'ACA','second amendment','climate change','ukraine','russia','europe','iraq','afganistan',
        'wallace','COVID','supreme court','black lives matter','drones','terrorism','clinton','bush',
        'ben shapiro','antifa','election security','travel ban','immigration','forgeiners']


for i in range(63,76):
    print(topics[i])
    url='https://www.foxnews.com/search-results/search?q='+topics[i]+''
    time.sleep(10)
    for j in range(11):
        driver.get(url)
        type_menu=driver.find_element_by_xpath(search_type_xpath)
        type_menu.click()
        text_type=driver.find_element_by_xpath(text_type_xpath)
        text_type.click()
        type_menu.click()
        
        #Enter Start Date
        begin_month_drop=driver.find_element_by_xpath(begin_month_xpath)
        begin_month_drop.click()
        
        jan_clicker_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[1]/ul/li[1]'
        jan_clicker=driver.find_element_by_xpath(jan_clicker_xpath)
        jan_clicker.click()
        
        begin_day=driver.find_element_by_xpath(begin_day_xpath)
        begin_day.click()
        
        first_day_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[2]/ul/li[1]'
        first_day=driver.find_element_by_xpath(first_day_xpath)
        first_day.click()
        
        start_year_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[3]/button'
        start_year=driver.find_element_by_xpath(start_year_xpath)
        start_year.click()
        
        start_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[1]/div[3]/ul/li['+str(11-j)+']'
        start=driver.find_element_by_xpath(start_xpath)
        start.click()
        
        
        #Enter End Date
        
        
        end_month_drop=driver.find_element_by_xpath(end_month_xpath)
        end_month_drop.click()
        
        dec_clicker_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div[1]/ul/li[12]'
        dec_clicker=driver.find_element_by_xpath(dec_clicker_xpath)
        dec_clicker.click()
        
        end_day=driver.find_element_by_xpath(end_day_xpath)
        end_day.click()
        
        last_day_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div[2]/ul/li[31]'
        last_day=driver.find_element_by_xpath(last_day_xpath)
        last_day.click()
        
        end_year=driver.find_element_by_xpath(end_year_xpath)
        end_year.click()
        
        end_xpath='/html/body/div/div/div/div/div[1]/div/div[2]/div[3]/div[2]/div[3]/ul/li['+str(11-j)+']'
        end=driver.find_element_by_xpath(end_xpath)
        end.click()
        
        search_xpath='/html/body/div/div/div/div/div[1]/div/div[1]/div[2]/div/a'
        search=driver.find_element_by_xpath(search_xpath)
        search.click()
        
        
        while True:
            time.sleep(2)
            try:        
                element=driver.find_elements_by_xpath('/html/body/div/div/div/div/div[2]/div/div[3]/div[2]/a/span')
                element[0].click()
                html = driver.page_source.encode('utf-8')
                html = html.decode("utf-8")
            except:
                break
        
        
        
        links=re.findall('<a href="(.+?)" target="_blank">',html)
        entries = [e for e in links if "politics" in e or "opinion" in e]
        entries=list(set(entries))
        entries = [e for e in entries if "https://www.foxnews.com/politics" != e ]
        entries = [e for e in entries if "https://www.foxnews.com/opinion" != e ]
        
        urls.extend(entries)



urls=list(set(urls))

df = pd.DataFrame(urls) 
    
# saving the dataframe 
df.to_csv('FOXNEWS.csv') 

#%%



data=pd.read_csv(r"C:\Users\mahon\FOXNEWS.csv")
N2=len(data['Link'])


links=list(data['Link'])

N2=len(links)
texts = ["" for i in range(N2)]

for j in range(0,600):
    print(j)
    page = urlopen(links[j])
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    
    dt=find_date(html)

    speaker=re.findall('="dcterms.creator" content="(.+?)">',html)
    
    year=int(dt[0:4])
    month=int(dt[5:7])
    
    if year<2019:
        continue
    
    if year==2021 and month>3:
        continue
    
    soup = BeautifulSoup(html, "html.parser")
    texts[j]=soup.get_text()
    texts[j]=texts[j].replace('\n','')
    
    texts[j]=texts[j].lower()
    
    tokens=nltk.tokenize.RegexpTokenizer("[\\w']+|[^\\w\\s]+").tokenize(texts[j])
    tokens = list(filter(lambda token: token not in string.punctuation, tokens))
    filter(lambda x: x in printable, tokens)
    tokens = [sub.replace("ago", '') for sub in tokens]
    tokens = [sub.replace('+', '') for sub in tokens] 
    tokens = [sub.replace(',', '') for sub in tokens] 
    tokens = [sub.replace('`', '') for sub in tokens] 
    tokens = [sub.replace('-', '') for sub in tokens]
    tokens = [sub.replace("'", '') for sub in tokens]
    tokens = [sub.replace("’", '') for sub in tokens]
    tokens = [sub.replace("”", '') for sub in tokens]
    tokens = [sub.replace("”", '') for sub in tokens]
    tokens = [sub.replace("‘", '') for sub in tokens]
    tokens = [sub.replace("“", '') for sub in tokens]
    tokens = [sub.replace(")", '') for sub in tokens]
    tokens = [sub.replace("(", '') for sub in tokens]
    tokens = [sub.replace("]", '') for sub in tokens]
    tokens = [sub.replace("[", '') for sub in tokens]
    tokens = [sub.replace('."', '') for sub in tokens]
    tokens = [sub.replace('."', '') for sub in tokens]
    tokens = [sub.replace('.', '') for sub in tokens]
    tokens = [sub.replace('NewsFacebookTwitterFlipboardPrintEmailYou', '') for sub in tokens]
    tokens = [sub.replace('NewsFacebookTwitterFlipboardPrintEmailNow', '') for sub in tokens]
    tokens = [sub.replace('"', '') for sub in tokens]
    tokens = [sub.replace('Fox', '') for sub in tokens]
    tokens = [sub.replace('com', '') for sub in tokens] 
    tokens=list(filter(lambda a: a != '', tokens))
    tokens=list(filter(lambda w: not w in stops,tokens))
    tokens = list(filter(lambda token: token not in excluded_words, tokens))
      
    bigram = list(ngrams(tokens, 2)) 
    for i in range(len(bigram)):
       bigram[i]=str(bigram[i])
    
    bigram=list(filter(lambda w: not w in excluded_bigrams,bigram))
    
    trigram=list(ngrams(tokens,3))
    for i in range(len(trigram)):
       trigram[i]=str(trigram[i])
    
    trigram=list(filter(lambda w: not w in excluded_trigrams,trigram))
    
     
    
    size_token=len(tokens)
    size_bigram=len(bigram)
    size_trigram=len(trigram)
     
    #Generate Words DF
    Net="Fox"
    lst4=[speaker][0]*size_token
    lst2=[Net]*size_token
    lst3=[dt]*size_token
    
    words_df_temp=pd.DataFrame({'Channel': lst2,'Date':lst3,'Speaker':lst4,'Word': tokens})   
      
    #Generate Bigrams DF
    lst4=[speaker][0]*size_bigram
    Net="Fox"
    lst2=[Net]*size_bigram
    lst3=[dt]*size_bigram
    
    bigrams_df_temp=pd.DataFrame({'Channel': lst2,'Date':lst3,'Speaker':lst4,'Bigrams': bigram})
    
    #Generate Trigrams DF
    lst4=[speaker][0]*size_trigram
    Net="Fox"
    lst2=[Net]*size_trigram
    lst3=[dt]*size_trigram
    
    trigrams_df_temp=pd.DataFrame({'Channel': lst2,'Date':lst3,'Speaker':lst4,'Trigrams': trigram})
    
    
    
    bigrams_df_temp.to_sql('scrape_bigrams', conn, if_exists='append', index=False)
    words_df_temp.to_sql('scrape_words', conn, if_exists='append', index=False)
    trigrams_df_temp.to_sql('scrape_trigrams', conn, if_exists='append', index=False)
    
    words_df=pd.concat([words_df,words_df_temp])
    bigrams_df=pd.concat([bigrams_df,bigrams_df_temp])
    trigrams_df=pd.concat([trigrams_df,trigrams_df_temp])












#%%

search_xpath='//*[@id="wrapper"]/div[2]/div[1]/div/div[1]/div[2]/input'
button_xpath='//*[@id="wrapper"]/div[2]/div[1]/div/div[1]/div[2]/div/a'

search_bar=driver.find_element_by_xpath(search_xpath)
search_bar.send_keys('Guns')

month_begin=driver.find_element_by_xpath(begin_month_xpath)
month_begin.click()
driver.find_element_by_xpath('//*[@id="02"]').click()


day_begin=driver.find_element_by_xpath(begin_day_xpath).click()
button=driver.find_element_by_xpath('//*[@id="01"]')
button=driver.find_element_by_xpath('/html/body/div/div/div/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/ul/li[1]')
button=driver.find_element_by_xpath('//*[@id="01"]/following-sibling::after')
driver.implicitly_wait(10)



driver.execute_script("arguments[0].click();", button)

<li id="01" class="01">01</li>

document.querySelector("#\\30 2")

button.click()

ActionChains(driver).move_to_element(button).click(button)

ActionChains(driver).move_to_element(button)
button.click()

year_begin=driver.find_element_by_xpath(begin_year_xpath)
year_begin.click()
driver.find_element_by_xpath('//*[@id="2016"]').click()

month_end=driver.find_element_by_xpath(end_month_xpath).click()
button=driver.find_element_by_xpath('//*[@id="01"]')
button.click()


day_end=driver.find_element_by_xpath(end_day_xpath).click()
button=driver.find_element_by_xpath('//*[@id="01"]')
button.click()

ActionChains(driver).move_to_element(button)
button.click()

//*[@id="wrapper"]/div[2]/div[1]/div/div[2]/div[3]/div[1]/div[2]/ul



search_button=driver.find_element_by_xpath(button_xpath)
search_button.click()




search_bar.clear()














