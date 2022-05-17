import math
import matplotlib.pyplot as plt
import pandas as pd
import re

def data_scrape():
    # create inactive group
    f = open("/home/sam/Coding/discord_chasing_values/inactive.csv", "r")
    temp = f.readlines()
    inactive = []
    for name in temp:
        inactive.append(name.split()[2])
    f.close

    # pulling data from file
    f = open("/home/sam/Coding/discord_chasing_values/chasing_raw.txt", "r")
    txt = f.read().replace("ApatheticEconomist", "Syllean").replace('66bakerzdozen66','Tashab9120').replace('HyperHC','i_Ferfs')

    results = []
    for i in range(1, 5):
        results.extend(
            re.findall(
                "((?:\d{2}/){2}\d{4})(?:.*\n){" + str(i) + "}(\S+) \((\S+%)", txt
            )
        )

    # creating pandas dataframe and drop duplicates and inactive users
    df_raw = pd.DataFrame(results, columns=["Date", "Username", "EB"])
    df = df_raw.drop_duplicates()
    for user in inactive:
        df = df[df.Username != user]  

    # pulling data and creating conversion dictionary
    f = open("/home/sam/Coding/discord_chasing_values/conversion_table.txt", "r")
    con_table_raw = f.read()
    f.close()

    con_table = str(con_table_raw.replace("\n", "\t")).split("\t")
    conversion_dict = {}
    for i in range(1, len(con_table), 2):
        try:
            conversion_dict[con_table[i]] = int(con_table[i - 1])
        except:
            conversion_dict[int(con_table[i])] = con_table[i - 1]
    return df, conversion_dict

def main():
    # adding extra columns to dataframe
    def EB_long(EB):
        oom = re.findall("\d(\D+)%", EB)[0]
        eb_long = float(re.findall("[\d\.]+", EB)[0]) * (10 ** conversion_dict[oom])
        return eb_long

    def Role(EB):
        oom = int(math.log10(EB_long(EB) / 100))
        role = conversion_dict[oom - oom % 3] + "farmer " + str(oom % 3 + 1)
        return role

    def upper(username):
        return username.upper()

    [df, conversion_dict] = data_scrape()
    df["EB_long (%)"] = df.apply(lambda row: EB_long(row.EB), axis=1)

    # convert dates to readable date values, ordering by Username (not discriminate of upper/lowercases), Date then EB. Index reset
    df["Date"] = pd.to_datetime(df.Date, dayfirst=True)
    df["user_upper"] = df.apply(lambda row: upper(row.Username), axis=1)
    df = df.sort_values(["user_upper", "Date", "EB_long (%)"]).reset_index()
    df = df.drop(columns=["user_upper"])

    # delete duplicate dates for each person, keep highest EB
    df_user = df.drop(columns=["index", "EB"]).drop_duplicates(
        subset=["Date", "Username"], keep="last"
    )

    # pivot Usernames into columns
    df_user = df_user.pivot(index="Date", columns="Username", values="EB_long (%)")

    # create list of Usernames
    users = pd.DataFrame({"Username": df.Username.unique()}).values.tolist()

    # filter off dates before start of group
    res = df_user.loc['2021-02-15':]
    df_user = res

    # new dataframe
    df_increase = pd.DataFrame(index=res.index)

    def increase(EB):
        min = res.min()[user]
        new_eb = EB / min
        return new_eb
    
    for user in users:
        df_increase[user] = res.apply(lambda row: increase(row[user]), axis=1)

    # write to csv
    df.to_csv("data.csv")
    df_user.to_csv("users.csv")
    df_increase.to_csv("increase.csv")

    return users, df_user, df_increase

def graph_all():
    [users, df_user, df_increase] = main()

    # define graph and add lines
    ax = df_user[users[0]].dropna().plot()
    for user in users:
        if user == users[0]:
            continue
        df_user[user].dropna().plot(ax=ax)
    plt.legend(bbox_to_anchor=(1.01,1.04), loc="upper left")
    plt.show()
    return ax

def graph_increase():
    [users, df_user, df_increase] = main()

    # define graph and add lines
    ax = df_increase[users[0]].dropna().plot()
    for user in users:
        if user == users[0]:
            continue
        df_increase[user].dropna().plot(ax=ax)
    plt.legend(bbox_to_anchor=(1.01,1.04), loc="upper left")
    plt.show()

    return ax

def top5():
    [users, df_user, df_increase] = main()

    top5 = []

    for user in users:
        # check if max value is more than list min
        
        
        #if 
        # add to list w/ user
        # sort
        # del smallest
        return

def test():
    [users, df_user, df_increase] = main()

    # define graph and add lines
    ax = df_user['DrunkenPangolin'].dropna().plot()
    df_user['Lelands89'].dropna().plot(ax=ax)
    plt.legend(bbox_to_anchor=(0.2,0.9), loc="upper right")
    plt.show()

data_scrape()
main()
test()