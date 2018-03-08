from keras.layers import Conv1D,Input,concatenate,MaxPooling1D,Dense,Lambda
from keras.models import Model,optimizers,load_model
from keras.callbacks import EarlyStopping, ModelCheckpoint,CSVLogger
import logging
import os
import numpy as np
import keras.backend as K
import datetime as dt

from ..untils import config
from ..owlio import process_axioms
from sklearn.metrics import confusion_matrix,precision_recall_fscore_support

NUM_OP = 25
NUM_CP = 43
NUM_DP = 7

def base_model():
    input_ras = Input(shape=(NUM_OP, NUM_CP), name='ra_input')
    input_dps = Input(shape=(NUM_DP,), name='da_input')
    #first_layer = concatenate([input_dps, input_ras])
    first_layer = input_ras
    repeat = 2
    next_layer = first_layer
    for i in range(repeat):
        next_layer = repeat_conv(next_layer)
    fc = Dense(64, activation='softmax')(next_layer)
    fc = Lambda(lambda x: K.squeeze(x, 1), name='squeeze')(fc)
    fc = concatenate([fc, input_dps])
    fc = Dense(NUM_CP, activation='softmax')(fc)
    m = Model(inputs = [input_ras, input_dps], outputs = fc)
    return m


def get_inout(inds):
    in_ras = []
    in_das = []
    out_cas = []
    for k,v in inds.items():
        ras = v['mat_ra']
        #ras = ras.flatten()
        in_ras.append(ras)
        in_das.append(v['mat_da'])
        out_cas.append(v['mat_ca'])
    in_ras = np.array(in_ras)
    in_das = np.array(in_das)
    out_cas = np.array(out_cas)
    return ([in_ras, in_das], out_cas)



def test_model(mf, tbox):
    testdir = 'D:/ontologies/lubm/data/test'
    testinds = process_axioms.load_abox(testdir, tbox)
    testin, testout = get_inout(testinds)
    model = load_model(mf)
    logging.info("model loaded from %s", mf)
    ytrue = testout
    ypred =  model.predict(testin,  verbose=1,  batch_size=100)
    ytrue = ytrue.argmax(axis=-1).tolist()
    ypred = ypred.argmax(axis=-1).tolist()
    cls2id = tbox['classes']
    id2cls = dict((i,c) for (c,i) in cls2id.items())
    ytrue = [id2cls[i].name for i in ytrue]
    ypred = [id2cls[i].name for i in ypred]
    classes = list(cls2id.keys())
    classes = [c.name for c in classes]
    prediction_summary(ytrue, ypred, classes)
    #res = model.evaluate(x=testin, y=testout,batch_size=100)
    #logging.info(res)


def train_model(model, input, output):
    loss = 'categorical_crossentropy'
    opt = optimizers.Adam(lr=config.params['learning_rate'], beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
    met = ['categorical_accuracy']
    model.compile(optimizer=opt,
             loss = loss,
             metrics= met,
             )
    logging.info(model.summary())
    monitor_quant = 'val_categorical_accuracy' #'val_loss'
    model_format = os.path.join(config.model_save_dir,  dt.datetime.now().strftime('%m_%d_%H') + \
                                '_{epoch:03d}_ACC_{val_categorical_accuracy:.3f}.hdf5' )
    checkpoint_val = ModelCheckpoint(model_format, monitor=monitor_quant, verbose=1, save_best_only=True, mode='auto')
    early_stop_val = EarlyStopping(monitor=monitor_quant, patience=3, mode='auto', min_delta=-5)
    csvlogger = CSVLogger(os.path.join(config.model_save_dir, 'log.csv'), append=False, separator=',')
    callbacks_list = [
        early_stop_val,
        checkpoint_val,
        csvlogger,
    ]
    hist = model.fit(input, output,
                     verbose=0,
                     epochs=config.params['epoch'],
                     shuffle=True,
                     batch_size=config.params['batch_size'],
                     callbacks=callbacks_list,
                     validation_split=0.2,
                     )



def repeat_conv(layer):
    conv = Conv1D(filters=64, kernel_size=2, strides=1, padding='valid')(layer)
    pool = MaxPooling1D(pool_size=5, strides=3, padding='valid')(conv)
    return pool


def prediction_summary(ytrue, ypred, classes):
    ytrue = list(ytrue)
    ypred = list(ypred)
    p, r, f1, s = precision_recall_fscore_support(ytrue, ypred, average=None, labels=classes)
    headers = ["precision", "recall", "f1-score", "support"]
    head_fmt = u'{:>{width}s} ' + u' {:>9}' * len(headers)
    width = 50
    digits = 2
    report = head_fmt.format(u'', *headers, width=width)
    report += '\n\n'
    row_fmt = '{:>{width}s} ' + ' {:>9.{digits}f}' * (len(headers)-1) + u' {:>9.{digits}f}\n'
    rows = zip(classes, p, r, f1, s)
    for row in rows:
        report += row_fmt.format(*row, width=width, digits=digits)

    report += '\n'

    # compute averages
    report += row_fmt.format('avg / total',
                             np.average(p, weights=s),
                             np.average(r, weights=s),
                             np.average(f1, weights=s),
                             np.sum(s),
                             width=width, digits=digits)
    logging.info("Report:  \n  %s", report)