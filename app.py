import streamlit as st
import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns

st.set_page_config(layout="wide")
st.sidebar.title("WhatsApp Chat Analyzer By Jay Lakhani")

upload_file = st.sidebar.file_uploader("Upload a .txt file")
if upload_file is not None:
    bytes_data = upload_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0, "All users")

    selected_user = st.sidebar.selectbox("Select User", user_list)

    if st.sidebar.button("Show Analysis"):
        # Show statistics
        num_message, words, num_media_messages, num_url = helper.fetch_stats(selected_user, df)
        st.title("Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Number of media")
            st.title(num_media_messages)
        with col4:
            st.header("Number of URL")
            st.title(num_url)

        #Timeline
        st.title("Monthly timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots();
        ax.plot(timeline['time'], timeline['message'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #Activity map
        st.title("Activity map")
        col1,col2=st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day= helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='orange')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='violet')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)
        
        
        # Finding busiest user in the group (group level)
        if selected_user == 'All users':
            st.title("Most busy Users")
            x, new_df = helper.most_busy_users(df)

            fig, ax = plt.subplots()
            fig1, ax1 = plt.subplots()
            col1, col2, col3 = st.columns(3)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                if 'percent' in new_df.columns and 'name' in new_df.columns:
                    ax1.pie(new_df['percent'], labels=new_df['name'], autopct='%1.1f%%', startangle=90)
                    st.pyplot(fig1)
                # else:
                #     st.error("Required columns for plotting not found in DataFrame.")

            with col3:
                st.dataframe(new_df)

        # wordcloud
        st.title("Wordcloud")
        df_wc=helper.create_word_cloud(selected_user,df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        st.title("Most common words")
        most_common_df=helper.most_common_words(selected_user,df)

        fig,ax=plt.subplots()

        # ax.barh(most_common_df[0],most_common_df[1])
        ax.barh(most_common_df.iloc[:, 0], most_common_df.iloc[:, 1])

        plt.xticks(rotation='vertical')

        st.pyplot(fig)

        #emojis analysis

        emoji_df=helper.imoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2=st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct='%1.1f%%')
            st.pyplot(fig)
