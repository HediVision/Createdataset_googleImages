import argparse
import requests
import cv2
import os
import impath

def downlaod_images(args):
	line = open(args["urls"]).read().strip().split("\n")
	counter=0
	for url in line:
		try:
			# try to download the image
			r = requests.get(url, timeout=60)
			# save the image to disk
			p = os.path.sep.join([args["output"], "{}.jpg".format(
				str(counter).zfill(8))])
			f = open(p, "wb")
			f.write(r.content)
			f.close()
			print("[INFO] downloaded: {}".format(p))
			counter += 1
		except:
			print("[INFO] error downloading {}...skipping".format(p))

def cleaning(args):
	cv2.namedWindow('clean',0)
	# loop over the image paths we just downloaded
	for imagePath in impath.list_images(args["output"]):
		# initialize if the image should be deleted or not
		delete = False
	
		# try to load the image
		try:
			image = cv2.imread(imagePath)
			# if the image is `None` then we could not properly load it
			# from disk, so delete it
			if image is None:
				delete = True
			else:
				cv2.imshow("clean",image)
				ch=cv2.waitKey(0)
				if(ch==32):
					delete = True
				if(ch==27):
					break
		except:
			print("Except")
			delete = True
		if delete:
			print("[INFO] deleting {}".format(imagePath))
			os.remove(imagePath)

def main(args):
	#downlaod_images(args)
	cleaning(args)
		

if __name__=="__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-u", "--urls", required=True,
		help="path to file containing image URLs")
	ap.add_argument("-o", "--output", required=True,
		help="path to output directory of images")
	args = vars(ap.parse_args())
	main(args)