import os

def get_subdirs(b='.'):
    '''
        Returns all sub-directories in a specific Path
    '''
    result = []
    for d in os.listdir(b):
        bd = os.path.join(b, d)
        if os.path.isdir(bd):
            result.append(bd)
    return result


def get_detection_folder():
    '''
        Returns the latest folder in a runs\detect
    '''
    detect_folder = os.path.join('runs', 'detect')
    if os.path.exists(detect_folder):
        return max(get_subdirs(detect_folder), key=os.path.getmtime)
    return None

def check_folders():
    paths = {
        'data_path' : 'data',
        'images_path' : 'data/images',
        'videos_path' : 'data/videos'
        
    }
    # Check whether the specified path exists or not
    notExist = list(({file_type: path for (file_type, path) in paths.items() if not os.path.exists(path)}).values())
    
    if notExist:
        print(f'Folder {notExist} does not exist. We will created')
        # Create a new directory because it does not exist
        for folder in notExist:
            os.makedirs(folder)
            print(f"The new directory {folder} is created!")
  
        
        