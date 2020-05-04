import sys
from bs4 import BeautifulSoup
import os


def list_html_files(path_html):
    abs_path= os.path.abspath(path_html)
    html_files= os.listdir(path_html)
    html_files= [os.path.join(abs_path, x) for x in html_files if x.endswith('.html')]
    return html_files

def get_name(html_file):
    name_view= html_file.split('.')[0]
    name_view= os.path.split(name_view)[1]
    name_view= name_view.replace(' ', '_').lower()
    return name_view

path_html= '/home/trona/Documents/freelance/freelancer_git/contributions/django-bootstrap-studio-tools/django_app/app/Proj/templates'
if __name__ == '__main__':
    path_html_files= sys.argv[1]
    app_name= sys.argv[2]
    
    html_files= list_html_files(path_html_files)
    
    for each_file in html_files: 
        print('processing {}'.format(each_file))

        with open(each_file, "r") as fp:
            soup = BeautifulSoup(fp, "lxml")
        
        # handle load
        for div in soup.find_all(attrs={"dj-load": True}):
            if div:
                forline = "{% load " + div.get('dj-load') + " %}"
                div.insert_before(forline)
                del div
        
        # handle for
        for div in soup.find_all(attrs={"dj-for": True}):
            if div:
                forline = "{% for " + div.get('dj-for') + " %}"
                div.insert_before(forline)
                if 'dj-for' in div.attrs:
                    del div.attrs['dj-for']
                    div.insert_after('{% endfor %}')
        
        # handle refs
        for ref in soup.find_all(attrs={"dj-ref": True}):
            if ref:
                if 'dj-ref' in ref.attrs:
                    refattr = ref.get('dj-ref')
                    if ref.string:
                        ref.string.replace_with('{{ ' + refattr + ' }}')
                    del ref.attrs['dj-ref']
        
        # handle if
        # eg:
        # {% if form.errors %}
        # ...
        # {% endif %}
        for ifs in soup.find_all(attrs={"dj-if": True}):
            if ifs:
                ifline = "{% if " + ifs.get("dj-if") + " %}"
                ifs.insert_before(ifline)
                if "dj-if" in ifs.attrs:
                    del ifs.attrs["dj-if"]
                    ifs.insert_after("{% endif %}")
        
                    
        # handle block
        for div in soup.find_all(attrs={"dj-block": True}):
            if div:
                blockline = "{% block " + div.get('dj-block') + " %}"
                div.insert_before(blockline)
                if 'dj-block' in div.attrs:
                    del div.attrs['dj-block']
                    div.insert_after('{% endblock %}')
         
        # handle scripts,
        # eg:
           # <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.4.1/jquery.easing.js">
            # eg <script src="{% static "assets/js/theme.js" %}">
        for div in soup.find_all("script"):
            if div:
                if not div.get("src").startswith("http"):
                    div.attrs["src"] = "{{% static '{}' %}}".format(div.attrs["src"])
        
        for div in soup.find_all("link"):
            if div:
                if not div.get("href").startswith("http"):
                    div.attrs["href"] = "{{% static '{}' %}}".format(div.attrs["href"])
        
        for div in soup.find_all("img"):
            if div:
                if not div.get("src").startswith("{%"):
                    div.attrs["src"] = "{{% static '{}' %}}".format(div.attrs["src"])
        
        for csrf in soup.find_all(attrs={"dj-csrf": True}):
            if csrf:
                csrf.insert(0, "{% csrf_token %}")
                if "dj-csrf" in csrf.attrs:
                    del csrf.attrs["dj-csrf"]
        
        # Check if we have the load static tag
        test= '{% load static %}' in soup.contents
        if test:
            pass
        else:
            div= soup.find('html')
            div.insert_before('{% load static %}')

        # Process links
        
        for each_html in html_files:
            name= get_name(each_html)
            links= soup.findAll(name='a', attrs={'href':'{}.html'.format(name)})
            if links: 
                for link in links: 
                    link.attrs['href'] = '''{{% url '{}:{}' %}}'''.format(app_name, name)
    
        with open(each_file, "w") as outfp:
            outfp.write(soup.prettify())
