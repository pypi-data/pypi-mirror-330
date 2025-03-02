from .models import load_sentiment_model
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import torch.nn as nn
import warnings
import logging
import pandas as pd
from tabulate import tabulate
import json
# Suppress warnings
warnings.filterwarnings("ignore")
# Suppress Hugging Face & PyTorch logging messages
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("torch").setLevel(logging.ERROR)
logging.getLogger().setLevel(logging.ERROR)

def sentiment_sentence(sentence):
    # Tokenize input text
    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
    inputs = tokenizer(sentence, truncation=True, padding='max_length', max_length=512, return_tensors='pt')
    
    # Run through the model
    with torch.no_grad():
        model = load_sentiment_model(model_filename="sentence_model.pt")
        outputs = model(**inputs)  # Model returns the full output, including logits

    # Extract logits and apply softmax
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)

    # Get the predicted class
    predicted_class = torch.argmax(probabilities, dim=1).item()
    class_mapping = {0: "negative", 1: "neutral", 2: "positive"}
    sentiment = class_mapping.get(predicted_class, "Unknown")

    return sentiment

def sentiment_document(overall_document, j_son=True):
    if j_son:
        overall_document = " | ".join(overall_document.values())
        
    # Tokenize input text
    tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
    inputs = tokenizer(overall_document, truncation=True, padding='max_length', max_length=512, return_tensors='pt')
    
    # Run through the model
    with torch.no_grad():
        model = load_sentiment_model(model_filename="document_model.pt")
        outputs = model(**inputs)  # Model returns the full output, including logits

    # Extract logits and apply softmax
    logits = outputs.logits
    probabilities = torch.nn.functional.softmax(logits, dim=1)

    # Get the predicted class
    predicted_class = torch.argmax(probabilities, dim=1).item()
    class_mapping = {0: "negative", 1: "neutral", 2: "positive"}
    sentiment = class_mapping.get(predicted_class, "Unknown")

    return sentiment

def sentiment_summary(dict):

    new_dict={}
    i=0
    for key in dict:
        i+=1
        new_dict[f"sentence {i}"] = sentiment_sentence(dict[key])
    #sentiment analysis at document level
    new_dict["Overall"]=sentiment_document(dict)
    table = tabulate(new_dict.items(), headers=["Categorisation", "Sentiment"], tablefmt="grid")
    return table


def query_intent(sentence):
        # Tokenize input text
    # Tokenize input text
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')  # Use 'uncased' to match the model
    inputs = tokenizer(sentence, truncation=True, padding='max_length', max_length=512, return_tensors='pt')
    
    # Extract only the required inputs
    input_ids = inputs['input_ids']
    attention_mask = inputs['attention_mask']
    # Run through the model
    with torch.no_grad():
        model=load_sentiment_model(model_filename="query_model.pt")
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)  # Pass only the required inputs

    # Apply softmax
    probabilities = torch.nn.functional.softmax(outputs, dim=1)

    # Get the predicted class
    predicted_class = torch.argmax(probabilities, dim=1).item()
    query_mapping = {0: "Course Overview and Information", 1: "Course Assessment" ,
    2: "Checking Announcement", 3: "Request for Permission", 4: "Learning Course Content",
    5: "Class Schedule", 6: "Greetings", 7: "Ending", 8: "Casual Chat" , 9: "No Query"}

    intent = query_mapping.get(predicted_class, "Unknown")

    return intent

def chat_summary(document):
    new_data = []
    i = 0

    for key in document:
        i += 1
        sentiment = sentiment_sentence(document[key])
        intent = query_intent(document[key])
        new_data.append([f"Sentence {i}", sentiment, intent])

    # Add document-level sentiment analysis
    new_data.append(["Overall", sentiment_document(document), "NA"])

    # Convert list into a table
    table = tabulate(new_data, headers=["Categorisation", "Sentiment", "Query Intent"], tablefmt="grid")
    return table

