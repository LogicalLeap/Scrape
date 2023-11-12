import requests
from bs4 import BeautifulSoup
import os

# Ask the user for the directory path
new_directory = input("Please enter the directory path: ")

# Check if the provided directory exists
if os.path.isdir(new_directory):
    # Change the current working directory to the specified path
    os.chdir(new_directory)
    print(f"Changed working directory to {new_directory}")
else:
    print(f"The directory {new_directory} does not exist.")

# Function to scrape a page for headers, paragraphs, and blog links
def scrape_page(url):
    try:
        # Perform the HTTP request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all header and paragraph elements
            index_content = soup.find_all(['h1', 'h2', 'h3', 'p', 'img'])  # if the main content is in headers and paragraphs


            # Print the text from each header and paragraph
            # Extract and print the text from the main content
            for element in index_content:
                print(element.get_text(strip=True))

            # Find all 'a' tags, which define hyperlinks
            links = soup.find_all('a')

            # Extract the href attribute from each link
            hrefs = [link.get('href') for link in links if link.get('href') is not None and "blog" in link.get('href')]

            # Construct full URLs for relative links and collect them
            blog_urls = [requests.compat.urljoin(url, href) for href in hrefs]

            # Return the list of blog URLs
            return blog_urls
        else:
            print(f'Failed to retrieve {url}')
            return []
    except requests.RequestException as e:
        print(f'Request failed: {e}')
        return []

# Function to scrape the main content from a blog post
def scrape_blog_content(blog_url):
    try:
        # Perform the HTTP request
        response = requests.get(blog_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the content of the response using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')

            # You might need to adjust the selectors depending on the site's structure
            # Here are some common examples:
            # main_content = soup.find('article')  # if the main content is within <article> tags
            # main_content = soup.find('div', class_='post-content')  # if the content is in a <div> with a specific class
            main_content = soup.find_all(['h1', 'h2', 'h3', 'p', 'img'])  # if the main content is in headers and paragraphs

            # Extract and print the text from the main content
            for element in main_content:
                print(element.get_text(strip=True))
        else:
            print(f'Failed to retrieve {blog_url}')
    except requests.RequestException as e:
        print(f'Request failed: {e}')

# List of URLs to scrape
urls = [
    'https://vidiq.com/blog/category/how-to-get-more-views/',
    # Add more URLs as needed
]

# This will hold all the URLs that contain "blog"
all_blog_urls = []

# Loop over each URL to scrape for blog links
for url in urls:
    blog_urls = scrape_page(url)
    all_blog_urls.extend(blog_urls)

# Print each URL that contains "blog"
for blog_url in all_blog_urls:
    print(blog_url)

# Now, for each URL in the all_blog_urls list, you can perform further scraping
for blog_url in all_blog_urls:
    print(f'Scraping content from {blog_url}')
    scrape_blog_content(blog_url)

    # Open the file in write mode
with open('E:\Game Dev\py\Scrape', 'w', encoding='utf-8') as file:
    # Loop over each URL to scrape for blog links
    for url in urls:
        blog_urls = scrape_page(url)
        all_blog_urls.extend(blog_urls)

    # Now, for each URL in the all_blog_urls list, you can perform further scraping
    for blog_url in all_blog_urls:
        file.write(f'Scraping content from {blog_url}\n')
        scrape_blog_content(blog_url)
