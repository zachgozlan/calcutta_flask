import pandas as pd

def new_winning_bid(min_legal_bid, real_bid, new_bid, increment):
    j = list([min_legal_bid, real_bid + increment, new_bid])
    j = [i if i > real_bid else 10000000 for i in j]
    return min(j)

def bid_calculator(df):

    opening = pd.read_csv('/home/zachgozlan/flask_app/opening_bids.csv', encoding='latin-1')

    current = opening.copy(deep=True)

    current['Leader'] = 'Opening'
    current['Timestamp'] = pd.Timestamp('2023-03-05 22:00:00')
    current = current[['Team', 'Seed', 'Region', 'Leader', 'Opening Bid', 'Increment', 'Timestamp']]
    current.columns = ['Team', 'Seed', 'Region', 'Leader', 'Current Bid', 'Increment', 'Timestamp']
    current = current.set_index('Team')
    opening = opening.set_index('Team')

    for i, j in df.iterrows():

        print(str(j.id), ' ', j['name'])

        new_bid = j.bid
        new_bidder = j['name']
        bid_time = j.ts
        bid_team = j.team

        try:
            current_bid_time = current.loc[bid_team]['Timestamp']
            current_bid = round(current.loc[bid_team]['Current Bid'],2)
            current_winner = current.loc[bid_team]['Leader']
            increment = round(current.loc[bid_team]['Increment'],2)
        except KeyError:
            continue

        bid_list = list(df[(df.team == bid_team) & (df.ts < bid_time)]['bid'])
        bid_list.append(opening.loc[bid_team]['Opening Bid'])

        real_bid = round(max(bid_list),2)
        try:
            real_bid_time = list(df[(df.team == bid_team) & (df.bid == real_bid)]['ts'])[0]
        except IndexError:
            real_bid_time = pd.Timestamp('2023-03-05 21:00:00')

        min_legal_bid = round(current_bid + increment,2)


        if (current_winner == 'Opening') and (new_bid >= current_bid):
                #transfers opening bid to first taker
                current.at[j.team, 'Leader'] = new_bidder
                current.at[j.team, 'Timestamp'] = j.ts
                continue

        if (current_winner == new_bidder) and (new_bid >= current_bid):
                #transfers opening bid to first taker
                current.at[j.team, 'Timestamp'] = j.ts
                continue

        if min_legal_bid > new_bid: #checks for invalid bid
            continue

        else:

            if new_bid >= min_legal_bid:
                #if new bid is legal...
                if (new_bid > real_bid) & (min_legal_bid <= new_bid):
                    #and higher than the real price listed
                    if new_bidder != current_winner:
                        current.at[j.team, 'Leader'] = new_bidder
                        current.at[j.team, 'Current Bid'] = round(new_winning_bid(min_legal_bid, real_bid, new_bid, increment),2)
                        current.at[j.team, 'Timestamp'] = bid_time
                        continue
                    else:
                        current.at[j.team, 'Timestamp'] = bid_time
                        continue

                if (new_bid + increment) < real_bid:
                    current.at[j.team, 'Current Bid'] = round(new_bid + increment,2)
                    continue

                if ((real_bid > new_bid) & (new_bid >= min_legal_bid)) | (real_bid == new_bid):
                    current.at[j.team, 'Current Bid'] = round(real_bid,2)
                    continue

    y = pd.DataFrame(df.team.value_counts(ascending=False))
    y.columns = ['Bid Count']

    final = current.merge(y, how='left', left_index=True, right_index=True)

    final = final.fillna(0)

    final = final[['Seed', 'Region', 'Leader', 'Current Bid', 'Increment','Bid Count', 'Timestamp']]
    final['Bid Count'] = [int(i) for i in final['Bid Count']]

    #final = final.sort_values(by=['Current Bid'], ascending=False)
    final.to_csv('/home/zachgozlan/flask_app/current_bids.csv', encoding='latin-1')
    return final

def current_leaders(df):
    df2 = bid_calculator(df)
    df2['Team'] = df2.index

    df2 = df2[['Leader', 'Current Bid', 'Team']]

    df2 = df2.groupby('Leader').agg({'Current Bid':'sum',
                             'Team':' | '.join})

    df2 = df2[df2.index != 'Opening']
    df2['Current Bid'] = ['$' + str(round(i,2)) for i in df2['Current Bid']]
    df2 = df2.sort_index(key=lambda x: x.str.lower())

    return df2

def current_prizes(df):
    df = bid_calculator(df)
    prize_value = sum(df['Current Bid'])
    round_32 = prize_value / (63*1.23)
    round_16 = prize_value / (63*.98)
    round_8 = prize_value / (63*.88)
    round_4 = prize_value / (63*(1/1.4))
    round_2 = prize_value / (63*(1/1.75))
    round_1 = prize_value - (round_32*32) - (round_16*16) - (round_8*8) \
                - (round_4*4) - (round_2*2)

    prize_frame = pd.DataFrame(
    {'round': ['Win Round of 64', 'Make Sweet 16', 'Make Elite 8', 'Make Final Four', 'Make Finals', 'Win Title'],
     'prize': [round_32, round_16, round_8, round_4, round_2, round_1],
     'total_prize': [round_32, \
                    round_32 + round_16,\
                    round_32 + round_16 + round_8,\
                    round_32 + round_16 + round_8+round_4,\
                    round_32 + round_16 + round_8+round_4+round_2,\
                    round_32 + round_16 + round_8+round_4+round_2+round_1]})

    prize_frame['total_prize'] = [str(round(i,2)) for i in prize_frame.total_prize]
    prize_frame['prize'] = [str(round(i,2)) for i in prize_frame.prize]
    prize_frame = prize_frame.set_index('round')

    return prize_frame
