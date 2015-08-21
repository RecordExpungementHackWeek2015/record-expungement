#-------------------------------------------------
#
# Project created by QtCreator 2015-01-04T18:45:27
#
#-------------------------------------------------

QT       += core

QT       -= gui

TARGET = pdf-form-filler
CONFIG   += console
CONFIG   -= app_bundle

TEMPLATE = app

SOURCES += main.cpp \
    formfiller.cpp \
    fieldinfo.cpp \
    maintask.cpp

CONFIG += link_pkgconfig

PKGCONFIG += poppler-qt4 QJson

HEADERS += \
    formfiller.h \
    fieldinfo.h \
    maintask.h
