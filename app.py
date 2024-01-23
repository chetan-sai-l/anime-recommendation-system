from flask import Flask,render_template,request
import pickle
import numpy as np
from fuzzywuzzy import process
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
most_popular_df = pickle.load(open('most_popular_df.pkl','rb'))
pt_value = pickle.load(open('pt_value.pkl','rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl','rb'))
anime_url = pickle.load(open('anime_url.pkl','rb'))
eng_title = pickle.load(open('eng_title.pkl','rb'))
anime_url_id = pickle.load(open('anime_url_id.pkl','rb'))
app = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')

def process_query(query):
    # Tokenize the query
    tokens = word_tokenize(query)

    # Remove stopwords
    additional_stopwords = {'please', 'recommend','would','like','search','know'}  # Add your additional words here
    stop_words = set(stopwords.words('english') + list(additional_stopwords))
    filtered_tokens = [word for word in tokens if word.lower() not in stop_words]

    # Apply stemming
    ps = PorterStemmer()
    stemmed_tokens = [ps.stem(word) for word in filtered_tokens]

    # Join the stemmed tokens into a string
    processed_query = ' '.join(stemmed_tokens)

    return processed_query

@app.route('/')
def index():
    return render_template('index.html',
                           anime_name =list(most_popular_df['name'].values),
                           image =list(most_popular_df['main_picture'].values),
                           votes =list(most_popular_df['num_rating'].values),
                           rating =list(most_popular_df['avg_rating'].values),
                           url =list(most_popular_df['url'].values)
                          )
@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')
@app.route('/recommend_anime',methods =['post'])
def recommend():
    user_input = request.form.get('user_input')
    processed_query = process_query(user_input)
    g_score1 = 75
    g_score2 = 75

    g_best_match_1, score1 = process.extractOne(processed_query, pt_value)
    if score1>g_score1:
            best_match1 = g_best_match_1
            g_score1 = score1
    g_best_match_2, score2 = process.extractOne(processed_query, eng_title)
    if score2>g_score2:
        best_match2 = g_best_match_2
        g_score2 = score2
    if max(g_score1,g_score2) < 80:
        return render_template('error.html')
    #print(best_match)
    if g_score1 >= g_score2:
        best_match = best_match1
        best_match3 = best_match1
        index = pt_value.index(best_match)
    else:
        best_match = anime_url_id.loc[anime_url_id['title_english'] == best_match2, 'title'].values
        best_match3 = best_match2
        if best_match not in pt_value:
            return render_template('error.html')
        index = pt_value.index(best_match)
    
    similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1], reverse = True)[1:11]
    # print(anime_name)
    # get_main_picture(anime_name)
    data = []
    for i in similar_items:
          item = []
        #   id = anime_url.loc[anime_url['name'] == pt.index[i[0]], 'anime_id'].values
        #   temp_df = anime_url_id[id]
          #temp_df = anime_url_id[anime_url['name'] == pt.index[i[0]]]
          tem_df = anime_url[anime_url['name'] == pt_value[i[0]]]
          anime_id = tem_df['anime_id'].values[0]  # Assuming there's only one match, extract the anime_id
          temp_df = anime_url_id[anime_url_id['anime_id'] == anime_id]
          item.extend(list(tem_df['name'].values))
          item.extend(list(temp_df['main_picture'].values))
          item.extend(list(temp_df['url'].values))
          data.append(item)
    print(data)
    return render_template('recommend.html',user_input=user_input,best_match3=best_match3,data=data)
@app.route('/contact')
def contact_ui():
    return render_template('contact.html')

if __name__ == '__main__': 
    app.run(debug=True)
