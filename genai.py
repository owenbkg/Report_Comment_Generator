# Example: reuse your existing OpenAI setup
from openai import OpenAI


class ai_model():
  def __init__(self):
    self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

  def api_comment_generation(self, name, sentences):
    completion = self.client.chat.completions.create(
      model="model-identifier",
      #message to the AI model 
      messages=[
        {"role": "system", "content": "Use a professional, objective,\
          and constructive tone to link the four provided sentences together. \
        Mention the student's name in the first sentence, and infer their gender and use pronouns\
        such as he or she in the later sentences. Do it in one paragraph."},
        {"role": "user", "content": "The name of the student is " + name + " and the sentences are " + '.'.join(sentences)}
      ],
      #setting a lower temperature to reduce randomness (So the comments themselves remain more or less unchagned)
      temperature=0.3,
    )
    #return only the message content
    return (completion.choices[0].message.content)

