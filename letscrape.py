import requests
from bs4 import BeautifulSoup
import urls

url = urls.url1

# Create an empty set to store the lowercase stop words
all_stop_words = set()

# List of stop words files
stop_words_files = [urls.sw1, urls.sw2, urls.sw3, urls.sw4, urls.sw5, urls.sw6]
# Load the list of positive words from a file
with open(urls.pw, 'r', encoding='iso-8859-1') as positive_words_file:
    positive_words = set(positive_words_file.read().splitlines())
with open(urls.nw, 'r', encoding='iso-8859-1') as negative_words_file:
    negative_words = set(negative_words_file.read().splitlines())

# Iterate through each stop words file and add lowercase stop words to the set
for stop_words_file_name in stop_words_files:
    with open(stop_words_file_name, 'r', encoding='iso-8859-1') as stop_words_file:
        lowercase_stop_words = set(word.lower() for word in stop_words_file.read().splitlines())
        all_stop_words.update(lowercase_stop_words)

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Identify and remove header and footer elements
    header = soup.find('header')  # Replace with the correct tag for header
    if header:
        header.extract()
    
    footer = soup.find('footer')  # Replace with the correct tag for footer
    if footer:
        footer.extract()
    
    # Extract the remaining text
    all_text = soup.get_text()
    
    # Remove blank lines from the text
    lines = all_text.split('\n')
    non_blank_lines = [line for line in lines if line.strip() != '']
    
    # Join the non-blank lines back together
    cleaned_text = '\n'.join(non_blank_lines)
    
    # Exclude the first 10 characters, first 160 lines, and the last 40 lines
    characters_to_exclude_start = 21
    lines_to_exclude_start = 162
    lines_to_exclude_end = 42
    
    cleaned_text_lines = cleaned_text.split('\n')[lines_to_exclude_start:-lines_to_exclude_end]
    cleaned_text_lines[0] = cleaned_text_lines[0][characters_to_exclude_start:]
    
    final_text = '\n'.join(cleaned_text_lines)
    
    # Tokenize the words in the extracted text
    words = final_text.split()
    
    # Filter out stop words (case-insensitive)
    filtered_words = [word for word in words if word.lower() not in all_stop_words]
    
    # Reconstruct the final cleaned text
    final_cleaned_text = ' '.join(filtered_words)
    
    # Count positive words
    positive_word_count = sum(1 for word in filtered_words if word.lower() in positive_words)
    
    # Count negative words
    negative_word_count = sum(1 for word in filtered_words if word.lower() in negative_words)
    
    # Define the output file path
    output_file_path = 'extracted_text.txt'
    
    # Write the final cleaned text to the output file
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write(final_cleaned_text)
    
    print(f"Cleaned and extracted text (without stop words) saved to {output_file_path}")
    print(positive_word_count, negative_word_count)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
