import openai

openai.api_key ="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"
class chatGPT:
    def get_api_response(self, prompt: str) -> str or None:
        text: str or None = None

        try:
            response: dict = openai.Completion.create(
                model='text-davinci-003',
                prompt=prompt,
                temperature=0.9,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0.6,
                stop=[' Manusia:', ' AI:']
            )

            choices: dict = response.get('choices')[0]
            text = choices.get('text')

        except Exception as e:
            print('ERROR:', e)

        return text
    
    def get_bot_response(self, pl: list[str]) -> str:
        prompt  = pl
        bot_response: str = self.get_api_response(prompt)

        if bot_response:
            pos: int = bot_response.find('\nAI: ')
            bot_response = bot_response[pos + 5:]
        else:
            bot_response = 'Terjadi Kesalahan...'

        return bot_response
    
    def prompt(self, text):
        msg = 'Semua yang saya tanyakan adalah tentang padi dan kamu hanya boleh menjawab tentang padi\n'
        msg += '\nManusia: apa itu bacterial_panicle_blight?'
        msg += '\nAI: Bacterial panicle blight (BPH) adalah penyakit bakteri yang menyerang tanaman padi. Penyakit ini disebabkan oleh bakteri Xanthomonas oryzae pv. oryzae. BPH dapat menyebabkan penurunan hasil panen yang signifikan, hingga mencapai 80%.'
        msg += f'\nManusia: {text}'

        return self.get_bot_response(msg)