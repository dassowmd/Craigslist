import pandas as pd
from tqdm import tqdm


def save_df(self, df, file_path):
    try:
        df.to_csv(file_path, encoding='utf8')
    except:
        raw_input("Unable to save file. Is the file already open? Press enter to try again")
        save_df(self, df, file_path)

class flatten():
    def flatten(self, url_read="C:\Users\dasso\OneDrive\Documents\GitHub\Craigslist\CraigslistPosting.csv", url_write="C:\Users\dasso\OneDrive\Documents\GitHub\Craigslist\Craigslist_Posting_Rehydrated.csv"):
        df = pd.read_csv(url_read, encoding='utf8')


        unique_IDs = df.Cl_Item_ID.unique()

        listing_rehydrated_list = []
        for ID in tqdm(unique_IDs):
            details = pd.DataFrame(df[df['Cl_Item_ID'] == ID])
            listing_rehydrated = dict()
            # print details['Cl_Item_ID']
            listing_rehydrated['Item_ID'] = details['Cl_Item_ID'].iloc[0]
            listing_rehydrated['RSS_Feed_String'] = details['RSS_Feed_String'].iloc[0]
            listing_rehydrated['ScrapedDateTime'] = details['ScrapedDateTime'].iloc[0]
            for d in details.iterrows():
                d = dict(d[1])
                # print d
                listing_rehydrated[d['KeyParam']] = d['ValueParam']
            listing_rehydrated_list.append(listing_rehydrated)
        listing_rehydrated_df = pd.DataFrame(listing_rehydrated_list)
        save_df(self, listing_rehydrated_df, url_write)



# f = flatten()
    # f.flatten()