# Godot_Translator_CSV_Python_Script
A python script that goes through your godot project folder, pulls all the text, translates them into your desired language, and saves them as a csv file

# Requirements
```
pip install deep-translator
```

# Supported languages
Afrikaans (af)
Albanian (sq)
Amharic (am)
Arabic (ar)
Armenian (hy)
Assamese (as)
Aymara (ay)
Azerbaijani (az)
Bambara (bm)
Basque (eu)
Belarusian (be)
Bengali (bn)
Bhojpuri (bho)
Bosnian (bs)
Bulgarian (bg)
Catalan (ca)
Cebuano (ceb)
Chichewa (ny)
Chinese Simplified (zh-CN)
Chinese Traditional (zh-TW)
Corsican (co)
Croatian (hr)
Czech (cs)
Danish (da)
Dhivehi (dv)
Dogri (doi)
Dutch (nl)
English (en)
Esperanto (eo)
Estonian (et)
Ewe (ee)
Filipino (tl)
Finnish (fi)
French (fr)
Frisian (fy)
Galician (gl)
Georgian (ka)
German (de)
Greek (el)
Guarani (gn)
Gujarati (gu)
Haitian Creole (ht)
Hausa (ha)
Hawaiian (haw)
Hebrew (iw)
Hindi (hi)
Hmong (hmn)
Hungarian (hu)
Icelandic (is)
Igbo (ig)
Ilocano (ilo)
Indonesian (id)
Irish (ga)
Italian (it)
Japanese (ja)
Javanese (jw)
Kannada (kn)
Kazakh (kk)
Khmer (km)
Kinyarwanda (rw)
Konkani (gom)
Korean (ko)
Krio (kri)
Kurdish Kurmanji (ku)
Kurdish Sorani (ckb)
Kyrgyz (ky)
Lao (lo)
Latin (la)
Latvian (lv)
Lingala (ln)
Lithuanian (lt)
Luganda (lg)
Luxembourgish (lb)
Macedonian (mk)
Maithili (mai)
Malagasy (mg)
Malay (ms)
Malayalam (ml)
Maltese (mt)
Maori (mi)
Marathi (mr)
Meiteilon Manipuri (mni-Mtei)
Mizo (lus)
Mongolian (mn)
Myanmar (my)
Nepali (ne)
Norwegian (no)
Odia (Oriya) (or)
Oromo (om)
Pashto (ps)
Persian (fa)
Polish (pl)
Portuguese (pt)
Punjabi (pa)
Quechua (qu)
Romanian (ro)
Russian (ru)
Samoan (sm)
Sanskrit (sa)
Scots Gaelic (gd)
Sepedi (nso)
Serbian (sr)
Sesotho (st)
Shona (sn)
Sindhi (sd)
Sinhala (si)
Slovak (sk)
Slovenian (sl)
Somali (so)
Spanish (es)
Sundanese (su)
Swahili (sw)
Swedish (sv)
Tajik (tg)
Tamil (ta)
Tatar (tt)
Telugu (te)
Thai (th)
Tigrinya (ti)
Tsonga (ts)
Turkish (tr)
Turkmen (tk)
Twi (ak)
Ukrainian (uk)
Urdu (ur)
Uyghur (ug)
Uzbek (uz)
Vietnamese (vi)
Welsh (cy)
Xhosa (xh)
Yiddish (yi)
Yoruba (yo)
Zulu (zu)

#Actual Code
```
#pip install deep-translator

### PYTHON SCRIPT TO TRANSLATE TEXT IN SCENE FILES ###

### I RECOMMEND RUNNING THIS ON A COPY OF YOUR PROJECT ###

import os
import re
import csv
from deep_translator import GoogleTranslator

# Set the directory path
# You can make this a folder containing your project or a .txt file if you already have the text extracted
directory = 'YOUR\\DIRECTORY\\PATH'

# Set the languages to translate to
translations = ["es", "fr", "de", "", ""]

# Set the regular expression to match text in scene files
text_pattern = re.compile(r'text\s*=\s*\"(.*?)\"')

def translate_text(text_match, translations):
	"""
	Translate the given text to each of the target languages specified in the translations list.
	"""
	row = ['', text_match]  # Start a row with a placeholder for 'Key' and the original text
	for lang in translations:
		if lang:
			try:
				# Initialize the GoogleTranslator for the target language
				translator = GoogleTranslator(source='en', target=lang[:2].lower())
				translation = translator.translate(text_match)  # Translate the text
				words = text_match.split()  # Split original text into words
				translated_words = translation.split()  # Split translated text into words
				
				# Adjust the capitalization of the translated words to match the original
				for i, word in enumerate(words):
					if word.istitle():
						translated_words[i] = translated_words[i].capitalize()
					elif word.isupper():
						translated_words[i] = translated_words[i].upper()
					elif word.islower():
						translated_words[i] = translated_words[i].lower()
					else:
						# Preserve original word's capitalization pattern
						translated_words[i] = ''.join(
							[char.upper() if original_char.isupper() else char.lower()
							 for char, original_char in zip(translated_words[i], word)]
						)
				translation = ' '.join(translated_words)  # Join the adjusted words back into a string
			except Exception as e:
				# Handle translation errors
				print(f"Skipping text: {text_match}")
				print(f"Error: {e}")
				translation = ''
			row.append(translation)  # Append the translation to the row
			print(f"Found text: {text_match}")
			print(f"{lang} translation: {translation}")
	return row

# Create the results file
with open('translations.csv', 'w', newline='', encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile)
	# Write the header row
	header = ['Key', 'English'] + [lang for lang in translations if lang]
	writer.writerow(header)

	# Check if the directory is a .txt file
	if directory.endswith('.txt'):
		# Read lines from the text file
		with open(directory, encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			for line in lines:
				text_match = line.strip()  # Remove leading/trailing whitespace
				if text_match:
					row = translate_text(text_match, translations)  # Translate and get a row
					writer.writerow(row)  # Write the row to the CSV file
	else:
		all_text_file = "all_text.txt"
		all_text = []
		# Iterate through the directory and find the text in scene files
		for root, dirs, files in os.walk(directory):
			for file in files:
				if file.endswith('.gd') or file.endswith('.tscn'):
					file_path = os.path.join(root, file)
					with open(file_path, encoding='utf-8', errors='ignore') as f:
						content = f.read()
						text_matches = text_pattern.findall(content)  # Find all text matches
						for text_match in text_matches:
							all_text.append(text_match)  # Add matches to the list

		# Write all found text to a combined file
		with open(all_text_file, 'w', encoding='utf-8') as f:
			for line in all_text:
				f.write(line + "\n")

		# Read lines from the combined text file and translate
		with open(all_text_file, encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			for line in lines:
				text_match = line.strip()
				if text_match:
					row = translate_text(text_match, translations)
					writer.writerow(row)


```
