import pandas as pd
from collections import Counter
from urllib.parse import urlparse
import os
import csv
import sqlite3
import shutil
import webbrowser  # Import the webbrowser module

def get_chrome_profile_path():
    home_directory = os.path.expanduser("~")
    return os.path.join(home_directory, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default')

def backup_and_open_history_db():
    try:
        # Construct the path to the Chrome History database
        history_db_path = os.path.join(get_chrome_profile_path(), 'History')

        # Check if the History file exists
        if not os.path.exists(history_db_path):
            raise FileNotFoundError(f"History database not found at {history_db_path}")

        # Create a backup copy of the History file
        backup_path = 'backup_history'
        os.makedirs(backup_path, exist_ok=True)
        backup_db_path = os.path.join(backup_path, 'History_backup')
        shutil.copyfile(history_db_path, backup_db_path)

        # Connect to the backup Chrome History database
        connection = sqlite3.connect(backup_db_path)
        cursor = connection.cursor()

        return connection, cursor

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def create_chrome_history_csv(output_csv):
    try:
        # Connect to the Chrome History database
        connection, cursor = backup_and_open_history_db()

        if connection is None or cursor is None:
            return

        # Execute the query to fetch website names
        query = "SELECT DISTINCT urls.url FROM urls"
        cursor.execute(query)

        # Fetch all the results
        results = cursor.fetchall()

        # Write results to CSV file
        with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Website'])  # Write header

            for row in results:
                csv_writer.writerow([row[0]])

        print(f"CSV file created successfully: {output_csv}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the database connection
        if connection:
            connection.close()
if __name__ == "__main__":
    # Replace 'path/to/output/chrome_history.csv' with the desired output path and filename
    output_csv = os.path.join(os.getcwd(), 'chrome_history.csv')
    create_chrome_history_csv(output_csv)
    
def analyze_chrome_history(csv_file_path, output_html_path='index.html'):
    try:
        # Read the CSV file containing Chrome history
        df = pd.read_csv(csv_file_path, encoding='utf-8')

        # Extract URLs from the DataFrame
        urls = [urlparse(url).netloc for col in df.columns for url in df[col].astype(str)]

        # Use Counter to count the frequency of each domain
        domain_counter = Counter(urls)

        # Sort the domains based on frequency (most frequent first)
        sorted_domains = sorted(domain_counter.items(), key=lambda x: x[1], reverse=True)

        print("Extracted data:")

        # Extract the top 5 domains
        top_5_domains = sorted_domains[:5]

        # Manually suggest potential job positions based on the top domains (expanded to 100 elements)
        job_positions_mapping = {
                        'lichess.org': 'Chess Player',
                        'www.google.com': 'Search Engine Optimization Specialist',
                        'www.linkedin.com': 'Professional Networker',
                        'learn.microsoft.com': 'Microsoft Certified Professional',
                        'ua.mail.yahoo.com': 'Email Administrator',
                        'www.youtube.com': 'Video Content Creator',
                        'github.com': 'Open Source Contributor',
                        'www.amazon.com': 'E-commerce Specialist',
                        'www.netflix.com': 'Entertainment Content Analyst',
                        'stackoverflow.com': 'Community Moderator',
                        'www.udemy.com': 'Online Course Instructor',
                        'www.instagram.com': 'Social Media Manager',
                        'www.facebook.com': 'Social Networking Analyst',
                        'www.reddit.com': 'Forum Moderator',
                        'www.airbnb.com': 'Hospitality Consultant',
                        'www.nytimes.com': 'Journalism Researcher',
                        'www.apple.com': 'iOS App Developer',
                        'www.microsoft.com': 'Software Developer',
                        'www.ibm.com': 'Data Scientist',
                        'www.spotify.com': 'Music Streaming Analyst',
                        'www.zillow.com': 'Real Estate Consultant',
                        'www.udacity.com': 'Online Learning Advocate',
                        'www.spotify.com': 'Music Streaming Analyst',
                        'www.medium.com': 'Content Writer',
                        'www.bloomberg.com': 'Financial Analyst',
                        'www.ted.com': 'Public Speaker',
                        'www.quora.com': 'Knowledge Curator',
                        'www.weather.com': 'Meteorological Data Analyst',
                        'www.coursera.org': 'Online Course Creator',
                        'www.nike.com': 'Sports Apparel Consultant',
                        'www.wikipedia.org': 'Content Editor',
                        'www.pexels.com': 'Photography Enthusiast',
                        'www.twitch.tv': 'Live Streaming Specialist',
                        'www.cisco.com': 'Network Security Analyst',
                        'www.nasa.gov': 'Space Exploration Researcher',
                        'www.etsy.com': 'Handmade Crafts Artisan',
                        'www.hulu.com': 'Streaming Content Reviewer',
                        'www.uber.com': 'Ride-share Consultant',
                        'www.waze.com': 'Navigation App Specialist',
                        'www.salesforce.com': 'CRM Administrator',
                        'www.sony.com': 'Entertainment Systems Analyst',
                        'www.adobe.com': 'Graphic Design Specialist',
                        'www.bbc.com': 'Broadcast Journalism Analyst',
                        'www.cnbc.com': 'Financial News Analyst',
                        'www.mercedes-benz.com': 'Automotive Technology Specialist',
                        'www.coca-cola.com': 'Beverage Marketing Specialist',
                        'www.starbucks.com': 'Coffee Culture Analyst',
                        'www.marvel.com': 'Comic Book Enthusiast',
                        'www.ikea.com': 'Interior Design Consultant',
                        'www.spotify.com': 'Music Playlist Curator',
                        'www.snapchat.com': 'Snap Content Creator',
                        'www.playstation.com': 'Gaming Console Analyst',
                        'www.nintendo.com': 'Video Game Developer',
                        'www.fitbit.com': 'Fitness Technology Consultant',
                        'www.yelp.com': 'Review Platform Analyst',
                        'www.tripadvisor.com': 'Travel Recommendations Analyst',
                        'www.spotify.com': 'Music Genre Analyst',
                        'www.ancestry.com': 'Genealogy Researcher',
                        'www.soundcloud.com': 'Music Streaming Enthusiast',
                        'www.zappos.com': 'Footwear Fashion Consultant',
                        'www.grammarly.com': 'Grammar and Writing Analyst',
                        'www.hubspot.com': 'Inbound Marketing Specialist',
                        'www.patagonia.com': 'Sustainable Fashion Advocate',
                        'www.tesla.com': 'Electric Vehicle Technology Analyst',
                        'www.nike.com': 'Sports Performance Analyst',
                        'www.ibm.com': 'Quantum Computing Researcher',
                        'www.britannica.com': 'Encyclopedia Editor',
                        'www.duolingo.com': 'Language Learning Specialist',
                        'www.hbo.com': 'Streaming Content Analyst',
                        'www.ibm.com': 'Blockchain Technology Consultant',
                        'www.cnn.com': 'News Broadcasting Analyst',
                        'www.coca-cola.com': 'Beverage Taste Tester',
                        'www.ibm.com': 'Quantum Computing Researcher',
                        'www.twitch.tv': 'Esports Analyst',
                        'www.canon.com': 'Photography Equipment Specialist',
                        'www.spotify.com': 'Music Discovery Analyst',
                        'www.slack.com': 'Team Collaboration Specialist',
                        'www.squarespace.com': 'Website Design Consultant',
                        'www.ebay.com': 'E-commerce Entrepreneur',
                        'www.dropbox.com': 'Cloud Storage Technology Specialist',
                        'www.samsung.com': 'Consumer Electronics Analyst',
                        'www.netflix.com': 'Binge-Watching Expert',
                        'www.ibm.com': 'Artificial Intelligence Researcher',
                        'www.spotify.com': 'Music Recommendation Analyst',
                        'www.oracle.com': 'Database Management Specialist',
                        'www.nintendo.com': 'Gaming Industry Analyst',
                        'www.spotify.com': 'Podcast Enthusiast',
                        'www.ibm.com': 'Quantum Computing Researcher',
                        'www.ibm.com': 'Quantum Computing Researcher',
                    }

# Manually suggest potential soft skills based on the top domains (expanded to 100 elements)
        soft_skills_mapping = {
                'lichess.org': 'Strategic Thinking',
                'www.google.com': 'Analytical Skills',
                'www.linkedin.com': 'Communication Skills',
                'learn.microsoft.com': 'Technical Skills',
                'ua.mail.yahoo.com': 'Organizational Skills',
                'www.youtube.com': 'Video Editing Skills',
                'github.com': 'Open Source Collaboration',
                'www.amazon.com': 'E-commerce Strategy',
                'www.netflix.com': 'Content Consumption Management',
                'stackoverflow.com': 'Problem-Solving Abilities',
                'www.udemy.com': 'Online Teaching Skills',
                'www.instagram.com': 'Social Media Management',
                'www.facebook.com': 'Social Networking Proficiency',
                'www.reddit.com': 'Community Engagement',
                'www.airbnb.com': 'Hospitality Management',
                'www.nytimes.com': 'Journalistic Research Skills',
                'www.apple.com': 'iOS App Development Skills',
                'www.microsoft.com': 'Software Development Proficiency',
                'www.ibm.com': 'Data Science Competence',
                'www.spotify.com': 'Music Streaming Knowledge',
                'www.zillow.com': 'Real Estate Market Awareness',
                'www.udacity.com': 'Online Learning Facilitation',
                'www.spotify.com': 'Music Streaming Expertise',
                'www.medium.com': 'Content Creation Writing',
                'www.bloomberg.com': 'Financial Analysis Skills',
                'www.ted.com': 'Public Speaking Abilities',
                'www.quora.com': 'Knowledge Sharing Skills',
                'www.weather.com': 'Meteorological Data Interpretation',
                'www.coursera.org': 'Online Course Design',
                'www.nike.com': 'Sports Apparel Design Skills',
                'www.wikipedia.org': 'Content Editing Proficiency',
                'www.pexels.com': 'Photography Editing Skills',
                'www.twitch.tv': 'Live Streaming Expertise',
                'www.cisco.com': 'Network Security Expertise',
                'www.nasa.gov': 'Space Exploration Knowledge',
                'www.etsy.com': 'Handmade Crafts Design Skills',
                'www.hulu.com': 'Streaming Content Evaluation',
                'www.uber.com': 'Ride-share Strategy',
                'www.waze.com': 'Navigation App Proficiency',
                'www.salesforce.com': 'CRM Management Skills',
                'www.sony.com': 'Entertainment Systems Expertise',
                'www.adobe.com': 'Graphic Design Proficiency',
                'www.bbc.com': 'Broadcast Journalism Expertise',
                'www.cnbc.com': 'Financial News Analysis Skills',
                'www.mercedes-benz.com': 'Automotive Technology Knowledge',
                'www.coca-cola.com': 'Beverage Marketing Strategy',
                'www.starbucks.com': 'Coffee Culture Awareness',
                'www.marvel.com': 'Comic Book Knowledge',
                'www.ikea.com': 'Interior Design Proficiency',
                'www.spotify.com': 'Music Playlist Curation',
                'www.snapchat.com': 'Snap Content Creation',
                'www.playstation.com': 'Gaming Console Expertise',
                'www.nintendo.com': 'Video Game Development Skills',
                'www.fitbit.com': 'Fitness Technology Proficiency',
                'www.yelp.com': 'Review Platform Analysis Skills',
                'www.tripadvisor.com': 'Travel Recommendations Knowledge',
                'www.spotify.com': 'Music Genre Analysis',
                'www.ancestry.com': 'Genealogy Research Abilities',
                'www.soundcloud.com': 'Music Streaming Enthusiast',
                'www.zappos.com': 'Footwear Fashion Knowledge',
                'www.grammarly.com': 'Grammar and Writing Expertise',
                'www.hubspot.com': 'Inbound Marketing Skills',
                'www.patagonia.com': 'Sustainable Fashion Awareness',
                'www.tesla.com': 'Electric Vehicle Technology Knowledge',
                'www.nike.com': 'Sports Performance Analysis Skills',
                'www.ibm.com': 'Quantum Computing Research Abilities',
                'www.britannica.com': 'Encyclopedia Editing Proficiency',
                'www.duolingo.com': 'Language Learning Knowledge',
                'www.hbo.com': 'Streaming Content Analysis Skills',
                'www.ibm.com': 'Blockchain Technology Proficiency',
                'www.cnn.com': 'News Broadcasting Analysis Skills',
                'www.coca-cola.com': 'Beverage Taste Testing Skills',
                'www.ibm.com': 'Quantum Computing Research Abilities',
                'www.twitch.tv': 'Esports Analysis Skills',
                'www.canon.com': 'Photography Equipment Knowledge',
                'www.spotify.com': 'Music Discovery Analysis Skills',
                'www.slack.com': 'Team Collaboration Proficiency',
                'www.squarespace.com': 'Website Design Knowledge',
                'www.ebay.com': 'E-commerce Entrepreneurship Skills',
                'www.dropbox.com': 'Cloud Storage Technology Proficiency',
                'www.samsung.com': 'Consumer Electronics Analysis Skills',
                'www.netflix.com': 'Binge-Watching Expertise',
                'www.ibm.com': 'Artificial Intelligence Research Abilities',
                'www.spotify.com': 'Music Recommendation Analysis Skills',
                'www.oracle.com': 'Database Management Proficiency',
                'www.nintendo.com': 'Gaming Industry Analysis Skills',
                'www.spotify.com': 'Podcast Enthusiast',
                'www.ibm.com': 'Quantum Computing Research Abilities',
                'www.ibm.com': 'Quantum Computing Research Abilities',
            }

        # Create HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Job and Soft Skills Recommendations</title>
        </head>
        <body>
            <h1>Top 5 Recommended Job Positions and Soft Skills</h1>

            <h2>Job Positions</h2>
            <table>
                <tr>
                    <th>Rank</th>
                    <th>Job Position</th>
                    <th>Domain Visits</th>
                </tr>
                """
        for i, (domain, frequency) in enumerate(top_5_domains, start=1):
            job_position = job_positions_mapping.get(domain, 'No available')
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{job_position}</td>
                    <td>{frequency}</td>
                </tr>
                """

        html_content += """
            </table>

            <h2>Soft Skills</h2>
            <table>
                <tr>
                    <th>Rank</th>
                    <th>Soft Skill</th>
                    <th>Domain Visits</th>
                </tr>
                """
        for i, (domain, frequency) in enumerate(top_5_domains, start=1):
            soft_skill = soft_skills_mapping.get(domain, 'No available')
            html_content += f"""
                <tr>
                    <td>{i}</td>
                    <td>{soft_skill}</td>
                    <td>{frequency}</td>
                </tr>
                """

        html_content += """
            </table>
        </body>
        </html>
        """

        # Write the HTML content to a file
        with open(output_html_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_content)

        print(f"HTML file created successfully: {output_html_path}")

        # Open the HTML file in the default web browser
        webbrowser.open(output_html_path, new=2)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'path/to/your/exported/history.csv' with the actual path to your exported Chrome history CSV file
    csv_file_path = 'chrome_history.csv'
    analyze_chrome_history(csv_file_path)
