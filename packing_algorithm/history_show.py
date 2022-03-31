# -*- encoding: utf-8 -*-
"""
=================================================
@path   : Packing-Algorithm -> history_show.py
@IDE    : PyCharm
@Author : zYx.Tom, 526614962@qq.com
@Date   : 2021-08-31 17:50
@Version: v0.1
@License: (C)Copyright 2020-2021, zYx.Tom
@Reference:
@Desc   :
==================================================
"""
from matplotlib import pyplot as plt


class HistoryShow(object):
    '''损失情况'''

    def showLoss(history):
        val_loss_values = history.history['val_loss']
        loss_values = history.history['loss']
        epochs = range(1, len(loss_values) + 1)
        plt.plot(epochs, loss_values, 'bo', color='#A6C8E0', label='Training loss')
        plt.plot(epochs, val_loss_values, 'b', color='#A6C8E0', label='Validation loss')
        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()
        plt.clf()

    '''准确率'''

    def showAccr(history):
        acc = history.history['accuracy']
        epochs = range(1, len(acc) + 1)
        val_acc = history.history['val_accuracy']
        plt.plot(epochs, acc, 'bo', color='#A6C8E0', label='Training acc')
        plt.plot(epochs, val_acc, 'b', color='#A6C8E0', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()
