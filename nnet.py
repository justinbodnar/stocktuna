size = int( len(data)*(0.75) )

train_data = np.array( data_clean[1:size] )
train_tags = np.array( tags_clean[1:size] )
test_data = np.array( data_clean[size:] )
test_tags = np.array( tags_clean[size:] )


model = keras.Sequential()
model.add( keras.layers.Dense( 54, input_dim=54 ) )
model.add( keras.layers.Dense( 64, input_dim=26 ) )
model.add( keras.layers.Dense( 128, input_dim=13 ) )
model.add( keras.layers.Dense(2, activation=tf.nn.softmax) )

model.compile(optimizer='adam',
	loss='sparse_categorical_crossentropy',
	metrics=['accuracy'])

model.fit(train_data, train_tags, epochs=50)

test_loss, test_acc = model.evaluate(test_data, test_tags)

print('Test accuracy:', test_acc)

'''
# save model
model_json = model.to_json()
with open( "models/model.3.json", "w") as json_file:
	json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("models/blackjackmodel.3.h5")
print( "Model saved" )
'''
