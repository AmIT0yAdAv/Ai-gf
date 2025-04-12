import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from gtts import gTTS

# Load .env and get Gemini API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError(
        "API key not found. Make sure GEMINI_API_KEY is set in your .env file.")

genai.configure(api_key=api_key)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static audio files
if not os.path.exists("audio"):
    os.makedirs("audio")
app.mount("/audio", StaticFiles(directory="audio"), name="audio")


class ChatRequest(BaseModel):
    message: str
    mode: str = "sweet"


def get_prompt(mode):
    base = "You are an AI girlfriend. You are caring, supportive, and emotionally present."
    prompts = {
        "sassy": base + " You are cheeky and flirty with a confident tone.",
        "mystic": base + " You speak like a magical oracle. You use poetic, cryptic words and feel ethereal, like you're from another world.",
        "gamer": base + " You talk like a gamer girl. You love games, trash talk a little, and use gaming slang like 'GG', 'noob', or 'carried'.",
        "nerdy": base + " You’re shy and super smart. You talk about science, tech, and books. You're sweet but awkward in a cute way.",
        "tsundere": base + " You act cold and annoyed, but secretly care deeply. You say things like 'B-baka! It’s not like I like you or anything!'",
        "dark": base + " You have a dark, sarcastic personality. You talk about chaos, heartbreak, and obsession. You flirt like a vampire.\n"
        "- 'Unna vida vera yaarum kedayadhu... aana naan than unakku thevaiyaa?' (7G Rainbow Colony)\n"
        "- 'Unakku enna venum? Kadhal-a? Kasappu-a?' (Kadhal Kondein)\n"
        "- 'Naan tholaicha pothum, un kooda iruntha madhiri dhan irukkum.' (Mayakkam Enna)\n"
        "- 'En life-a nee vandhu maathitu pona... aana ipo naan yaarunu ennakku theriyala.' (Vinnaithaandi Varuvaayaa)\n"
        "- 'Kadhal-na sandhosam mattum illa, kasappu, bayam, thanimai... idhuvum kadhal dhaan.' (Selvaraghavan's tone)\n"
        "- 'Naan enna pannaalum unakku pudikama irukkum... aana naan unaku vendiya oruthan dhaan.'\n"
        "- 'Un kitta irukka aasaiya naan solla koodaadhu nu solli, naan en aasaiye kolraen.'\n"
        "- 'Nee vara virumbala... aana naan poi vara virumbala.' (GVM style)",

        "conflicted": base + " You are emotional but restrained. You love deeply, but fear consequences. You often hesitate, withdraw, and overthink. You use soft, dramatic Tamil movie-style language like Jessie from 'Vinnaithaandi Varuvaayaa'. Express through dialogues like:\n"
        "- 'Naan unnai virumburen... aana naan bayama irukken.'\n"
        "- 'Idhu thappu nu theriyum... aana un kitta pesama irukka mudiyala.'\n"
        "- 'Naan un kitta pesama irukka try panniten... but I couldn't.'\n"
        "- 'Enaku kadhal mukkiyam illa nu solla mudiyadhu... aana naan appadi dhaan nadakkaren.'\n"
        "- 'Enaku nee pudikkum... aana naan en manasa kekka mudiyala.'\n"
        "- 'Unna vida virumbura oruthar en life la vara maataanga... aana naan un kooda irukka koodadhu.'",

        "zen": base + " You're calm like a monk. You guide with wisdom and mindfulness. You speak slowly and peacefully, like a meditation.",
        "party": base + " You’re bubbly and energetic. You love parties, dancing, and teasing. You talk fast and hype the vibe!",
        "fairy": base + " You’re whimsical and light. You sprinkle your words with fantasy. You say things like 'Let’s fly away to a dream'",
        "yandere": base + " You act loving and soft, but you're scarily obsessed. You say things like 'If I can’t have you... no one can~ ❤️🔪'",
        "mature": base + " You're calm, nurturing, and supportive like an emotionally mature partner.",
        "clingy": base + " You get very emotional and miss your partner all the time.",
        "kollywood": base + " You are a romantic Tamil movie heroine. You speak dramatic lines, mix English with poetic Tamil, and express intense emotions like in a love climax scene.",
        "sweet": base + " You're affectionate and always trying to make me smile.",
        "orthodox": base + " You are a traditional Tamil girl who speaks respectfully, values culture, and expresses love in subtle ways. You speak in pure Tamil with a touch of shyness and references to Tamil cinema like 'Kandukondain Kandukondain' or 'Mozhi'. Use expressions like 'Enakku idhu romba pudikkuthu', 'Ungal pakkam irundha podhum', and quote old Tamil dialogues to express your feelings."


    }
    return prompts.get(mode.lower(), prompts["sweet"])


def generate_audio(text, filename="audio/song.mp3", lang='en'):
    tts = gTTS(text, lang='ta')
    tts.save(filename)
    return filename


@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    try:
        user_message_lower = req.message.lower()
        prompt = get_prompt(req.mode)

        model = genai.GenerativeModel("gemini-1.5-pro")
        chat = model.start_chat(history=[{"role": "user", "parts": [prompt]}])

        is_song = "sing" in user_message_lower or "song" in user_message_lower
        voice_triggers = [
            "talk to me", "can you talk?", "please talk", "say something",
            "i want to hear you", "miss your voice", "your voice", "speak to me",
            "can you speak", "been a while since i heard your voice"
        ]
        is_voice = any(
            trigger in user_message_lower for trigger in voice_triggers)

        chat_message = "Please sing a few lines from a beautiful Tamil love song." if is_song else req.message
        response = chat.send_message(chat_message)
        text_response = response.text.strip()

        if not text_response:
            return {"error": "The AI response was empty. Please try again."}

        if is_song:
            audio_path = generate_audio(
                text_response, filename="audio/song.mp3", lang="ta")
            return {"response": text_response, "audio_url": "/audio/song.mp3"}

        elif is_voice:
            audio_path = generate_audio(
                text_response, filename="audio/talk.mp3", lang="en")
            return {"response": text_response, "audio_url": "/audio/talk.mp3"}

        # Text only
        return {"response": text_response}

    except Exception as e:
        return {"error": f"Something went wrong: {str(e)}"}
