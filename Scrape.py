import requests
from bs4 import BeautifulSoup
import os
import time
from collections import OrderedDict

# Set a User-Agent to mimic a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Function to scrape the main content from a blog post
def scrape_blog_content(blog_url, file):
    print(f"Scraping content from {blog_url}... ", end="")
    try:
        # Perform the HTTP request
        response = requests.get(blog_url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Write the URL of the blog post to the file
            file.write(f'URL: {blog_url}\n')

            # Write the title of the blog post to the file, if it exists
            title = soup.find('h1')
            if title:
                file.write(f'Title: {title.get_text(strip=True)}\n\n')

            # Find all relevant content elements such as headers and paragraphs
            content_elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'])

            # Write the text from the content elements to the file
            for element in content_elements:
                file.write(element.get_text(strip=True) + '\n')

            # Add a separator after each blog post's content for readability
            file.write('\n' + '-'*80 + '\n\n')

            print("Done.")
        else:
            file.write(f'Failed to retrieve {blog_url}\n')
    except requests.RequestException as e:
        print("Failed.")


# List of URLs to scrape
urls = [
    input("Please enter the main URL you want to scrape from: "),
    # Add more URLs as needed
]

# Function to scrape a page for headers, paragraphs, and blog links
def scrape_page(url):
    blog_urls = []
    try:
        # Perform the HTTP request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all 'a' tags, which define hyperlinks
            links = soup.find_all('a')

            # Extract the href attribute from each link
            hrefs = [link.get('href') for link in links if link.get('href') is not None and "blog" in link.get('href')]

            # Construct full URLs for relative links and collect them
            blog_urls = [requests.compat.urljoin(url, href) for href in hrefs]
    except requests.RequestException as e:
        print(f'Request failed: {e}')
    return blog_urls

# This will hold all the URLs that contain "blog"
all_blog_urls = []

# Loop over each URL to scrape for blog links
for url in urls:
    blog_urls = scrape_page(url)
    all_blog_urls.extend(blog_urls)

# Specify the directory you want to save the file to
output_directory = input("Please enter the directory path where you want to save the output: ")

# Check if the provided directory exists
if os.path.isdir(output_directory):
    # Change the current working directory to the specified path
    os.chdir(output_directory)
    print(f"Changed working directory to {output_directory}")
else:
    print(f"The directory {output_directory} does not exist.")
    
# Specify the path to the output file within the new directory
output_file_name = input("Please name your output file: ") + '.txt'
output_path = os.path.join(output_directory, output_file_name)

# Open the file in write mode
with open(output_path, 'w', encoding='utf-8') as file:
    # Now, for each URL in the all_blog_urls list, you can perform further scraping
    for blog_url in all_blog_urls:
        scrape_blog_content(blog_url, file)


def remove_duplicates(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # To keep track of unique content blocks
    unique_content_blocks = set()
    # To keep the final output with preserved order
    final_output = []
    # Buffer for the current content block
    current_block = []

    for line in content:
        if line.strip() == '-'*80:  # Assuming '------' is your delimiter
            # Convert block to a tuple and add to the set to remove duplicates
            block_tuple = tuple(current_block)
            if block_tuple not in unique_content_blocks:
                unique_content_blocks.add(block_tuple)
                final_output.extend(current_block + [line])  # Add the block and delimiter to the final output
            # Reset the current block
            current_block = []
        else:
            # Add the line to the current block
            current_block.append(line)

    # Write the final output back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(final_output)

# The rest of your scraping code here

# Call the remove_duplicates function after all scraping is done
output_path = "output.txt"  # The path to your output file
remove_duplicates(output_path)
print("Duplicates have been removed from the output.")
