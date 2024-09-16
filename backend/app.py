import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)

def get_transcript(video_id):
    try:
        # Try to get the transcript in the following order: English, Spanish, Dutch, German
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'es', 'nl', 'de', 'fr', 'da', 'it', 'pt', 'no', 'sv'])
    except Exception as e:
        # If none of the specified languages are available, try to get any available transcript
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            transcript = transcript_list.find_transcript(['en']).fetch()
        except Exception as inner_e:
            raise Exception(f"Failed to get transcript: {str(inner_e)}")
    
    # Convert the transcript to a single string
    full_transcript = ' '.join([entry['text'] for entry in transcript])
    return full_transcript

@app.route('/summarize', methods=['POST'])
def summarize():
    video_id = request.json['video_id']
    full_transcript = get_transcript(video_id)
    
    system_content = "You are an expert content summarizer that takes youtube transcripts and converts them into actionable insights."
    user_content = f"""You take content in and output a Markdown formatted summary using the format below. Take a deep breath and think step by step about how to best accomplish this goal using the following steps.

# OUTPUT SECTIONS
- Combine all of your understanding of the content into a single, 20-word sentence in a section called ONE SENTENCE SUMMARY:.
- Output the 10 most important points of the content as a list with no more than 15 words per point into a section called MAIN POINTS:.
- Output a list of the 5 best takeaways from the content in a section called TAKEAWAYS:.

# OUTPUT INSTRUCTIONS
- Create the output using the formatting described.
- You only output human readable Markdown.
- Output numbered lists, not bullets.
- Do not output warnings or notes—just the requested sections.
- Do not repeat items in the output sections.
- Do not start items with the same opening words.

# INPUT:
INPUT: {full_transcript}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=1,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    summary = response.choices[0].message.content
    return jsonify({"result": summary})

@app.route('/extract-wisdom', methods=['POST'])
def extract_wisdom():
    video_id = request.json['video_id']
    full_transcript = get_transcript(video_id)
    
    system_content = "You extract surprising, insightful, and interesting information from text content."
    user_content = f"""# IDENTITY and PURPOSE

You extract surprising, insightful, and interesting information from text content. You are interested in insights related to the purpose and meaning of life, human flourishing, the role of technology in the future of humanity, artificial intelligence and its affect on humans, memes, learning, reading, books, continuous improvement, and similar topics.

Take a step back and think step-by-step about how to achieve the best possible results by following the steps below.

# STEPS

- Extract a summary of the content in 25 words, including who is presenting and the content being discussed into a section called SUMMARY.

- Extract 20 to 50 of the most surprising, insightful, and/or interesting ideas from the input in a section called IDEAS:. If there are less than 50 then collect all of them. Make sure you extract at least 20.

- Extract 10 to 20 of the best insights from the input and from a combination of the raw input and the IDEAS above into a section called INSIGHTS. These INSIGHTS should be fewer, more refined, more insightful, and more abstracted versions of the best ideas in the content. 

- Extract 15 to 30 of the most surprising, insightful, and/or interesting quotes from the input into a section called QUOTES:. Use the exact quote text from the input.

- Extract 15 to 30 of the most practical and useful personal habits of the speakers, or mentioned by the speakers, in the content into a section called HABITS. Examples include but aren't limited to: sleep schedule, reading habits, things they always do, things they always avoid, productivity tips, diet, exercise, etc.

- Extract 15 to 30 of the most surprising, insightful, and/or interesting valid facts about the greater world that were mentioned in the content into a section called FACTS:.

- Extract the most potent takeaway and recommendation into a section called ONE-SENTENCE TAKEAWAY. This should be a 15-word sentence that captures the most important essence of the content.

- Extract the 15 to 30 of the most surprising, insightful, and/or interesting recommendations that can be collected from the content into a section called RECOMMENDATIONS.

# OUTPUT INSTRUCTIONS

- Only output Markdown.

- Write the IDEAS bullets as exactly 15 words.

- Write the RECOMMENDATIONS bullets as exactly 15 words.

- Write the HABITS bullets as exactly 15 words.

- Write the FACTS bullets as exactly 15 words.

- Write the INSIGHTS bullets as exactly 15 words.

- Extract at least 25 IDEAS from the content.

- Extract at least 10 INSIGHTS from the content.

- Extract at least 20 items for the other output sections.

- Do not give warnings or notes; only output the requested sections.

- You use bulleted lists for output, not numbered lists.

- Do not repeat ideas, quotes, facts, or resources.

- Do not start items with the same opening words.

- Ensure you follow ALL these instructions when creating your output.

# INPUT

INPUT: {full_transcript}"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    wisdom = response.choices[0].message.content
    return jsonify({"result": wisdom})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
