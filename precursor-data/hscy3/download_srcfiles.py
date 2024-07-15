# This is a script that downloads all the files from
# https://hsc-release.mtk.nao.ac.jp/archive/filetree/pdr3_wide/
# which are needed for focal plane reconstruction

import os,sys,re
from pathlib import Path
from tqdm import tqdm
import urllib.request
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup

def get_link(base_url,string,username,password):
    # Function to list all teh subdirectories
    dir_pattern  = re.compile(r'%s'%string)

    # Create a password manager
    password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
    password_mgr.add_password(None, base_url, username, password)

    # Create an authentication handler
    auth_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

    # Create an opener with the authentication handler
    opener = urllib.request.build_opener(auth_handler)

    # Install the opener
    urllib.request.install_opener(opener)

    response = urllib.request.urlopen(base_url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    links = soup.find_all('a')

    ret_links=[]
    for link in links:
        href = link.get('href')
        if dir_pattern.match(href):
            file_url = base_url + href
            ret_links.append(file_url)
    
    return ret_links


def download_file(file_url, local_filename):
    # Function to download a file
    try:
        response = urllib.request.urlopen(file_url)
        with open(local_filename, 'wb') as f:
            f.write(response.read())
        #print(f"Downloaded {local_filename}")
    except HTTPError as e:
        #print(f'HTTP Error: {e.code} - {e.reason}')
        print('HTTP Error')
    except URLError as e:
        #print(f'URL Error: {e.reason}')
        print('URL Error')
    except Exception as e:
        #print(f'Error: {e}')
        print('Error')


if __name__ == "__main__":

    username = str(sys.argv[1])
    password = str(sys.argv[2])

    home = get_link('https://hsc-release.mtk.nao.ac.jp/archive/filetree/pdr3_wide/','0',username,password)

    for sub in home:
        subsub  = get_link(sub,'HSC',username,password)[0]+'output/'
        dir_out = subsub.replace('https://hsc-release.mtk.nao.ac.jp/archive/filetree/pdr3_wide/','')
        DLs     = get_link(subsub,'SRC-',username,password)

        Path(dir_out).mkdir(parents=True, exist_ok=True)

        with open(dir_out[:5]+'.txt', 'w') as f:
            for line in DLs:
                f.write(f"{line}\n")

        for file_i in tqdm(DLs):
            file_out = file_i.replace('https://hsc-release.mtk.nao.ac.jp/archive/filetree/pdr3_wide/','')
            download_file(file_i, file_out)


