#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import spacy
import json

spacy.cli.download("en_core_web_sm")


# ## Smogon

# ### Tidy data

# In[2]:


smogon_url = 'https://www.smogon.com/dex/sm/pokemon/' #most pokemon in this generation
smogon_text = requests.get(smogon_url).text
smogon_soup = BeautifulSoup(smogon_text,'html.parser')


# In[3]:


smogon_javascript = smogon_soup.find_all('script', class_="", attrs={'type':'text/javascript'})[1]
left_brace_location = smogon_javascript.text.find('{')
smogon_json = smogon_javascript.text[left_brace_location:]
smogon_object = json.loads(smogon_json)
smogon_data = smogon_object['injectRpcs'][1][1]
smogon_pokemon = smogon_data['pokemon']
def is_standard(pokemon):
    return pokemon['isNonstandard'] == 'Standard' #fan-created Pokemon are labeled as Nonstandard
smogon_real_pokemon = list(filter(is_standard,smogon_pokemon))


# In[4]:


pokemon_table = pd.DataFrame(data=smogon_real_pokemon)
# pokemon_table.head()


# In[5]:


def get_nth_element(lst, n):
    if len(lst) > (n-1):
        return lst[n-1]
    else:
        return np.nan
    
def get_additional_information(oob, key):
    return oob[key]

pokemon_formats = pokemon_table['formats'].apply(get_nth_element, args=(1,))
pokemon_abilities_1 = pokemon_table['abilities'].apply(get_nth_element, args=(1,))
pokemon_abilities_2 = pokemon_table['abilities'].apply(get_nth_element, args=(2,))
pokemon_abilities_3 = pokemon_table['abilities'].apply(get_nth_element, args=(3,))
pokemon_abilities_4 = pokemon_table['abilities'].apply(get_nth_element, args=(4,))
pokemon_types_1 = pokemon_table['types'].apply(get_nth_element, args=(1,))
pokemon_types_2 = pokemon_table['types'].apply(get_nth_element, args=(2,))
pokemon_natdex = pokemon_table['oob'].apply(lambda oob: oob["dex_number"] if isinstance(oob,dict) else -1)
pokemon_evo = pokemon_table['oob'].apply(lambda oob: " ".join(oob["evos"]) if isinstance(oob,dict) else np.nan)


# In[6]:


pokemon = pokemon_table.drop(
    columns=["types","abilities","oob","isNonstandard"]).assign(
    formats=pokemon_formats,ability_1=pokemon_abilities_1,
              ability_2=pokemon_abilities_2,ability_3=pokemon_abilities_3,
              ability_4=pokemon_abilities_4,type_1=pokemon_types_1,type_2=pokemon_types_2,
              nat_dex=pokemon_natdex, evos=pokemon_evo)
# pokemon.head()


# ### Prepare for features

# In[7]:


#some competitive terminology
smogon_dict = {}
smogon_dict["attack_discretized"] = pd.cut(pokemon["atk"], bins=2 ,labels=["weak", "strong"])
smogon_dict["spa_discretized"] = pd.cut(pokemon['spa'], bins=2, labels=["weak","strong"])
smogon_dict["def_discretized"] = pd.cut(pokemon["def"], bins=2 ,labels=["frail", "bulky"])
smogon_dict["spd_discretized"] = pd.cut(pokemon["spd"], bins=2 ,labels=["frail", "bulky"])
smogon_dict["spe_discretized"] = pd.cut(pokemon["spe"], bins=2 ,labels=["slow", "fast"])
smogon_dict["weight_discretized"] = pd.cut(pokemon["weight"], bins=2 ,labels=["light", "heavy"])
smogon_dict["height_discretized"] = pd.cut(pokemon["height"], bins=2 ,labels=["short", "tall"])


# In[8]:


smogon_dict["abilities"] = pokemon_table["abilities"].str.join(" ")
smogon_dict["types"] = pokemon_table["types"].str.join(" ")
smogon_dict["evos"] = pokemon["evos"]
smogon_dict["names"] = pokemon["name"]
smogon_dict["nat_dex"] = pokemon["nat_dex"]


# In[9]:


smogon_pokemon = pd.DataFrame(smogon_dict)
descriptions = smogon_pokemon.apply(lambda col: ' '.join(col.astype(str)), axis=1)
smogon_pokemon_descriptions = pd.DataFrame({"name": pokemon["name"], "nat_dex": pokemon["nat_dex"], "description": descriptions})
# smogon_pokemon_descriptions.head()


# ----

# ## Bulbapedia

