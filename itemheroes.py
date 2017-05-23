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
    buy = pd.DataFrame(0, index=item_ids, columns=hero_ids)
    win = pd.DataFrame(0, index=item_ids, columns=hero_ids)
    loss = pd.DataFrame(0, index=item_ids, columns=hero_ids)
    i_ser = pd.Series(0, index=item_ids)
    h_ser = pd.Series(0, index=hero_ids)
    for match in tqdm(matches, desc="Processing Matches"):
        for i, pl in enumerate(match['players']):
            hero = pl['hero_id']
            hero_is_radiant = i < 5
            h_ser[hero] += 1
            for slot in slots:
                item = pl[slot]
                if item != 0:
                    # old_val = buy.get_value(item, hero)
                    # new_val = old_val + 1
                    # buy.set_value(item, hero, new_val)
                    buy.ix[item, hero] += 1
                    i_ser[item] += 1
                    if match['radiant_win'] != hero_is_radiant:  # logical xor
                        loss.ix[item, hero] += 1
                    else:
                        win.ix[item, hero] += 1

    # Next we process the data into percentages instead of raw values
    print("Calculating percentages")
    buy_i = buy.divide(i_ser, axis='index')
    buy_h = buy.divide(h_ser, axis='columns')
    buy = buy_i.multiply(buy_h)

    return buy, win, loss


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
        if 'river' in r:
            bad_items.append(r)
    df = df.drop(bad_items)

    df = df.transpose()  # Looks nicer this way

    return df


def show(df, filename='out.png', pallete=None):
    print("Building Graphic")

    sns.set(style="white")

    f, ax = plt.subplots(figsize=(20, 15))
    if pallete is None:
        pallete = sns.light_palette("navy", as_cmap=True)
    sns.heatmap(
                df, cmap=pallete,
                square=True, xticklabels=True, yticklabels=True,
                linewidths=.03, cbar_kws={"shrink": .5}, ax=ax)

    plt.xticks(rotation=90, fontsize=8)
    plt.yticks(rotation=0, fontsize=8)

    plt.savefig(filename)
    plt.show()


def main():
    pick, win, loss = build_data()
    total = win.add(loss)

    # winloss = win.divide(win.add(loss)) # naieve
    winloss = win.add(1).divide(total.add(2))  # laplace

    pick = preprocess_for_display(pick)
    winloss = preprocess_for_display(winloss)
    pick = pick.pow(1.0/4.0)  # exagerate the values in the buy rate cahrt
    winloss = winloss*2.0 - 1.0  # Change from 0,1 winrate to -1,+1

    coolwarm = sns.diverging_palette(20, 220, as_cmap=True)
    show(pick, 'pick.png')
    show(winloss, 'win.png', pallete=coolwarm)
    show(pick*winloss, 'pickwin.png', pallete=coolwarm)


if __name__ == '__main__':
    main()
