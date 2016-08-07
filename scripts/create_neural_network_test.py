"""Test script for creating a neural network on the user_is_pro target."""
import graphlab as gl


def main():
    """Run the Main script."""
    backup = '/home/ubuntu/data/GL_BUILDINGS_MODEL_CHECKPOINT'
    data = '/home/ubuntu/data/GL_BUILDINGS_MODELING_DATA_RESIZED'
    images = gl.load_sframe(data)
    images_train, images_test = images.random_split(0.8)
    model = gl.neuralnet_classifier.create(images_train, target='user_is_pro',
                                           features=['resized_image'],
                                           max_iterations=100, network=None,
                                           #  validation_set=images_test,
                                           class_weights='auto', metric='auto',
                                           random_crop=False, input_shape=None,
                                           random_mirror=False,
                                           learning_rate=0.001, momentum=0.9,
                                           l2_regularization=0.0005,
                                           bias_l2_regularization=0.0,
                                           init_random='gaussian',
                                           init_sigma=0.01, init_bias=0.0,
                                           model_checkpoint_path=backup,
                                           model_checkpoint_interval=5)
    model.save('/home/ubuntu/data/GL_BUILDINGS_MODEL')

if __name__ == "__main__":
    main()
