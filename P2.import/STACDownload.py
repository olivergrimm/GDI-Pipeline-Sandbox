import requests

url = "https://app.geopilot.ch/api/v1/delivery/assets/94"

output_file = "./_data/av_current.xtf"

def download_file(url, output_path):

    try:
        response = requests.get(url, stream=True)  
        response.raise_for_status()  

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):  
                file.write(chunk)

        print(f"✅ Datei erfolgreich heruntergeladen: {output_path}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Fehler beim Herunterladen der Datei: {e}")

download_file(url, output_file)