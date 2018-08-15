from keras.applications import VGG16
from keras.applications import VGG19
from keras.applications import ResNet50
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--include_top", type=int, default=1, help="whether or nor to include top of CNN")
args = vars(ap.parse_args())

print("[INFO] loading network...")
model = ResNet50(weights="imagenet", include_top=args["include_top"] > 0)
print("[INFO] showing layers...")

for (i, layer) in enumerate(model.layers):
	print("[INFO] {}\t{}".format(i, layer.__class__.__name__))