def conversion(chatlog, num_of_chats):

    conversations = chatlog.get("chatlog", [] ) # Ensure chatlog exists

    flattened_records = []

    for conv in conversations[:num_of_chats]:
        for msg in conv.get("messages", []):  # Ensure messages exist
            record = {
                "_id": conv["_id"]["$oid"],
                "Person": conv["Person"],
                "stime_text": conv["stime"]["text"],
                "stime_timestamp": conv["stime"]["timestamp"],
                "last_interact_text": conv["last_interact"]["text"],
                "last_interact_timestamp": conv["last_interact"]["timestamp"],
                "llm_deployment_name": conv.get("llm_deployment_name", None),
                "llm_model_name": conv.get("llm_model_name", None),
                "vectorstore_index": conv.get("vectorstore_index", None),
                "overall_cost": conv.get("overall_cost", {}).get("overall_cost", None),
                "overall_tokens": conv.get("overall_cost", {}).get("overall_tokens", None),
                "role": msg.get("role", None),
                "content": msg.get("content", None),
                "recorded_on_text": msg.get("recorded_on", {}).get("text", None),
                "recorded_on_timestamp": msg.get("recorded_on", {}).get("timestamp", None),
                "token_cost": msg.get("token_cost", {}).get("cost", 0),  # Default 0 if missing
                "tokens": msg.get("token_cost", {}).get("tokens", 0)  # Default 0 if missing
            }
            flattened_records.append(record)

    df = pd.DataFrame(flattened_records)

    # Convert timestamps to readable datetime format
    df["stime_timestamp"] = pd.to_datetime(df["stime_timestamp"], unit="s", errors="coerce")
    df["last_interact_timestamp"] = pd.to_datetime(df["last_interact_timestamp"], unit="s", errors="coerce")
    df["recorded_on_timestamp"] = pd.to_datetime(df["recorded_on_timestamp"], unit="s", errors="coerce")
    #df = df[df["role"] != "ai"]
    df.loc[df["role"] == "user", "user_sentiment"] = df["content"].apply(sentiment_sentence)
    df.loc[df["role"] == "user", "query_intent"] = df["content"].apply(query_intent)
    df["conversation_id"]=pd.factorize(df["Person"])[0] + 1
    df["previous_query_intent"] = None

    # Loop through the rows and assign previous 'user' content to the current 'user' row
    for i in range(1, len(df)):
        if df.loc[i, "role"] == "user":
            # Look backward and find the previous row with 'role' == 'user'
            previous_user_row = df.loc[:i-1][df["role"] == "user"].iloc[-1:]
            if not previous_user_row.empty:
                df.loc[i, "previous_query_intent"] = previous_user_row["query_intent"].values[0]
        # Check if the current value is not None and if the conversation_id is different from the previous row
            if df.loc[i, "previous_query_intent"] is not None and df.loc[i, "conversation_id"] != df.loc[i-1, "conversation_id"]:
                # Set the value to None if the condition is met
                df.loc[i, "previous_query_intent"] = None

    df["overall_chat"] = df.groupby('conversation_id')['content'].transform(
        lambda x: ' | '.join(x[x.index.isin(df[df['role'] == 'user'].index)]))
    first_rows = df.groupby('conversation_id').head(1).index

    # Apply sentiment analysis only to the first row of each unique conversation_id
    df['chat_sentiment'] = df.apply(
        lambda row: sentiment_document(row['overall_chat'], False) if row.name in first_rows else None, 
        axis=1
    )
    df["recorded_on_text"] = pd.to_datetime(df["recorded_on_text"])

    # Initialize a new column for time differences
    df["chatbot_response_time"] = None

    # Loop through the rows and compute time difference for 'user' rows with same conversation_id
    for i in range(len(df) - 1):  # Loop up to second-to-last row
        if df.loc[i, "role"] == "user" and df.loc[i, "conversation_id"] == df.loc[i+1, "conversation_id"]:
            # Calculate the time difference in seconds by subtracting the current row's recorded_on_text from the next row's
            df.loc[i, "chatbot_response_time"] = (df.loc[i+1, "recorded_on_text"] - df.loc[i, "recorded_on_text"]).total_seconds()
    conversation_times = df.groupby("conversation_id")["recorded_on_text"].agg(lambda x: (x.max() - x.min()).total_seconds())

    # Merge the conversation time back into the DataFrame
    df = df.merge(conversation_times.rename("overall_conversation_time"), on="conversation_id")

    return df

