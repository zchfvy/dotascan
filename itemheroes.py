import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm

from data import matches, items, heroes


def build_data():
    slots = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5',
             'backpack_0', 'backpack_1', 'backpack_2']

    item_ids = [i['id'] for i in items]
    hero_ids = [h['id'] for h in heroes]
    df = pd.DataFrame(0, index=item_ids, columns=hero_ids)
    i_ser = pd.Series(0, index=item_ids)
    h_ser = pd.Series(0, index=hero_ids)
    for match in tqdm(matches, desc="Processing Matches"):
        for pl in match['players']:
            hero = pl['hero_id']
            h_ser[hero] += 1
            for slot in slots:
                item = pl[slot]
                if item != 0:
                    old_val = df.get_value(item, hero)
                    new_val = old_val + 1
                    df.set_value(item, hero, new_val)
                    i_ser[item] += 1

    # Next we process the data into percentages instead of raw values
    print("Calculating percentages")
    df_i = df.divide(i_ser, axis='index')
    df_h = df.divide(h_ser, axis='columns')
    df = df_i.multiply(df_h)

    return df


def preprocess_for_display(df):
    print("Preprocessing data for display")

    def process_hero(name):
        return name.replace('npc_dota_hero', '').replace('_', ' ')

    def process_item(name):
        return name.replace('item_', '').replace('_', ' ')

    # Fill in column names
    heromap = {h['id']: process_hero(h['name']) for h in heroes}
    itemmap = {i['id']: process_item(i['name']) for i in items}
    df = df.rename(columns=heromap, index=itemmap)

    # delete things we dont want to show
    bad_items = []
    for r in itemmap.values():
        if 'recipe' in r:
            bad_items.append(r)
        elif 'river_painter' in r:
            bad_items.append(r)
    df = df.drop(bad_items)

    df = df.transpose()  # Looks nicer this way

    return df


def show(df):
    print("Building Graphic")

    sns.set(style="white")

    f, ax = plt.subplots(figsize=(11, 9))
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    sns.heatmap(
                df, cmap=cmap,
                square=True, xticklabels=True, yticklabels=True,
                linewidths=.03, cbar_kws={"shrink": .5}, ax=ax)

    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)
    plt.show()


def main():
    df = build_data()
    df = preprocess_for_display(df)
    show(df)


if __name__ == '__main__':
    main()
