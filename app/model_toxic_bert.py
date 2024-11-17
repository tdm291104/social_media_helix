# from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
# from pydantic import BaseModel

# class TextRequest(BaseModel):
#     text: str

# model_name_toxic = "unitary/toxic-bert"
# tokenizer_toxic = AutoTokenizer.from_pretrained(model_name_toxic)
# model_toxic = AutoModelForSequenceClassification.from_pretrained(model_name_toxic)

# toxic_pipeline = pipeline("text-classification", model=model_toxic, tokenizer=tokenizer_toxic)