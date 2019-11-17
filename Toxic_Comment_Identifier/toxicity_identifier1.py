from keras.models import load_model
import pickle
import re
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
from flask import Flask, request, render_template,jsonify
from keras import backend as K
import os

app = Flask(__name__)

def clean_comment(comment):
    #comment=df['comment_text']
    comment = comment.lower()
    comment = re.sub(r"what's", "what is ", comment)
    comment = re.sub(r"\'s", " ", comment)
    comment = re.sub(r"\'ve", " have ", comment)
    comment = re.sub(r"can't", "can not ", comment)
    comment = re.sub(r"n't", " not ", comment)
    comment = re.sub(r"i'm", "i am ", comment)
    comment = re.sub(r"\'re", " are ", comment)
    comment = re.sub(r"\'d", " would ", comment)
    comment = re.sub(r"\'ll", " will ", comment)
    comment = re.sub(r"\'scuse", " excuse ", comment)
    comment = re.sub('\W', ' ', comment)
    comment = re.sub('\s+', ' ', comment)
    comment = re.sub(r":|!|#|@|%|_|(|)|[|]|\'|\"", "", comment)
    comment = comment.strip()
    return comment






def identify_toxicity(comment):
    K.clear_session()
    model = load_model('Toxicity_Identifier_V1')
    t_file=open('tokenizer.pickle', 'rb')
    tokenizer = pickle.load(t_file)
    max_length=100
    cleaned_comment=clean_comment(comment)
    df=pd.DataFrame(columns=['cleaned_comment'])
    df['cleaned_comment']=[cleaned_comment]

    df['cleaned_comment_seq']=tokenizer.texts_to_sequences(df['cleaned_comment'])
    cleaned_comment_seq_padded = pad_sequences(df['cleaned_comment_seq'], maxlen=max_length, padding='post',truncating='post')
    p_list=[float("{0:.4f}".format(p)) for p in model.predict_proba(cleaned_comment_seq_padded)[0]]
    r=''
    r+='<b>TOXIC :</b> '+str(p_list[0])+'&nbsp ; &nbsp'
    r+='<b>SEVERE_TOXIC :</b> '+str(p_list[1])+'&nbsp ; &nbsp'
    r+='<b>OBSCENE :</b> '+str(p_list[2])+'&nbsp ; &nbsp'
    r+='<b>THREAT :</b> '+str(p_list[3])+'&nbsp ; &nbsp'
    r+='<b>INSULT :</b> '+str(p_list[4])+'&nbsp ; &nbsp'
    r+='<b>IDENTITY_HATE : </b>'+str(p_list[5])
    return r


@app.route('/')
def home():
    return render_template('toxicity_identifier.html')
        
        
@app.route('/join', methods=['GET','POST'])
def my_form_post():
    K.clear_session()
    print('Inside logic')
    text1 = request.form['text1']
    word = request.args.get('text1')
    toxicity= identify_toxicity(text1)
    result = {
        "output": toxicity
    }
    result = {str(key): value for key, value in result.items()}
    return jsonify(result=result)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=True, port=port)