import math
import matplotlib.pyplot as plt
import pandas as pd
import re


def data_scrape():
    # pulling data from file
    f = open("/home/sam/Coding/discord_chasing_values/chasing_raw.txt", "r")
    txt = f.read().replace("ApatheticEconomist", "Syllean")
    f.close()

    results = []
    for i in range(1, 5):
        results.extend(
            re.findall(
                "((?:\d{2}/){2}\d{4})(?:.*\n){" + str(i) + "}(\S+) \((\S+%)", txt
            )
        )

    # creating pandas dataframe and drop duplicates
    df_raw = pd.DataFrame(results, columns=["Date", "Username", "EB"])
    df = df_raw.drop_duplicates()

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

    # write to csv
    df.to_csv("data.csv")
    df_user.to_csv("Users.csv")

    # create list of Usernames
    users = pd.DataFrame({"Username": df.Username.unique()}).values.tolist()
    return users, df_user, df


def graph_all():
    [users, df_user, df] = main()

    # define graph and add lines
    ax = df_user[users[0]].dropna().plot()
    for user in users:
        if user == users[0]:
            continue
        df_user[user].dropna().plot(ax=ax)
    plt.show()
    return ax


def graph_increase():
    [users, df_user, df] = main()

    # create new df from increases
    increase = pd.DataFrame(index=df_user.index)
    for user in users:
        increase[user] = df_user.apply(
            lambda row: df_user[user] / df_user.min()[user], axis=1
        )
    ax = increase[users[0]].dropna().plot()
    for user in users:
        print(user)
        if user == users[0]:
            continue
        increase[user].dropna().plot(ax=ax)
    plt.show()
    return ax


user = "DrunkenPangolin"
[users, df_user, df] = main()
df_user.apply(lambda row: df_user[user] / df_user.min()[user], axis=1)
print(df_user[(df_user[username])])
