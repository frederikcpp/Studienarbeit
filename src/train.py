"""Train the CycleGAN model."""

import tensorflow as tf
import toml
import os

import utils.load_data
import utils.misc
import model
import matplotlib.pyplot as plt
import uuid


def main():
    if os.name == 'posix':
        config = toml.load('config/config.toml')
    else:
        config = toml.load(os.path.realpath(os.path.join(os.path.dirname(__file__), 'config/config.toml')))

    BATCH_SIZE = config['training']['batch_size']
    BUFFER_SIZE = 1000
    IMAGE_SIZE = config['model']['image_size']

    path_to_train_directory = config['paths']['train_data']
    #training_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', path_to_train_directory))
    training_path = path_to_train_directory
    x_train = tf.keras.utils.image_dataset_from_directory(training_path, batch_size=BATCH_SIZE,
                                                          image_size=(IMAGE_SIZE, IMAGE_SIZE), labels=None,
                                                          shuffle=True, crop_to_aspect_ratio=True)
    x_train_processed = utils.load_data.normalize_dataset(x_train)

    PATH_TO_PICTOGRAMS = config['paths']['pictograms']
    # pictograms_path = os.path.realpath(os.path.join(os.path.dirname(__file__), '..', PATH_TO_PICTOGRAMS))
    pictograms_path = PATH_TO_PICTOGRAMS
    x_pictograms = tf.keras.utils.image_dataset_from_directory(pictograms_path, batch_size=BATCH_SIZE,
                                                               image_size=(IMAGE_SIZE, IMAGE_SIZE), labels=None,
                                                               shuffle=True, crop_to_aspect_ratio=False) # change last param to True!
    x_pictograms_processed = utils.load_data.normalize_dataset(x_pictograms)

    #for pictograms in x_pictograms_processed:
    #    for pictogram in pictograms:
    #        plt.imshow(pictogram)
    #        plt.show()

    cycle_gan = model.CycleGan(config)
    cycle_gan.compile()
    cycle_gan.restore_latest_checkpoint_if_exists()
    cycle_gan.print_welcome()
    cycle_gan.fit(x_pictograms_processed, x_train_processed, epochs=config['training']['number_of_epochs'])
    return


if __name__ == '__main__':
    main()
