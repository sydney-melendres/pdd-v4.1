import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Latency Analysis", page_icon="📊")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('final-data/round_summary_adjusted.csv')
    except Exception as e:
        st.error(f"Error loading the data: {str(e)}")
        return None

df = load_data()

if df is not None:
    def generate_statistics(df):
        grouped = df.groupby('latency')
        result_dfs = {}
        
        for latency, group in grouped:
            unique_player_ips = group['player_ip'].unique()
            latency_df = pd.DataFrame(index=unique_player_ips)
            
            group = group[group['latency'] == latency]
            
            for game_round in group['game_round'].unique():
                round_scores = group[group['game_round'] == game_round].set_index('player_ip')['score'].rename(f'Round_{game_round}')
                latency_df = latency_df.join(round_scores, how='left')
            
            latency_df['Mean'] = latency_df.mean(axis=1)
            latency_df['StdDev'] = latency_df.std(axis=1)
            
            if 0 in result_dfs:
                latency_df['mean_difference'] = latency_df['Mean'] - result_dfs[0]['Mean']
            else:
                latency_df['mean_difference'] = 0
            
            result_dfs[latency] = latency_df
        
        return result_dfs

    result_dfs = generate_statistics(df)

    st.title('Players\' Mean Scores vs Latency Statistical Analysis')

    latency_values = list(result_dfs.keys())
    selected_latency = st.selectbox('Select Latency Value (ms)', latency_values, index=0)

    st.subheader(f'Statistics for Latency {selected_latency}')
    st.dataframe(result_dfs[selected_latency])

    fig, ax = plt.subplots(figsize=(12, 8))

    for player_ip in df['player_ip'].unique():
        means = [result_dfs[latency].loc[player_ip, 'Mean'] for latency in result_dfs.keys() if player_ip in result_dfs[latency].index]
        ax.plot(list(result_dfs.keys()), means, marker='o', label=f'Player {player_ip}')
    
    ax.set_xticks(list(result_dfs.keys()))
    ax.set_xlabel('Latency')
    ax.set_ylabel('Mean Score')
    ax.set_title('Players\' Mean Scores vs Latency')
    ax.legend()

    st.pyplot(fig)

else:
    st.error("Cannot proceed with analysis due to data loading error.")