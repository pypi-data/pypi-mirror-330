Usage Sample
''''''''''''

.. code:: python

        from keras_model_hub import TextCNN

        model = Sequential([
                Embedding(vocab_size, embed_dim, input_length=None, mask_zero=False),
                TextCNN(num_classes, activation='softmax')
	])
