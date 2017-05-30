import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm


def get_data(fresh=False):
    if not fresh:
        try:
            win = pd.read_pickle('item_win.pickle')
            loss = pd.read_pickle('item_loss.pickle')
            return win, loss
        except:
            print("Error reading pickled data")
            print("Loading data fresh")

    win, loss = build_data()

    win.to_pickle('item_win.pickle')
    loss.to_pickle('item_loss.pickle')

    return win, loss


def build_data():
    from data import get_matches, get_items
    slots = ['item_0', 'item_1', 'item_2', 'item_3', 'item_4', 'item_5',
             'backpack_0', 'backpack_1', 'backpack_2']

    items = get_items()
    matches = get_matches()

    item_ids = [i['id'] for i in items]
    win = pd.Series(0, index=item_ids)
    loss = pd.Series(0, index=item_ids)
    for match in tqdm(matches, desc="Processing Matches"):
        for i, pl in enumerate(match['players']):
            hero_is_radiant = i < 5
            for slot in slots:
                item = pl[slot]
                if item != 0:
                    if match['radiant_win'] != hero_is_radiant:  # logical xor
                        loss[item] += 1
                    else:
                        win[item] += 1

    return win, loss


def preprocess_for_display(dat):
    from data import get_items
    print("Preprocessing data for display")

    items = get_items()
    items_index = {i['id']: i for i in items}

    for item_id, value in dat.iteritems():
        items_index[item_id]['winrate'] = value

    bad_items = []
    for item_id, it in items_index.items():
        if 'recipe' in it['name']:
            bad_items.append(item_id)
        if 'river' in it['name']:
            bad_items.append(item_id)
    for item_id in bad_items:
        del items_index[item_id]

    df = pd.DataFrame(items_index)
    df = df.transpose()

    df['cost'] = df['cost'].apply(pd.to_numeric)

    print(df)

    return df


def show(df, filename='out.png', pallete=None):
    print("Building Graphic")

    sns.set(style="white")

    f, ax = plt.subplots(figsize=(20, 15))
    if pallete is None:
        pallete = sns.light_palette("navy", as_cmap=True)
    sns.regplot(x="cost", y="winrate", data=df)

    plt.savefig(filename)
    plt.show()


def main():
    win, loss = get_data()
    total = win.add(loss)

    # winloss = win.divide(win.add(loss)) # naieve
    winloss = win.add(1).divide(total.add(2))  # laplace
    #winloss = winloss*2.0 - 1.0  # Change from 0,1 winrate to -1,+1

    winloss = preprocess_for_display(winloss)

    coolwarm = sns.diverging_palette(20, 220, as_cmap=True)
    show(winloss, 'win.png', pallete=coolwarm)


if __name__ == '__main__':
    main()
