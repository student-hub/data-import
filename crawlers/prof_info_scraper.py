from bs4 import BeautifulSoup
import bs4, requests, json, os, sys, re, html, argparse

# if any of the info is not collected anymore, maybe these ids changed
INFO_IDS = {
    "name": "cbfv_45",
    "office": "cbfv_31",
    "position": "cbfv_63",
    "phone": "cbfv_43"
}

URL = "https://cs.pub.ro/index.php/?option=com_comprofiler&task=userslist"
SPAN_LINK_CLASS = "cbListFieldCont cbUserListFC_formatname"
PROFILE_AREA_CLASS = "cbProfile"

def extract_email(soup):
    # cbMailRepl is a static identifier, we use it to find the id of the mail span, which is dynamic
    mail_class = "cbMailRepl"
    mail_span = soup.find(class_=mail_class)
    if mail_span is None:
        print(f"Could not find known mail static class: {mail_class}")
        return None
    
    mail_span_id = mail_span['id']
    if mail_span_id is None:
        print(f"Could not find mail span id.")
        return None
    
    # next we find the script that uses the mail id
    # the script has no src, it's embedded in the html, the id is used in a line with this format
    # $('#mail_span_id').html(variable_name);
    # we need to extract both the script and the variable_name
    scripts = soup.head.findAll("script", attrs={'src': None})
    target_script, target_variable = None, None
    search_str = re.compile(f"\$\('#{mail_span_id}'\)\.html\(([a-zA-Z0-9]+)\);")
    for script in scripts:
        content = script.contents[0]
        match = search_str.findall(content)
        if len(match) > 0:
            target_script = content
            target_variable = match[0]
            break
    
    if target_script is None:
        print(f"Could not find any script that uses the id: {mail_span_id}")
        return None

    # we found the script and the variable name, so we use it to find the email
    # the variable holds the email in a similar format to
    # var variable_name = 'html_encoded_str' + 'html_encoded_@' + 'html_encoded_domain' + 'html_encoded_subdomain' + 'html_encoded_ro';
    # the email address is html encoded, at the time of writing this script, I was unable to find a way to decode the strings
    # before extracting the email
    search_str = re.compile(f"var\s*{target_variable}\s*=\s*(('[a-zA-Z0-9&#;\.@]+'\s*\+?\s*)+);")
    match = search_str.findall(target_script)

    # html decode and cleanup
    mail = html.unescape(match[0][0]).replace("'", "").replace('+', '').replace(' ', '')
    # trim
    mail = ''.join(mail.split())
    
    return mail

def extract_photo(soup):
    # if links for pictures are not exracted, maybe this class changed
    photo_class = "cbFullPict"
    img = soup.find("img", class_=photo_class)
    if img is None:
        print(f"Could not find img tag with class: {photo_class}")
        return None
    try:
        return img["src"]
    except KeyError:
        print("The found img does not have a src attribute.")
        return None

def get_soup(url: str):
    response = requests.get(url)
    return BeautifulSoup(response.text, 'html.parser')

def get_prof_info(prof_url):
    print(prof_url)
    info = {}
    soup = get_soup(prof_url)
    profile_area = soup.find(class_=PROFILE_AREA_CLASS)
    for key, id in INFO_IDS.items():
        try:
            info[key] = profile_area.find(id=id).text
        except AttributeError as e:
            print(f'Failed to extract {key} by id from {prof_url}: {e}')
    
    info['photo'] = extract_photo(soup)
    info['email'] = extract_email(soup)
    
    return info

def get_info():
    soup = get_soup(URL)
    prof_urls = [elem.a['href'] for elem in soup.findAll("span", class_=SPAN_LINK_CLASS)]

    prof_info = []

    for prof_url in prof_urls:
        prof_info.append(get_prof_info(prof_url))
        
    return {"people": prof_info}

def write_json_info_to_file():
    parser = argparse.ArgumentParser(description="Extract information about ACS teachers.")
    parser.add_argument('--output', help='File to output to. Default: prof_info.json', default='prof_info.json')

    args = parser.parse_args()

    with open(args.output, 'w') as f:
        f.write(json.dumps(get_info()))

if __name__ == '__main__':
    write_json_info_to_file()