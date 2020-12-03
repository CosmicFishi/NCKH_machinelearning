from keras.layers import Conv2D, Dense, Flatten
from keras import layers
from keras.models import Sequential


def train(X_train, y_train, X_test, y_test):
    model = Sequential()
    model.add(Dense(10, input_dim=X_train.shape[1], activation="relu"))
    model.add(Dense(1, activation="sigmoid"))
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    history = model.fit(X_train, y_train,
                        epochs=100,
                        verbose=False,
                        validation_data=(X_test, y_test),
                        batch_size=10)
    print(history.__dict__)
    # loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
    # print("Training accuracy: {:.4f}".format(accuracy))
    loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
    print("Training accuracy: {:.4f}".format(accuracy))


def cnn(X_train, y_train, X_test, y_test):
    # create model
    model = Sequential()

    # add model layers
    model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(1, 4, 4, 1)))
    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(10, activation='softmax'))

    # compile model using accuracy to measure model performance
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    # train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)

    loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
    print("Testing Accuracy:  {:.4f}".format(accuracy))
