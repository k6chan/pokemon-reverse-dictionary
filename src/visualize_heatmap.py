#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


df = pd.read_csv("models/data/bulbapedia_smogon_data.csv")
# df.head()


# In[3]:


names = df["name"].to_list()


# In[4]:


# Doc2Vec model

documents = []
for row in df.iterrows():
    doc = row[1]["description"]
    tag = row[1]["name"]
    documents.append(TaggedDocument(doc.split(),[tag]))
d2v_model = Doc2Vec(documents, vector_size=5, min_count=1)


# In[5]:


# matplotlib example heatmap from documentation

cols_pokemon = names[405:410]
rows_pokemon = names[405:410]

rows = []
for row in rows_pokemon:
    row_lst = []
    for col in cols_pokemon: 
        correlations = np.corrcoef(d2v_model.__getitem__(row),d2v_model.__getitem__(col))
        row_lst.append(np.round(correlations[1][0],2))
    rows.append(row_lst)
rows = np.array(rows)

fig, ax = plt.subplots()
im = ax.imshow(rows)

ax.set_xticks(np.arange(len(cols_pokemon)), labels=cols_pokemon)
ax.set_yticks(np.arange(len(rows_pokemon)), labels=rows_pokemon)

plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

for i in range(len(rows_pokemon)):
    for j in range(len(cols_pokemon)):
        text = ax.text(j, i, rows[i, j],
                       ha="center", va="center", color="w")

ax.set_title("Correlation between Pokemon document vectors")
fig.tight_layout()

plt.savefig("correlation_heatmap.eps", dpi=300)
plt.savefig("correlation_heatmap.png", dpi=300)

plt.show()

