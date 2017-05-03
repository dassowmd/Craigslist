import pandas as pd


class flatten():
    def flatten(self):
        df = pd.read_csv("C:\Users\dasso\OneDrive\Documents\GitHub\Craigslist\CraigslistPosting.csv", encoding='utf8')


        unique_IDs = df.Cl_Item_ID.unique()

        listing_rehydrated_list = []
        for ID in unique_IDs:
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
        listing_rehydrated_df.to_csv("C:\Users\dasso\OneDrive\Documents\GitHub\Craigslist\Craigslist_Posting_Rehydrated.csv", encoding='utf8')