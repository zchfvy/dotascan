import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from data import matches, items, heroes

sns.set(style="white")

slots = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5',
         'backpack_0', 'backpack_1', 'backpack_2']

item_ids = [i['id'] for i in items]
hero_ids = [h['id'] for h in heroes]
df = pd.DataFrame(index=item_ids, columns=hero_ids)
for match in matches:
    for pl in match['players']:
        for slot in slots:
            hero = pl['hero_id']
            item = pl[slot]
            if item != 0:
                old_val = df.get_value(item, hero)
                if pd.isnull(old_val):
                    new_val = 1
                else:
                    new_val = old_val + 1
                df.set_value(item, hero, new_val)

# delete empty rows
df = df.dropna(axis='index', how='all')
# and columns
df = df.dropna(axis='columns', how='all')
# then make all the NaNs into zero
df = df.fillna(0)

print df

f, ax = plt.subplots(figsize=(11,9))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(df, cmap=cmap, vmax=.3,
            square=True, xticklabels=5, yticklabels=5,
            linewidths=.5, cbar_kws={"shrink": .5}, ax=ax)

plt.show()
