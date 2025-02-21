# features/spam_detection.py
import nltk
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Download required NLTK data
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Load stopwords and punctuation
stop_words = set(stopwords.words('english'))
punctuation = string.punctuation

# Text preprocessing function
def preprocess_text(text):
    # Tokenize text
    tokens = word_tokenize(text.lower())

    # Remove stop words and punctuation
    filtered_tokens = [word for word in tokens if word not in stop_words and word not in punctuation]

    # Join tokens back into a string
    return ' '.join(filtered_tokens)

# Create the ML pipeline
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(preprocessor=preprocess_text)),  # Apply text preprocessing within TF-IDF
    ('classifier', MultinomialNB()),
])

# Sample training data (replace with your dataset)
train_data = [
    ("Free entry in 2 a wkly comp to win FA Cup final tkts 21st May 2005. Text FA to 87121 to receive entry question(std txt rate)T&C's apply 08452810075over18's", "spam"),
    ("URGENT! You have won a 1 week FREE membership in our £100000 Prize Jackpot! Txt the word: CLAIM to No: 81010 T&C www.dbuk.net LCCLTD POBOX 4403LDNW1A7RW18", "spam"),
    ("I've been searching for the right words to thank you for this breather. I promise i wont take your help for granted and will fulfil my promise. You have been wonderful and a blessing at all times", "ham"),
    ("Hey whats up? You and me we're both getting porked tonight.", "ham"),
    ("Had your mobile 11 months or more? U R entitled to update to the latest colour mobiles with camera for Free! Call The Mobile Update Co FREE on 08002986030", "spam"),
    ("SIX chances to win CASH! From 100 to 20,000 pounds txt> CSH11 and send to 87575. Cost 150p/day, 6days 16+ TsandCs apply Reply HL 4 info", "spam"),
    ("England v Macedonia - dont miss the goals/red cards ! WAP> GETPOLYS< Get fantastic pics www.pics4u.com 16+", "spam"),
    ("Is that seriously how you spell his name?", "ham"),
    ("I‘m going to try for 2 months ha ha only joking", "ham"),
    ("So ü pay first lar... Then when is da stock comping?", "ham"),
    ("Aft i finish my lunch then i go str down lor. Ard 3 smth like dat. U finish ur lect already?", "ham")
]

X_train = [text for text, label in train_data]
y_train = [label for text, label in train_data]

# Train the pipeline
pipeline.fit(X_train, y_train)

def check_spam(text):
    # Preprocess the input text
    processed_text = preprocess_text(text)
    
    # Use the pipeline to predict whether the text is spam
    prediction = pipeline.predict([text])[0]
    
    # Return True if the prediction is 'spam', False otherwise
    return prediction == 'spam'
