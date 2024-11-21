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

	all_text_file = "all_text.txt"

	# Check if the directory is a .txt file
	if directory.endswith('.txt'):
		# Read lines from the text file
		with open(directory, encoding='utf-8', errors='ignore') as f:
			lines = f.readlines()
			if not lines:
				print("No text found in the .txt file.")
				exit()
			for line in lines:
				text_match = line.strip()  # Remove leading/trailing whitespace
				if text_match:
					row = translate_text(text_match, translations)  # Translate and get a row
					writer.writerow(row)  # Write the row to the CSV file
	else:
		# Check if all_text.txt exists in the directory
		all_text_path = os.path.join(directory, all_text_file)
		if os.path.isfile(all_text_path):
			print("Found existing text file, skipping project iteration.")
			with open(all_text_path, encoding='utf-8', errors='ignore') as f:
				lines = f.readlines()
				if not lines:
					print("No text found in the .txt file.")
					exit()
				for line in lines:
					text_match = line.strip()
					if text_match:
						row = translate_text(text_match, translations)
						writer.writerow(row)
		else:
			# Iterate through the directory and find the text in scene files
			any_scene_files = False
			all_text = []  # Initialize the list of all text found
			for root, dirs, files in os.walk(directory):
				for file in files:
					if file.endswith('.gd') or file.endswith('.tscn'):
						any_scene_files = True
						file_path = os.path.join(root, file)
						with open(file_path, encoding='utf-8', errors='ignore') as f:
							content = f.read()
							text_matches = text_pattern.findall(content)  # Find all text matches
							for text_match in text_matches:
								all_text.append(text_match)  # Add matches to the list

			if not any_scene_files:
				print("No .gd or .tscn files were found in the directory. Please check the directory path.")
				exit()

			# Write all found text to a combined file
			with open(all_text_file, 'w', encoding='utf-8') as f:
				if not all_text:
					print("No text found in the project files.")
					exit()
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

