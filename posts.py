from firebase import firebase

def get_post_ids_by_hotspot(hotspot):
    
    db_address = "https://placenessdb3.firebaseio.com/"
    sub_address = "/CoexIparkData"
    
    fb = firebase.FirebaseApplication(db_address, None)
    
    hotspot_address = "%s/%s" % (sub_address, hotspot) 
    
    posts = fb.get(hotspot_address, None, params={'shallow':'true'})    
    post_ids = posts.keys()
    
    return post_ids


if __name__ == "__main__":
    get_post_ids_by_hotspot("246221160")
    