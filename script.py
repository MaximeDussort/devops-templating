import os
import csv
import markdown
import jinja2

CONTENT_DIR = './content'
TEMPLATE_DIR = './templates'
OUTPUT_DIR = '.'

env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR, encoding='utf-8'))
def generate_home_page(news_list):
    template = env.get_template('index.html')
    rendered = template.render(news=news_list)
    with open(os.path.join(OUTPUT_DIR, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(rendered)

def generate_news_page(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        text = f.read()
        html_content = markdown.markdown(text)
    
    template = env.get_template('news_detail.html')
    rendered = template.render(content=html_content)
    
    output_file = os.path.join(OUTPUT_DIR, os.path.basename(markdown_file).replace('.md', '.html'))
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(rendered)

def generate_members_page(csv_file):
    members = []
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            members.append(row)
    
    template = env.get_template('members.html')
    rendered = template.render(members=members)
    
    with open(os.path.join(OUTPUT_DIR, 'members.html'), 'w', encoding='utf-8') as f:
        f.write(rendered)

def generate_site():
    news_list = []    
    for filename in os.listdir(CONTENT_DIR):
        if filename.endswith('.md'):
            markdown_file = os.path.join(CONTENT_DIR, filename)
            title = get_title_from_md(markdown_file)

            generate_news_page(os.path.join(CONTENT_DIR, filename))
            get_image_name = filename[-14:]
            news_list.append({
                'title': title,
                'link': filename.replace('.md', '.html'),
                'image': get_image_name.replace('.md', '.webp'),
            })
    generate_home_page(news_list)
    generate_members_page(os.path.join(CONTENT_DIR, 'membres.csv'))

def get_title_from_md(markdown_file):
    with open(markdown_file, 'r', encoding='utf-8') as f:
        first_line = f.readline().strip()  # Lire la première ligne et retirer les espaces superflus
        if first_line.startswith('#'):
            # Si la première ligne commence par #, on le retire pour obtenir le titre
            return first_line[1:].strip()
        else:
            # Si aucune balise # n'est trouvée, on retourne la ligne telle quelle
            return first_line

if __name__ == '__main__':
    generate_site()