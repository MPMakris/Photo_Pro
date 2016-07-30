Notes Based on **Neural Networks and Deep Learning**, [Chapter 6](<http://neuralnetworksanddeeplearning.com/chap6.html>).
## CNN
* Feature Mapping / "Convolutional Layer":
  * Map a single array of pixels into multiple arrays (each is a 'feature'). Each pixel in destination arrays maps to an NxN subarray ('receptive field') in the input array.
* Pooling:
  * Reducing each single feature array into a single reduced pooled array but taking a max/average/RSS of the array pixels. The feature array subarray of MxM gets reduced to a single pixel in output pooled array.
* Created More Images:
  * A useful way of increasing the training set and accounting for variance in images is to produce slightly edited versions of the training data. Variations include:
    - translating
    - rotating
    - stretching
  * Allows us to increase training data size by multiples, avoiding overfitting and maybe require less epochs.
* Ensembling:
  * By ensembling multiple CNN, we can take a vote at the end to increaes accuracy.
* Cross Validation:
  * Each CNN should have a training set and a validation set, and they should share a common test set. The training and validation sets are used to determining which epoch's version of the model should be used to measure accuracy for the test set.
 ---
## DBN - Deep Belief Networks
* Can be used to back-generate inputs from outputs. For example, on the MNIST set, by specifying a numeric output, it will generate an image of the number as a sample input (i.e. opposite of normal direction).
*   