# In[11]:


bulbapedia_url = "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number"
bulbapedia_text = requests.get(bulbapedia_url).text
bulbapedia_soup = BeautifulSoup(bulbapedia_text,'html.parser')


# In[12]:


bulbapedia_ndex = bulbapedia_soup.find_all("td", {"style":"font-family:monospace,monospace"})
ndex = list(map(lambda n: n.text[1:], bulbapedia_ndex))
ndex_ser = pd.Series(ndex).astype(int)

# ndex_ser.head()


# In[13]:


bulbapedia_rows = bulbapedia_soup.find_all(lambda tag: tag.name == 'td' and not tag.attrs)[:-1] # exclude the final td, which is not a Pokemon

bulbapedia_names = []

bulbapedia_thumbnails = []
for soup in bulbapedia_rows:
    img_search = soup.find('a')
    bulbapedia_names.append(img_search.get("href"))
    
    src_search = soup.find('img')
    if src_search is not None:
        bulbapedia_thumbnails.append(src_search.get("src"))
bulbapedia_names = bulbapedia_names[1::2]
bulbapedia_names_ser = pd.Series(bulbapedia_names)
# bulbapedia_names = bulbapedia_names_ser.unique() #remove duplicates
bulbapedia_names_ser = pd.Series(bulbapedia_names)
                                     
bulbapedia_thumbnails_ser = pd.Series(bulbapedia_thumbnails)
bulbapedia_thumbnails_ser = pd.Series(bulbapedia_thumbnails)

bulbapedia_dex = pd.DataFrame({"page":bulbapedia_names_ser, "thumbnail": bulbapedia_thumbnails_ser})
bulbapedia_dex_unique = bulbapedia_dex.iloc[bulbapedia_dex[["page"]].drop_duplicates().index].reset_index().drop(columns=["index"]) #remove alternate forms
# bulbapedia_dex_unique.head()


# In[14]:


bulbapedia_pokemon_table = bulbapedia_dex_unique.assign(ndex=ndex_ser, thumbnail="https:" + bulbapedia_dex_unique["thumbnail"])
# bulbapedia_pokemon_table.head()


# In[15]:


CACHE = {}
vocab = spacy.load('en_core_web_sm')

def get_bulbapedia_biology(page_pokemon):
    if page_pokemon in CACHE:
        return CACHE[page_pokemon]
    page_root = "https://bulbapedia.bulbagarden.net"
    entry_text = requests.get(page_root + page_pokemon).text
    entry_soup = BeautifulSoup(entry_text,'html.parser')
    pokemon_text_lst = []
    biology_span = entry_soup.find("span",id="Biology").next_elements
    for i, element in enumerate(biology_span):
        if i == 0:
            continue
        if element.name == "h2": # next section
            break
        pokemon_text_lst.append(element.get_text(strip=True))
    pokemon_text = ' '.join(pokemon_text_lst).strip()
    doc = vocab(pokemon_text)
    tokens = set()
    for token in doc:
        if token.pos_ == 'NOUN':
            tokens.add(token.lemma_)
    nouns = " ".join(tokens)
    CACHE[page_pokemon] = nouns
    return nouns


# ### Prepare for merging

# In[16]:


# removes alternate forms and Gen 8+ Pokemon
bulbapedia_smogon = bulbapedia_pokemon_table.assign(
    ndex = bulbapedia_pokemon_table["ndex"]).merge(
    smogon_pokemon_descriptions, how="inner", left_on="ndex", right_on="nat_dex")
bulbapedia_smogon = bulbapedia_smogon.assign(ndex=bulbapedia_smogon['ndex'].astype(int)).set_index("ndex")
# bulbapedia_smogon.head()


# In[17]:


bulbapedia_smogon_descriptions_separate = bulbapedia_smogon.assign(biology = bulbapedia_smogon["page"].apply(get_bulbapedia_biology))


# In[18]:


bulbapedia_smogon_tidy = bulbapedia_smogon_descriptions_separate.assign(
    description = bulbapedia_smogon_descriptions_separate["description"] + " " + bulbapedia_smogon_descriptions_separate["biology"]).drop(
    columns=["page", "biology","nat_dex"])

# bulbapedia_smogon_tidy.head()


# In[30]:


# lowercase
bulbapedia_smogon_tidy = bulbapedia_smogon_tidy.assign(description=bulbapedia_smogon_tidy["description"].str.lower())


# In[31]:


bulbapedia_smogon_tidy.to_csv("bulbapedia_smogon_data.csv")

