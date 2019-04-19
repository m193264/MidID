import face_recognition
import pickle
import numpy as np
import os
import argparse
from resize_imgs import exif_open

def extract_embeddings_from_directory(unknown_photo_directory,alpha_named_files=True):
	'''
	Takes the name of a directory
	Creates a list of embeddings of all photos in the directory
	Creates a list of the file names in the directory
	'''
	count = 1
	embeddings = []
	img_files = []
	file_list = os.listdir(unknown_photo_directory)
	for img_file in file_list:
		full_filename = unknown_photo_directory + '/' + img_file

		print("Loading file ",count," of ",len(file_list),'\t',img_file)
		count+=1
		# Load image file
		try:
			img = face_recognition.load_image_file(full_filename)
		except ValueError:
			print("Failed to open file ",img_file)
			continue

		# Extract embedding
		try:
            		encoding = face_recognition.face_encodings(img)[0]
		except IndexError:
			print("Unable to locate face in photo. Check image file",img_file)
			continue

		# Add to list
		embeddings.append(encoding)
		if alpha_named_files:
			alpha = img_file[:6]
			img_files.append(alpha)
		else:
			img_files.append(img_file)
	return embeddings, img_files

def img2alpha(imageio_img, embeddings, embedding_IDs):
	'''
	returns the alpha of an image opened with imageio of a midshipman
	'''
	unknown_encoding = face_recognition.face_encodings(imageio_img)[0]
	comparison_res = face_recognition.face_distance(embeddings,unknown_encoding)
	top_res_idx = np.argmin(comparison_res)
	return embedding_IDs[top_res_idx]

def load_embeddings_file(full_fname):
	with open(full_fname,'rb') as f:
		embeddings = pickle.load(f)
		img_fnames = pickle.load(f)
		return embeddings, img_fnames


def load_embeddings_directory(embeddings_directory):
	'''
	directory must contain pkl files of embeddings
	embeddings are a numpy array
	IDs are Midshipman alphas
	'''
	file_list=os.listdir(embeddings_directory)
	total_embeddings = []
	total_embedding_IDs = []

	for fname in file_list:
		full_fname = embeddings_directory + '/' + fname
		with open(full_fname,'rb') as f:
			embeddings = pickle.load(f)
			img_fnames = pickle.load(f)
			total_embeddings = total_embeddings + embeddings
			total_embedding_IDs = total_embedding_IDs + img_fnames
	return total_embeddings, total_embedding_IDs


def save_embeddings(out_file,embeddings,embedding_IDs):
	'''
	saves embeddings and embedding_IDs to a pkl file
	'''
	with open(out_file,'wb') as datafile:
		pickle.dump(embeddings,datafile,pickle.HIGHEST_PROTOCOL)
		pickle.dump(embedding_IDs,datafile,pickle.HIGHEST_PROTOCOL)

def main():
	'''
	Extracts embeddings from a directory given as a command line argument
	Saves embeddings to a pkl file with the same name as the directory
	'''
	parser=argparse.ArgumentParser()
	parser.add_argument("img_directory")
	args=parser.parse_args()
	img_directory=args.img_directory

	embeddings, img_files = extract_embeddings_from_directory(img_directory,True)

	# save data to file
	print("Saving to file",end="...")
	save_embeddings(img_directory+'.pkl',embeddings, img_files)
	print("Done")


if __name__ == "__main__":
	main()
