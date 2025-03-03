import warnings
warnings.filterwarnings("ignore", message="urllib3 v2 only supports OpenSSL 1.1.1+")

from plexapi.server import PlexServer
from plexapi.exceptions import Unauthorized, NotFound


class PlexManager:

    def __init__(self, server_url, token):
        self.server_url = server_url
        self.token = token
        self.server = None

    def connect(self):
        try:
            import requests

            import urllib3
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

            session = requests.Session()
            session.verify = False

            self.server = PlexServer(self.server_url, self.token, session=session)
            return True
        except Unauthorized:
            print("Error: Invalid token or unauthorized access")
            return False
        except Exception as e:
            print(f"Error connecting to Plex server: {e}")
            return False

    def get_libraries(self):
        if not self.server:
            if not self.connect():
                return []

        return self.server.library.sections()

    def get_all_collections(self):
        if not self.server:
            if not self.connect():
                return {}

        libraries = self.get_libraries()
        all_collections = {}

        for library in libraries:
            try:
                collections = library.collections()
                all_collections[library.title] = collections
            except Exception as e:
                print(f"Error retrieving collections from {library.title}: {e}")

        return all_collections

    def get_empty_collections(self):
        all_collections = self.get_all_collections()
        empty_collections = {}

        for library_name, collections in all_collections.items():
            empty_in_library = []
            for collection in collections:
                if len(collection.items()) == 0:
                    empty_in_library.append({
                        "id": collection.ratingKey,
                        "title": collection.title,
                        "count": 0
                    })

            if empty_in_library:
                empty_collections[library_name] = empty_in_library

        return empty_collections

    def delete_collection(self, collection_id):
        if not self.server:
            if not self.connect():
                return False

        try:
            collection = self.server.fetchItem(collection_id)
            collection.delete()
            return True
        except NotFound:
            print(f"Collection with ID {collection_id} not found")
            return False
        except Exception as e:
            print(f"Error deleting collection: {e}")
            return False
