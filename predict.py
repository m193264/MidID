import face_recognition
import embeddings
import pickle
import os


def load_name_handle_map_from_file(map_file):
	with open(map_file,'rb') as f:
		name_handle_map = pickle.load(f)
		return name_handle_map

def handle2Name(name_handle_map, handle):
    try:
        if handle.isdigit():
            name = name_handle_map['m'+handle]
        else:
            name = name_handle_map[handle]
    except Exception as e:
        # No Name Found
        name = ''
    return name

def grabMidsPhotoLink(handle):
	link_root = 'https://deep-learning-capstone/'
	link = 'imgs/mids-imgs/'
	group = handle[:2]
	if group == '19':
		link = link + '2019/' + handle + '.jpg'
	elif group == '20':
		link = link + '2020/' + handle + '.jpg'
	elif group == '21':
		link = link + '2021/' + handle + '.jpg'
	elif group == '22':
		link = link + '2022/' + handle + '.jpg'
	else:
		link = 'imgs/unknown.jpg'
	if not os.path.isfile(link):
		link = 'imgs/unknown.jpg'
	return link_root + link



def predict (img_arr):
	encodings, IDs = embeddings.load_embeddings_directory('embeddings_pkl')
	name_handle_map = load_name_handle_map_from_file('handleNameMap.pkl')
	unknown_encoding = face_recognition.face_encodings(img_arr)[0]
	distances = face_recognition.face_distance(encodings, unknown_encoding)
	match_idxs = distances.argsort()[:3]
	top_handles = [IDs[i] for i in match_idxs]
	top_probs = [1-distances[i] for i in match_idxs]
	top_names = [handle2Name(name_handle_map, handle) for handle in top_handles]
	midsPhotoLink = grabMidsPhotoLink(top_handles[0])
	return top_handles, top_probs, top_names, midsPhotoLink

def main():
	img = face_recognition.load_image_file('capture.png')
	res = predict(img)
	print(res)

if __name__ == "__main__":
	main()
